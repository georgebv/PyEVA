from MainWindow import Ui_MainWindow
from PyQt4 import QtGui, QtCore
import sys
import os


class PyEVAMainWindow(QtGui.QMainWindow, Ui_MainWindow):
    def __init__(self, parent=None):
        QtGui.QWidget.__init__(self, parent)
        self.setupUi(self)
        self.actionExit.triggered.connect(self.mwExit)
        self.actionNew.triggered.connect(self.mwNew)

    def mwExit(self):
        sys.stdout.write('Exiting the application')
        sys.exit(0)

    def mwNew(self):
        sys.stdout.write('Starting new PyEVA instance')
        raise RuntimeError('How do I run the same instance?')

def main():
    app = QtGui.QApplication(sys.argv)
    MainWindow = PyEVAMainWindow()
    MainWindow.show()
    sys.exit(app.exec_())

main()

