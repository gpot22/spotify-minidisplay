from PyQt5 import QtCore, QtGui
import time
from random import choice
from os import scandir
from utils import get_track_id, get_track_image, get_track_name, is_track, ad_is_playing, is_playing_track, get_artist_names, display_artist_names

IDLE_TIME = 5
IMG_FLAG = False

class BackgroundLoop(QtCore.QThread):
    finished = QtCore.pyqtSignal()
    def __init__(self, win, sp):
        super().__init__()
        self.win = win
        self.sp = sp
        self.image = None
        
        self.force_toggled = False
        self.win_resized = False
        
        self.last_song_id = None
        
        self.static_image = False
        self.shuffle_image = False
        self.shuffle_timer = 0
        
        self.idle = False
        self.idle_timer = 0
        
        self.ad = False
        
        self.image_bank = [i.name for i in scandir('images')]
        
    def run(self):
        # timer = time.time()
        while True:
            # self.win.raise_()
            if self.win_resized:
                self.set_label_pixmap()
            if self.idle and not self.static_image:  # if idle, shuffle through images
                self.ad = True
                self.idle_timer = (self.idle_timer+1)%IDLE_TIME
                if self.idle_timer == 0:
                    self.set_static_image()
            elif self.shuffle_image:  # if idle, shuffle through images
                self.shuffle_timer = (self.shuffle_timer+1)%8  # shuffle every 5 seconds
                if self.shuffle_timer == 0:
                    self.set_static_image()
            # else:
            track_dict = self.sp.current_user_playing_track()
            # If ad, set random image and set text only on first iteration
            if ad_is_playing(track_dict):
                self.idle = False
                self.ad = True
                if self.win.nameLabel.text() != 'Ad':
                    self.win.nameLabel.setText('Ad')
                    self.win.artistLabel.setText('')
                    if not self.static_image and not self.shuffle_image:
                        self.set_static_image()
            # playing song
            elif is_track(track_dict) and is_playing_track(track_dict):
                self.idle = False
                self.ad = False
                temp_id = get_track_id(track_dict)
                if self.last_song_id != temp_id:  # song is different from last iteration
                    self.last_song_id = temp_id
                    self.win.nameLabel.setText(get_track_name(track_dict))
                    self.win.artistLabel.setText(display_artist_names(get_artist_names(track_dict)))
                    if not self.static_image and not self.shuffle_image:
                        self.set_image(get_track_image(track_dict))
                        self.set_label_pixmap()
            # not playing song, not playing ad
            else:
                self.idle = True
            time.sleep(1)

    def is_playing(self) -> bool:
        return not self.idle and not self.ad
    
    def get_image(self) -> str:
        return self.image
    
    def set_image(self, image) -> None:
        self.image = image
        
    def set_image_and_display(self, image) -> None:
        self.set_image(image)
        self.static_image = True
        self.set_label_pixmap(True)
    
    def force(self) -> None:
        self.force_toggled = True
        
    def get_random_image(self) -> str:
        img = choice(self.image_bank)
        
        self.image_bank = [i.name for i in scandir('images') if (not IMG_FLAG or not i.name.startswith('flag'))]
        if img in self.image_bank:
            self.image_bank.remove(img)
        else:
            print("not " + img)
        return 'images/' + img
    def set_label_pixmap(self, force=False):
        if not force and not self.win_resized:
            return
        self.win_resized = False
        pixmap = self.win.createImagePixmap(self.image) if self.image.startswith('https') else QtGui.QPixmap(self.image)
        self.win.imageLabel.setPixmap(self.win.resizePixmapToLabel(pixmap))
    
    def set_static_image(self):
        self.image = self.get_random_image()
        self.set_label_pixmap(True)
        
        
        
    