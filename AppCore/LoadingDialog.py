from PyQt4 import QtGui, QtCore
import sys
from win32api import GetSystemMetrics


class LoadingDialog(QtGui.QWidget):
    def __init__(self, parent=None):
        QtGui.QWidget.__init__(self, parent, QtCore.Qt.WindowStaysOnTopHint)
        self.movie = QtGui.QMovie('loading.gif', QtCore.QByteArray(), self)
        self.movie_screen = QtGui.QLabel()
        self.setGeometry(
            int(GetSystemMetrics(0) / 2 - 400 / 2),
            int(GetSystemMetrics(1) / 2 - 300 / 2),
            400,
            300
        )
        main_layout = QtGui.QVBoxLayout()
        main_layout.addWidget(self.movie_screen)
        main_layout.setContentsMargins(0, 0, 0, 0)
        self.setLayout(main_layout)
        self.setWindowFlags(QtCore.Qt.FramelessWindowHint)
        self.movie.setCacheMode(QtGui.QMovie.CacheAll)
        self.movie.setSpeed(150)
        self.movie_screen.setMovie(self.movie)
        self.movie.start()

if __name__ == '__main__':
    app = QtGui.QApplication(sys.argv)
    player = ImagePlayer()
    player.show()
    sys.exit(app.exec())
