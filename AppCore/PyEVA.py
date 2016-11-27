from MainWindow import Ui_MainWindow
from PyQt4 import QtGui, QtCore
import pandas as pd
import pickle
import sys
import subprocess
import  multiprocessing


class PyEVAMainWindow(QtGui.QMainWindow, Ui_MainWindow):

    global PyEVA_state

    def __init__(self, parent=None):
        QtGui.QWidget.__init__(self, parent)
        self.setupUi(self)
        self.mwUI_activator()

        # Map toolbar actions
        self.actionExit.triggered.connect(self.mwExit)
        self.actionNew.triggered.connect(self.mwNew)
        self.actionHelp.triggered.connect(self.mwHelp)
        self.actionSave.triggered.connect(self.mwSave)
        self.actionOpen.triggered.connect(self.mwOpen)
        self.actionSettings.triggered.connect(self.mwSettings)

        # Map buttons
        self.pushButton_2.clicked.connect(self.mwLoadSeries)
        self.pushButton.clicked.connect(self.mwParse)

    # Toolbar functions

    def mwNew(self):
        try:
            print('Spawning a new PyEVA process')
            subprocess.Popen('PyEVa.exe', close_fds=True)
        except:
            print('WARNING: The <New> method currently does not work through Python\n'
                  'If running through executable, make sure that the PyEVA.exe'
                  ' is present in the application root directory')

    def mwSave(self):
        global PyEVA_state
        if PyEVA_state[0][0] == 'save_name':
            save_name = QtGui.QFileDialog.getSaveFileName(self, 'Save current PyEVA project',
                                                          '/project_name', '*.PyEVA')
            if save_name != '':
                print('Dumping current project state at: {}'.format(save_name))
                PyEVA_state[0][0] = save_name
                with open(save_name, 'wb') as f:
                    pickle.dump(PyEVA_state, f)
                self.setWindowTitle(' '.join(['PyEVA -', 'project', PyEVA_state[0][0].split('/')[-1].split('.')[0]]))
            else:
                pass
        else:
            print('Project state dumped at: {}'.format(PyEVA_state[0][0]))
            with open(PyEVA_state[0][0], 'wb') as f:
                pickle.dump(PyEVA_state, f)
            QtGui.QMessageBox.information(self, 'Save successful', 'Project {} saved successfully'.format(
                PyEVA_state[0][0].split('/')[-1].split('.')[0]
            ))

    def mwOpen(self):
        global PyEVA_state
        load_name = QtGui.QFileDialog.getOpenFileName(self, 'Load existing PyEVA project',
                                                      '/PyEVA project', '*.PyEVA')
        if load_name != '':
            PyEVA_state = pickle.load(open(load_name, 'rb'))
            print('Opened project at: {}'.format(PyEVA_state[0][0]))
            self.mwUI_activator()

    def mwSettings(self):
        # TODO: make <Settings> method work
        QtGui.QMessageBox.warning(self, 'Warning', 'Settings option is not yet implemented')

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

    # Button functions

    def mwParse(self):
        global PyEVA_state
        # Todo: make the <Parse> method work
        # PyEVA_state[1][1] = 'Extremes'
        self.mwUI_activator()
        QtGui.QMessageBox.warning(self, 'Warning', 'Parsing module is not yet implemented')

    def mwLoadSeries(self):
        global PyEVA_state
        file_name = QtGui.QFileDialog.getOpenFileName(self, 'Open file', '/PyEVA parsed series', '*.csv')
        if file_name != '':
            print('Passed file at {}'.format(file_name))
            data = pd.read_csv(file_name, index_col=0)
            data.index = pd.to_datetime(data.index)
            PyEVA_state[1][0] = data
            PyEVA_state[1][1] = 'Extremes'
        self.mwUI_activator()

    def mwFit(self):
        global PyEVA_state
        # Do some fitting here (state changing)
        QtGui.QMessageBox.information(self, 'Fit successful', 'Distribution fit complete')

    # Auxiliary functions

    def mwUI_activator(self):
        global PyEVA_state
        series = '☐'
        extremes = '☐'
        fit = '☐'
        if PyEVA_state[0][0] != 'save_name':
            self.setWindowTitle(' '.join(['PyEVA -', 'project', PyEVA_state[0][0].split('/')[-1].split('.')[0]]))
        if type(PyEVA_state[1][0]) != type('Series'):
            self.pushButton_3.setEnabled(True)
            self.pushButton_4.setEnabled(True)
            series = '☒'
        else:
            self.pushButton_3.setEnabled(False)
            self.pushButton_4.setEnabled(False)
        if type(PyEVA_state[1][1]) != type('Extremes'):
            self.comboBox_2.setEnabled(True)
            self.checkBox.setEnabled(True)
            self.pushButton_5.setEnabled(True)
            self.label_4.setEnabled(True)
            self.label_5.setEnabled(True)
            extremes = '☒'
        else:
            self.comboBox_2.setEnabled(False)
            self.checkBox.setEnabled(False)
            self.pushButton_5.setEnabled(False)
            self.label_4.setEnabled(False)
            self.label_5.setEnabled(False)
        PyEVA_state[0][1] = '''Extreme Value Analysis summary:


    > Time series loaded: {series}


    > Extreme values extracted: {extremes}


    > Distribution fit: {fit}
            '''.format(series=series, extremes=extremes, fit=fit)
        self.plainTextEdit.setPlainText(PyEVA_state[0][1])

def main():
    # Initialize global program state object ([0] - GUI, [1] - EVA)
    global PyEVA_state
    status_pane = '''Extreme Value Analysis summary:


        > Time series loaded: {series}


        > Extreme values extracted: {extremes}


        > Distribution fit: {fit}
    '''.format(series='☐', extremes='☐', fit='☐')
    PyEVA_state = [['save_name', status_pane], ['Series', 'Extremes', 'Fit'], 'EVA_class']
    app = QtGui.QApplication(sys.argv)
    MainWindow = PyEVAMainWindow()
    MainWindow.show()
    sys.exit(app.exec_())

main()


