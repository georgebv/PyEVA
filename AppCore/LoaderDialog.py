import sys
from PyQt4 import QtGui, QtCore
import time


class Loader(QtGui.QWidget):

    def __init__(self, parent=None):
        QtGui.QWidget.__init__(self, parent)
        self.setWindowTitle('Processing...')
        self.movie_screen = QtGui.QLabel()
        main_layout = QtGui.QVBoxLayout()
        main_layout.setContentsMargins(0, 0, 0, 0)
        main_layout.addWidget(self.movie_screen)
        self.setLayout(main_layout)
        self.setWindowFlags(QtCore.Qt.FramelessWindowHint)
        self.movie = QtGui.QMovie(r".\loading.gif", QtCore.QByteArray(), self)
        self.movie.setCacheMode(QtGui.QMovie.CacheAll)
        self.movie.setSpeed(200)
        self.movie_screen.setMovie(self.movie)
        self.movie.start()


app = QtGui.QApplication(sys.argv)
player = Loader()
player.show()
sys.exit(app.exec_())



