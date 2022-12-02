import time
from PyQt5 import QtWidgets, QtGui, QtCore
import spotipy
from spotipy.oauth2 import SpotifyClientCredentials, SpotifyOAuth
import urllib.request

from windowUI import Ui_PlayerWindow
from backgroundtask import BackgroundLoop
from utils import get_track_image

import json

# client details
with open('my_client.json', 'r') as f:
    my_client_info = json.load(f)
'''
{
    "client_id": "id_string",
    "client_secret": "secret_string",
    "redirect_uri": "uri_string",
}
'''
client_id = my_client_info["client_id"]
client_secret = my_client_info["client_secret"]
redirect_uri = my_client_info["redirect_uri"]
client_credentials_manager = SpotifyClientCredentials(
    client_id=client_id, client_secret=client_secret)

# auth details
scope = 'user-read-recently-played user-read-playback-position ' \
        'user-top-read playlist-read-collaborative playlist-modify-public ' \
        'playlist-read-private playlist-modify-private user-read-email ' \
        'user-library-modify user-library-read streaming ' \
        'user-read-currently-playing user-modify-playback-state user-read-playback-state ugc-image-upload'
sp = spotipy.Spotify(client_credentials_manager=client_credentials_manager, auth_manager=SpotifyOAuth(
    scope=scope, client_id=client_id, client_secret=client_secret, redirect_uri=redirect_uri))

SCR_YLIM = 25  # can't drag higher than y=25 on mac :b

