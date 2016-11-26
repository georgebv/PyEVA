from MainWindow import Ui_MainWindow
from PyQt4 import QtGui, QtCore
import pandas as pd
import pickle
import sys
import os


# Setup current project state (a global variable, must be declared as global in each function / method)
# First item - GUI state, second item - internal EVA state
#  Store all global variable in PyEVA_state
PyEVA_state = [['save_name', 'None'], ['Series', 'None']]


class PyEVAMainWindow(QtGui.QMainWindow, Ui_MainWindow):

    global PyEVA_state

    def __init__(self, parent=None):
        QtGui.QWidget.__init__(self, parent)
        self.setupUi(self)

        # Map actions
        self.actionExit.triggered.connect(self.mwExit)
        self.actionNew.triggered.connect(self.mwNew)
        self.actionHelp.triggered.connect(self.mwHelp)
        self.actionSave.triggered.connect(self.mwSave)
        self.actionOpen.triggered.connect(self.mwOpen)

        # Map buttons
        self.pushButton_2.clicked.connect(self.mwLoadSeries)
        self.pushButton.clicked.connect(self.mwParse)

    def mwNew(self):
        # TODO: make <New> method work
        print('Starting new PyEVA instance')
        QtGui.QMessageBox.warning(self, 'Warning', 'New project option is not yet implemented')

    def mwSave(self):
        global PyEVA_state
        print('Current save_name is: {}'.format(PyEVA_state[0][0]))
        if PyEVA_state[0][0] == 'save_name':
            save_name = QtGui.QFileDialog.getSaveFileName(self, 'Save current PyEVA project', '/project_name')
            if save_name != '':
                save_name += '.PyEVA'
                print('Passed project save path at: {}'.format(save_name))
                PyEVA_state[0][0] = save_name
                with open(save_name, 'wb') as f:
                    pickle.dump(PyEVA_state, f)
                self.setWindowTitle(' '.join(['PyEVA -', 'project', PyEVA_state[0][0].split('/')[-1].split('.')[0]]))
            else:
                pass
        else:
            print('Saved project at: {}'.format(PyEVA_state[0][0]))
            with open(PyEVA_state[0][0], 'wb') as f:
                pickle.dump(PyEVA_state, f)
            QtGui.QMessageBox.information(self, 'Save successful', 'Project saved successfully')

    def mwOpen(self):
        global PyEVA_state
        load_name = QtGui.QFileDialog.getOpenFileName(self, 'Load existing PyEVA project', '/PyEVA project', '*.PyEVA')
        if load_name != '':
            PyEVA_state = pickle.load(open(load_name, 'rb'))
            print('Opened project at: {}'.format(PyEVA_state[0][0]))
            # TODO: make the PyEVA_state variable update the program state
            self.setWindowTitle(' '.join(['PyEVA -', 'project', PyEVA_state[0][0].split('/')[-1].split('.')[0]]))
                # Button state
        else:
            pass

    def mwHelp(self):
        help_dialog = QtGui.QMessageBox.about(self, 'Help', 'PyEVA, an Extreme Value Analysis application\n'
                                                            'Build 0.1b, built on November 26, 2016\n\n'
                                                            'Powered by open source software\n'
                                                            'Designed by Georgii Bocharov\n'
                                                            'For reference go to https://github.com/georgebv/PyEVA\n\n'
                                                            'Licenced under GPLv3')

    def mwExit(self):
        choice = QtGui.QMessageBox.question(self, 'Exit application', 'You are about to quit PyEVA. Proceed?',
                                            QtGui.QMessageBox.Yes | QtGui.QMessageBox.No)
        if choice == QtGui.QMessageBox.Yes:
            print('Closing the application')
            sys.exit(0)
        else:
            pass

    def mwParse(self):
        global PyEVA_state
        # Todo: make the <Parse> method work
        QtGui.QMessageBox.warning(self, 'Warning', 'Parsing module is not yet implemented')

    def mwLoadSeries(self):
        global PyEVA_state
        # TODO: make proper data import from csv
        file_name = QtGui.QFileDialog.getOpenFileName(self, 'Open file', '/PyEVA parsed series', '*.csv')
        if file_name != '':
            print('Passed file at {}'.format(file_name))
            data = pd.read_csv(file_name)
            # make data into a DataFrame with datetime index and regular columns
            # PyEVA_state[1][0] = data
        else:
            pass

def main():
    app = QtGui.QApplication(sys.argv)
    MainWindow = PyEVAMainWindow()
    MainWindow.show()
    sys.exit(app.exec_())

main()


