from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_PlayerWindow(object):
    def setupUi(self, PlayerWindow):
        PlayerWindow.setObjectName("PlayerWindow")
        PlayerWindow.resize(300, 300)
        PlayerWindow.setWindowTitle("Spotify Miniplayer")
        # PlayerWindow.setWindowFlag(QtCore.Qt.FramelessWindowHint)
        self.setWindowFlags(QtCore.Qt.Window | QtCore.Qt.FramelessWindowHint | QtCore.Qt.WindowStaysOnTopHint)
        self.centralwidget = QtWidgets.QWidget(PlayerWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.imageLabel = QtWidgets.QLabel(self.centralwidget)
        self.imageLabel.setGeometry(QtCore.QRect(0, 0, 300, 300))
        self.imageLabel.setAlignment(QtCore.Qt.AlignCenter)
        self.imageLabel.setObjectName("imageLabel")
        
        self.overlayLabel = QtWidgets.QLabel(self.centralwidget)
        self.overlayLabel.setGeometry(QtCore.QRect(0, 0, 300, 300))
        self.overlayLabel.setStyleSheet('background-color: rgba(0, 0, 0, 90)')
        self.overlayLabel.setHidden(True)
        
        self.closeBtn = QtWidgets.QPushButton(self.centralwidget)
        self.closeBtn.setGeometry(QtCore.QRect(10, 10, 40, 40))
        self.closeBtn.setStyleSheet('background:transparent;')
        self.closeBtn.setIcon(QtGui.QIcon('assets/close.png'))
        self.closeBtn.setIconSize(QtCore.QSize(40, 40))
        self.closeBtn.setHidden(True)
        font = QtGui.QFont()
        font.setPixelSize(20)
        self.nameLabel = QtWidgets.QLabel(self.centralwidget)
        self.nameLabel.setGeometry(QtCore.QRect(0, 240, 300, 30))
        self.nameLabel.setStyleSheet('color: white')
        self.nameLabel.setAlignment(QtCore.Qt.AlignCenter)
        self.nameLabel.setFont(font)
        self.nameLabel.setHidden(True)
        font.setPixelSize(11)
        self.artistLabel = QtWidgets.QLabel(self.centralwidget)
        self.artistLabel.setGeometry(QtCore.QRect(0, 260, 300, 30))
        self.artistLabel.setStyleSheet('color: white')
        self.artistLabel.setAlignment(QtCore.Qt.AlignCenter)
        self.artistLabel.setFont(font)
        self.artistLabel.setHidden(True)
        
        # self.playBtn = QtWidgets.QPushButton(self.centralwidget)
        # self.playBtn.setGeometry(QtCore.QRect(125, 200, 50, 50))
        # self.playBtn.setObjectName("playBtn")
        # self.prevBtn = QtWidgets.QPushButton(self.centralwidget)
        # self.prevBtn.setGeometry(QtCore.QRect(50, 200, 50, 50))
        # self.prevBtn.setObjectName("prevBtn")
        # self.nextBtn = QtWidgets.QPushButton(self.centralwidget)
        # self.nextBtn.setGeometry(QtCore.QRect(200, 200, 50, 50))
        # self.nextBtn.setObjectName("nextBtn")
        PlayerWindow.setCentralWidget(self.centralwidget)

        self.retranslateUi(PlayerWindow)
        QtCore.QMetaObject.connectSlotsByName(PlayerWindow)

    def retranslateUi(self, PlayerWindow):
        _translate = QtCore.QCoreApplication.translate
        PlayerWindow.setWindowTitle(_translate("PlayerWindow", "Spotify Miniplayer"))
        # self.playBtn.setText(_translate("PlayerWindow", ">"))
        # self.prevBtn.setText(_translate("PlayerWindow", "<<"))
        # self.nextBtn.setText(_translate("PlayerWindow", ">>"))
    