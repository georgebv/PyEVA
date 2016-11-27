import sys
from PyQt4 import QtGui, QtCore
from PyQt4.QtGui import QPalette


class Window(QtGui.QMainWindow):

    def __init__(self):
        super(Window, self).__init__()
        self.setGeometry(50, 50, 500, 300)
        self.setWindowTitle('PyEVA')
        self.setWindowIcon(QtGui.QIcon(r'C:\Users\georg\Documents\GitHub\PyEVA\QtGUI\images\lambda.png'))

        extractAction = QtGui.QAction('&Exit', self)
        extractAction.setShortcut('Ctrl+Q')
        extractAction.setStatusTip('Quit PyEVA')
        extractAction.triggered.connect(self.close_application)

        self.statusBar()

        mainMenu = self.menuBar()
        fileMenu = mainMenu.addMenu('&File')
        fileMenu.addAction(extractAction)

        self.home()

    def home(self):
        btn = QtGui.QPushButton('Quit', self)
        btn.clicked.connect(self.close_application)
        btn.resize(btn.minimumSizeHint())
        btn.move(0, 100)

        extractAction = QtGui.QAction(QtGui.QIcon(
            r'C:\Users\georg\Documents\GitHub\PyEVA\QtGUI\images\lambda.png'),
            'Press lambda',
            self)
        extractAction.triggered.connect(self.close_application)

        self.toolBar = self.addToolBar('Wave length')
        self.toolBar.addAction(extractAction)

        checkBox = QtGui.QCheckBox('Enlarge window', self)
        checkBox.stateChanged.connect(self.enlarge_window)
        checkBox.move(100, 25)

        self.show()

    def close_application(self):
        choice = QtGui.QMessageBox.question(self, 'Quitting the application',
                                            'Do you want to quit?', QtGui.QMessageBox.Yes |
                                            QtGui.QMessageBox.No)
        if choice == QtGui.QMessageBox.Yes:
            print('Commencing exit')
            sys.exit()
        else:
            pass

    def enlarge_window(self, state):
        if state == QtCore.Qt.Checked:
            self.setGeometry(50, 50, 1000, 600)
        else:
            self.setGeometry(50, 50, 500, 300)

def main():
    app = QtGui.QApplication(sys.argv)
    GUI = Window()
    sys.exit(app.exec_())

main()