class MyPlayerWindow(Ui_PlayerWindow, QtWidgets.QMainWindow):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.pressing = False
        self.force_details = False
        self.clickTimer = 0
        # start background loop
        self.bgLoop = BackgroundLoop(self, sp)
        self.bgLoop.start()
        # initialize variables for resizing the window
        self.gripSize = 16
        self.grips = []
        for _ in range(4):
            grip = QtWidgets.QSizeGrip(self)
            grip.resize(self.gripSize, self.gripSize)
            self.grips.append(grip)
        # min/max window dimensions
        self.setMinimumWidth(200)
        self.setMinimumHeight(200)
        self.myAspectRatio = 1
        # default image
        self.bgLoop.set_image('images/milkmochacomfy.png')
        pixmap = QtGui.QPixmap('images/milkmochacomfy.png')
        pixmap = self.resizePixmapToLabel(pixmap)
        self.imageLabel.setPixmap(pixmap)
        
        self.closeBtn.clicked.connect(self.close)
        
        # Hotkeys
        self.shortcut1 = QtWidgets.QShortcut(QtGui.QKeySequence('1'), self)
        self.shortcut1.activated.connect(lambda: self.bgLoop.set_image_and_display('images/milkmochacomfy.png'))
        self.shortcut2 = QtWidgets.QShortcut(QtGui.QKeySequence('2'), self)
        self.shortcut2.activated.connect(lambda: self.bgLoop.set_image_and_display('images/dinoxmas.png'))
        self.shortcut9 = QtWidgets.QShortcut(QtGui.QKeySequence('9'), self)
        self.shortcut9.activated.connect(lambda: self.bgLoop.set_image_and_display('images/snowybg.png'))
        
        # keep details on screen?
        self.shortcut0 = QtWidgets.QShortcut(QtGui.QKeySequence('0'), self)
        self.shortcut0.activated.connect(lambda:self.toggleForceDetails())

    # - - - - - - - - - - - WINDOW EVENT OVERRIDES - - - - - - - - - - -
    # Handle resizing
    def resizeEvent(self, ev):
        super().resizeEvent(ev)
        self.handleWindowResize()
        self.handleWindowAspectRatio()
        self.imageLabel.setGeometry(0, 0, self.width(), self.height())
        self.overlayLabel.setGeometry(0, 0, self.width(), self.height())
        w = self.width()-(70*(max(1, self.width()//250)))
        self.nameLabel.setGeometry(0, w, self.width(), 30)
        self.artistLabel.setGeometry(0, w + 20, self.width(), 30)
        self.bgLoop.win_resized = True

    # Handle dragging
    def mousePressEvent(self, ev):
        self.start = self.mapToGlobal(ev.pos())
        self.pressing = True
        self.clickTimer = time.time()

    def mouseMoveEvent(self, ev):
        if self.pressing:
            self.end = self.mapToGlobal(ev.pos())
            self.movement = self.end-self.start
            if self.movement.y() < 0 and -5 < self.geometry().y() < 26 and -5 < self.end.y()<26:  # mac doesnt let you go above y=25; fix bug related to this
                self.end = QtCore.QPoint(self.end.x(), self.start.y())
                self.movement = QtCore.QPoint(self.movement.x(), 0)
            self.move(self.mapToGlobal(self.movement).x(), self.mapToGlobal(self.movement).y())
            self.start = self.end

    def mouseReleaseEvent(self, ev):
        self.pressing = False
        self.setFocus()
        if(time.time() - self.clickTimer <= 0.15):  # register as a click
            if ev.button() == 1:  # toggle random image
                self.bgLoop.static_image = (not self.bgLoop.static_image or not self.bgLoop.is_playing())
                self.bgLoop.shuffle_image = False
                if self.bgLoop.static_image:
                    self.bgLoop.set_static_image()
                else:
                    sp_dict = sp.currently_playing()
                    img = get_track_image(sp_dict)
                    self.bgLoop.set_image(img)
                    self.bgLoop.set_label_pixmap()
                    
                    # self.bgLoop.last_song_id = None  # make it reset to track image
            elif ev.button() == 2:  # shuffle images
                self.bgLoop.shuffle_image = (not self.bgLoop.shuffle_image or not self.bgLoop.is_playing())
                self.bgLoop.static_image = False
                if self.bgLoop.shuffle_image:
                    self.bgLoop.set_static_image()
                else:
                    sp_dict = sp.currently_playing()
                    img = get_track_image(sp_dict)
                    self.bgLoop.set_image(img)
                    self.bgLoop.set_label_pixmap()
    # Handle mouse in/out
    def enterEvent(self, ev):
        if not self.force_details:
            self.showDetails()
        self.closeBtn.setHidden(False)
        
    def leaveEvent(self, ev):
        if not self.pressing and not self.force_details:
            self.hideDetails()
        self.closeBtn.setHidden(True)

    # - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
    # - - - - - - - - - - - - - - - - Window Resizing - - - - - - - - - - - - - - - -
    def handleWindowResize(self):
        rect = self.rect()
        # top left grip doesn't need to be moved...
        # top right
        self.grips[1].move(rect.right() - self.gripSize, 0)
        # bottom right
        self.grips[2].move(
            rect.right() - self.gripSize, rect.bottom() - self.gripSize)
        # bottom left
        self.grips[3].move(0, rect.bottom() - self.gripSize)

    def handleWindowAspectRatio(self):
        if self.width() * self.myAspectRatio != self.height():
            self.resize(self.width(), self.width())

    # def handleImageResize(self):
    #     self.imageLabel.setGeometry(0, 0, self.width(), self.height())
    #     image = self.bgLoop.get_image()
    #     if image == None:
    #         return
    #     # pixmap = self.createImagePixmap(image)
    #     # pixmap = self.resizePixmapToLabel(pixmap)
    #     # self.imageLabel.setPixmap(pixmap)
    
    def createImagePixmap(self, url):
        data = urllib.request.urlopen(url).read()
        pixmap = QtGui.QPixmap()
        pixmap.loadFromData(data)
        return pixmap

    def resizePixmapToLabel(self, pixmap):
        return pixmap.scaled(self.imageLabel.width(), self.imageLabel.height())

    def resizeImagePixmap(self, pixmap, w, h):
        return pixmap.scaled(w, h)

    def showDetails(self):
        self.overlayLabel.setHidden(False)
        # self.closeBtn.setHidden(False)
        self.nameLabel.setHidden(False)
        self.artistLabel.setHidden(False)
    
    def hideDetails(self):
        self.overlayLabel.setHidden(True)
        # self.closeBtn.setHidden(True)
        self.nameLabel.setHidden(True)
        self.artistLabel.setHidden(True)
    
    def toggleForceDetails(self):
        self.force_details = not self.force_details
        return self.showDetails() if self.force_details else self.hideDetails()
        

if __name__ == "__main__":
    '''My app runs on 5 lines of code yepyep ez B)'''
    import sys
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = MyPlayerWindow()
    MainWindow.show()
    sys.exit(app.exec_())
