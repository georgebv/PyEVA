from MainWindow import Ui_MainWindow
from ParseDialog import Ui_Dialog as Ui_ParseDialog
from PlotSeriesDialog import Ui_Dialog as Ui_PlotSeriesDialog


from PyQt4 import QtGui, QtCore
import pandas as pd
import pickle
import sys
import subprocess
import datetime
import matplotlib.pyplot as plt
import numpy as np
from tkinter import filedialog, messagebox
import tkinter


class PyEVAMainWindow(QtGui.QMainWindow, Ui_MainWindow):

    global app_state

    def __init__(self, parent=None):
        QtGui.QWidget.__init__(self, parent)
        self.setupUi(self)
        self.mwUI_update()

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
        self.pushButton_11.clicked.connect(self.mwExportSeries)
        self.pushButton_8.clicked.connect(self.mwPlotSeries)

    ##################################################
    # Toolbar functions
    ##################################################

    def mwNew(self):
        try:
            print('Spawning a new PyEVA process')
            subprocess.Popen('PyEVa.exe', close_fds=True)
        except:
            print('WARNING: The <New> method currently does not work through Python\n'
                  'If running through executable, make sure that the PyEVA.exe'
                  ' is present in the application root directory')

    def mwSave(self):
        global app_state
        if app_state[0][0] == 'save_name':
            save_name = QtGui.QFileDialog.getSaveFileName(self, 'Save current PyEVA project',
                                                          '/project_name', '*.PyEVA')
            if save_name != '':
                print('Dumping current project state at: {}'.format(save_name))
                app_state[0][0] = save_name
                with open(save_name, 'wb') as f:
                    pickle.dump(app_state, f)
                self.setWindowTitle(' '.join(['PyEVA -', 'project', app_state[0][0].split('/')[-1].split('.')[0]]))
        else:
            print('Project state dumped at: {}'.format(app_state[0][0]))
            with open(app_state[0][0], 'wb') as f:
                pickle.dump(app_state, f)
            QtGui.QMessageBox.information(self, 'Save successful', 'Project {} saved successfully'.format(
                app_state[0][0].split('/')[-1].split('.')[0]
            ))

    def mwOpen(self):
        global app_state
        load_name = QtGui.QFileDialog.getOpenFileName(self, 'Load existing PyEVA project',
                                                      '/PyEVA project', '*.PyEVA')
        if load_name != '':
            app_state = pickle.load(open(load_name, 'rb'))
            print('Opened project at: {}'.format(app_state[0][0]))
            self.mwUI_update()

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

    ##################################################
    # Button functions
    ##################################################

    def mwParse(self):
        global app_state
        print('Opening the parser dialog window')
        app_state[1][1] = 'Extremes'
        parseUI = PyEVAParseDialog()
        parseUI.PyEVAParseDialogCloseSignal.connect(self.mwUI_update)
        parseUI.show()
        print('Parser dialog window closed with exit status {}'.format(parseUI.exec()))

    def mwLoadSeries(self):
        global app_state
        file_name = QtGui.QFileDialog.getOpenFileName(self, 'Open file', '/PyEVA parsed series', '*.csv')
        if file_name != '':
            print('Passed file at {}'.format(file_name))
            data = pd.read_csv(file_name, index_col=0)
            print(data)
            app_state[1][0] = data
            app_state[1][1] = 'Extremes'
        self.mwUI_update()

    def mwPlotSeries(self):
        global app_state
        print('Opening the time series plotting dialog window')
        plotUI = PyEVAPlotSeriesDialog()
        plotUI.show()
        print('Time series plotter dialog window closed with exit status {}'.format(plotUI.exec()))

    def mwExportSeries(self):
        global app_state
        save_name = QtGui.QFileDialog.getSaveFileName(self, 'Save current PyEVA project',
                                                      '/time series', '*.csv')
        if save_name != '':
            print('Dumping parsed time series at: {}'.format(save_name))
            app_state[1][0].to_csv(save_name)

    def mwFit(self):
        global app_state
        # Do some fitting here (state changing)
        QtGui.QMessageBox.information(self, 'Fit successful', 'Distribution fit complete')
        self.mwUI_update()

    ##################################################
    # UI handling functions
    ##################################################

    def mwUI_update(self):
        global app_state
        series = '☐'
        extremes = '☐'
        fit = '☐'

        if app_state[0][0] != 'save_name':
            self.setWindowTitle(' '.join(['PyEVA -', 'project', app_state[0][0].split('/')[-1].split('.')[0]]))

        if type(app_state[1][0]) != type('Series'):
            self.pushButton_3.setEnabled(True)
            self.pushButton_4.setEnabled(True)
            self.pushButton_8.setEnabled(True)
            self.pushButton_11.setEnabled(True)
            series = '☒'
        else:
            self.pushButton_3.setEnabled(False)
            self.pushButton_4.setEnabled(False)
            self.pushButton_8.setEnabled(False)
            self.pushButton_11.setEnabled(False)

        if type(app_state[1][1]) != type('Extremes'):
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

        app_state[0][1] = '''Extreme Value Analysis summary:


    > Time series loaded: {series}


    > Extreme values extracted: {extremes}


    > Distribution fit: {fit}
            '''.format(series=series, extremes=extremes, fit=fit)
        self.plainTextEdit.setPlainText(app_state[0][1])


class PyEVAParseDialog(QtGui.QDialog, Ui_ParseDialog):

    global app_state

    PyEVAParseDialogCloseSignal = QtCore.pyqtSignal()

    def __init__(self, parent=None):
        QtGui.QWidget.__init__(self, parent)
        self.setupUi(self)

        # Map buttons to functions
        self.pushButton.clicked.connect(self.pdPreview)
        self.pushButton_2.clicked.connect(self.pdLoad)
        self.pushButton_3.clicked.connect(self.pdParse)

    def pdLoad(self):
        global app_state
        file_name = QtGui.QFileDialog.getOpenFileName(self, 'Open file', '/data')
        if file_name != '':
            print('Passed file at {}'.format(file_name))
            self.tableWidget.clear()
            self.tableWidget.setColumnCount(0)
            self.tableWidget.setRowCount(0)
            with open(file_name, 'r') as f:
                app_state[-1][0] = [line for line in f.readlines()]
            app_state[-1][0] = [row for row in app_state[-1][0] if row != '\n']
            if len(app_state[-1][0]) > 100:
                first = ''.join(app_state[-1][0][0:50])
                mid = 'First 50 rows\n' + len((app_state[-1][0][0:50][-1])) * '-' + '\nLast 50 rows\n'
                last = ''.join(app_state[-1][0][-50:])
                self.plainTextEdit.setPlainText('\n'.join([first, mid, last]))
            else:
                self.plainTextEdit.setPlainText(''.join(app_state[-1][0]))

    def pdPreview(self):
        global app_state
        if app_state[-1][0] != 'Raw data':
            print('Parsing loaded data')
            separator = self.lineEdit.text()
            self.tableWidget.clear()
            self.tableWidget.setColumnCount(0)
            self.tableWidget.setRowCount(0)

            ##################################################
            # Parsing with dates
            ##################################################

            if self.checkBox_2.checkState():
                # Parse with headers
                if self.checkBox.checkState():
                    headers_row = self.spinBox.value() - 1
                    values_row = self.spinBox_2.value() - 1
                    headers = app_state[-1][0][headers_row]
                    headers_separator = self.lineEdit_8.text()
                    headers = headers.split(sep=headers_separator)
                    headers = [x for x in headers if len(x) > 0 and x !='\n']

                    data = [line.split(separator) for line in app_state[-1][0]][values_row:]

                    self.tableWidget.setRowCount(50)
                    self.tableWidget.setColumnCount(len(headers))

                    if self.lineEdit_2.text() != '0':
                        year = (self.spinBox_3.value() - 1, self.lineEdit_2.text())
                    else:
                        year = (self.spinBox_3.value() - 1, 'all')

                    if self.lineEdit_3.text() != '0':
                        month = (self.spinBox_4.value() - 1, self.lineEdit_3.text())
                    else:
                        month = (self.spinBox_4.value() - 1, 'all')

                    if self.lineEdit_4.text() != '0':
                        day = (self.spinBox_5.value() - 1, self.lineEdit_4.text())
                    else:
                        day = (self.spinBox_5.value() - 1, 'all')

                    if self.lineEdit_5.text() != '0':
                        hour = (self.spinBox_6.value() - 1, self.lineEdit_5.text())
                    else:
                        hour = (self.spinBox_6.value() - 1, 'all')

                    if self.checkBox_4.checkState():
                        if self.lineEdit_6.text() != '0':
                            minute = (self.spinBox_7.value() - 1, self.lineEdit_6.text())
                        else:
                            minute = (self.spinBox_7.value() - 1, 'all')
                    else:
                        minute = None

                    if self.checkBox_5.checkState():
                        if self.lineEdit_7.text() != '0':
                            second = (self.spinBox_8.value() - 1, self.lineEdit_7.text())
                        else:
                            second = (self.spinBox_8.value() - 1, 'all')
                    else:
                        second = None

                    if year[1] != 'all':
                        years = [int(x[year[0]][int(year[1].split('-')[0]) - 1:int(year[1].split('-')[1])]) for x in
                                 data]
                    else:
                        years = [int(x[year[0]]) for x in data]

                    if month[1] != 'all':
                        months = [int(x[month[0]][int(month[1].split('-')[0]) - 1:int(month[1].split('-')[1])]) for x in
                                  data]
                    else:
                        months = [int(x[month[0]]) for x in data]

                    if day[1] != 'all':
                        days = [int(x[day[0]][int(day[1].split('-')[0]) - 1:int(day[1].split('-')[1])]) for x in data]
                    else:
                        days = [int(x[day[0]]) for x in data]

                    if hour[1] != 'all':
                        hours = [int(x[hour[0]][int(hour[1].split('-')[0]) - 1:int(hour[1].split('-')[1])]) for x in
                                 data]
                    else:
                        hours = [int(x[hour[0]]) for x in data]

                    if minute is None:
                        minutes = None
                    else:
                        if minute[1] != 'all':
                            minutes = [int(x[minute[0]][int(minute[1].split('-')[0]) - 1:int(minute[1].split('-')[1])])
                                       for x in data]
                        else:
                            minutes = [int(x[minute[0]]) for x in data]

                    if second is None:
                        seconds = None
                    else:
                        if second[1] != 'all':
                            seconds = [int(x[second[0]][int(second[1].split('-')[0]) - 1:int(second[1].split('-')[1])])
                                       for x in data]
                        else:
                            seconds = [int(x[second[0]]) for x in data]

                    if minutes is None:
                        dates = [
                            datetime.datetime(
                                year=years[i],
                                month=months[i],
                                day=days[i],
                                hour=hours[i])
                            for i in range(len(data))
                            ]
                    else:
                        if seconds is None:
                            dates = [
                                datetime.datetime(
                                    year=years[i],
                                    month=months[i],
                                    day=days[i],
                                    hour=hours[i],
                                    minute=minutes[i])
                                for i in range(len(data))
                                ]
                        else:
                            dates = [
                                datetime.datetime(
                                    year=years[i],
                                    month=months[i],
                                    day=days[i],
                                    hour=hours[i],
                                    minute=minutes[i],
                                    second=seconds[i])
                                for i in range(len(data))
                                ]

                    for i, row in enumerate(data[0:50]):
                        for j, col in enumerate(row):
                            self.tableWidget.setItem(i, j, QtGui.QTableWidgetItem(str(col)))

                    if data[0][-1] == '\n':
                        data = [x[:-1] for x in data]
                    for i in range(len(data)):
                        for j in range(len(data[i])):
                            try:
                                data[i][j] = float(data[i][j])
                            except:
                                pass

                    for i in range(len(headers)):
                        self.tableWidget.setHorizontalHeaderItem(i, QtGui.QTableWidgetItem(headers[i]))
                    for i in range(50):
                        self.tableWidget.setVerticalHeaderItem(i, QtGui.QTableWidgetItem(str(dates[i])))

                # Parse without headers
                else:
                    values_row = self.spinBox_2.value() - 1
                    data = [line.split(separator) for line in app_state[-1][0]][values_row:]

                    self.tableWidget.setRowCount(50)
                    self.tableWidget.setColumnCount(len(data[50]))

                    if self.lineEdit_2.text() != '0':
                        year = (self.spinBox_3.value() - 1, self.lineEdit_2.text())
                    else:
                        year = (self.spinBox_3.value() - 1, 'all')

                    if self.lineEdit_3.text() != '0':
                        month = (self.spinBox_4.value() - 1, self.lineEdit_3.text())
                    else:
                        month = (self.spinBox_4.value() - 1, 'all')

                    if self.lineEdit_4.text() != '0':
                        day = (self.spinBox_5.value() - 1, self.lineEdit_4.text())
                    else:
                        day = (self.spinBox_5.value() - 1, 'all')

                    if self.lineEdit_5.text() != '0':
                        hour = (self.spinBox_6.value() - 1, self.lineEdit_5.text())
                    else:
                        hour = (self.spinBox_6.value() - 1, 'all')

                    if self.checkBox_4.checkState():
                        if self.lineEdit_6.text() != '0':
                            minute = (self.spinBox_7.value() - 1, self.lineEdit_6.text())
                        else:
                            minute = (self.spinBox_7.value() - 1, 'all')
                    else:
                        minute = None

                    if self.checkBox_5.checkState():
                        if self.lineEdit_7.text() != '0':
                            second = (self.spinBox_8.value() - 1, self.lineEdit_7.text())
                        else:
                            second = (self.spinBox_8.value() - 1, 'all')
                    else:
                        second = None

                    if year[1] != 'all':
                        years = [int(x[year[0]][int(year[1].split('-')[0]) - 1:int(year[1].split('-')[1])]) for x in
                                 data]
                    else:
                        years = [int(x[year[0]]) for x in data]

                    if month[1] != 'all':
                        months = [int(x[month[0]][int(month[1].split('-')[0]) - 1:int(month[1].split('-')[1])]) for x in
                                  data]
                    else:
                        months = [int(x[month[0]]) for x in data]

                    if day[1] != 'all':
                        days = [int(x[day[0]][int(day[1].split('-')[0]) - 1:int(day[1].split('-')[1])]) for x in data]
                    else:
                        days = [int(x[day[0]]) for x in data]

                    if hour[1] != 'all':
                        hours = [int(x[hour[0]][int(hour[1].split('-')[0]) - 1:int(hour[1].split('-')[1])]) for x in
                                 data]
                    else:
                        hours = [int(x[hour[0]]) for x in data]

                    if minute is None:
                        minutes = None
                    else:
                        if minute[1] != 'all':
                            minutes = [int(x[minute[0]][int(minute[1].split('-')[0]) - 1:int(minute[1].split('-')[1])])
                                       for x in data]
                        else:
                            minutes = [int(x[minute[0]]) for x in data]

                    if second is None:
                        seconds = None
                    else:
                        if second[1] != 'all':
                            seconds = [int(x[second[0]][int(second[1].split('-')[0]) - 1:int(second[1].split('-')[1])])
                                       for x in data]
                        else:
                            seconds = [int(x[second[0]]) for x in data]

                    if minutes is None:
                        dates = [
                            datetime.datetime(
                                year=years[i],
                                month=months[i],
                                day=days[i],
                                hour=hours[i])
                            for i in range(len(data))
                            ]
                    else:
                        if seconds is None:
                            dates = [
                                datetime.datetime(
                                    year=years[i],
                                    month=months[i],
                                    day=days[i],
                                    hour=hours[i],
                                    minute=minutes[i])
                                for i in range(len(data))
                                ]
                        else:
                            dates = [
                                datetime.datetime(
                                    year=years[i],
                                    month=months[i],
                                    day=days[i],
                                    hour=hours[i],
                                    minute=minutes[i],
                                    second=seconds[i])
                                for i in range(len(data))
                                ]

                    for i, row in enumerate(data[0:50]):
                        for j, col in enumerate(row):
                            self.tableWidget.setItem(i, j, QtGui.QTableWidgetItem(str(col)))

                    if data[0][-1] == '\n':
                        data = [x[:-1] for x in data]
                    for i in range(len(data)):
                        for j in range(len(data[i])):
                            try:
                                data[i][j] = float(data[i][j])
                            except:
                                pass

                    for i in range(50):
                        self.tableWidget.setVerticalHeaderItem(i, QtGui.QTableWidgetItem(str(dates[i])))

                # data = dpParse(file_name, separator=self.lineEdit.text())
                # for i in range(len(data)):
                #     self.tableWidget.setVerticalHeaderItem(i, QtGui.QTableWidgetItem(dates[i]))
                # for i in range(len(headers)):
                #     self.tableWidget.setHorizontalHeaderItem(i, QtGui.QTableWidgetItem(headers[i]))

            ##################################################
            # Parsing without dates
            ##################################################

            else:
                # Parse with headers
                if self.checkBox.checkState():
                    headers_row = self.spinBox.value() - 1
                    values_row = self.spinBox_2.value() - 1
                    data = [line.split(separator) for line in app_state[-1][0]][values_row:]
                    headers = app_state[-1][0][headers_row]
                    headers_separator = self.lineEdit_8.text()
                    headers = headers.split(sep=headers_separator)
                    headers = [x for x in headers if len(x) > 0 and x !='\n']
                    if data[0][-1] == '\n':
                        data = [x[:-1] for x in data]
                    for i in range(len(data)):
                        for j in range(len(data[i])):
                            try:
                                data[i][j] = float(data[i][j])
                            except:
                                pass
                    self.tableWidget.setRowCount(50)
                    self.tableWidget.setColumnCount(len(headers))
                    for i in range(len(headers)):
                        self.tableWidget.setHorizontalHeaderItem(i, QtGui.QTableWidgetItem(headers[i]))
                    for i, row in enumerate(data[0:50]):
                        for j, col in enumerate(row):
                            self.tableWidget.setItem(i, j, QtGui.QTableWidgetItem(str(col)))
                # Parse without headers
                else:
                    values_row = self.spinBox_2.value() - 1
                    data = [line.split(separator) for line in app_state[-1][0]][values_row:]
                    self.tableWidget.setRowCount(50)
                    self.tableWidget.setColumnCount(len(data[50]))
                    if data[0][-1] == '\n':
                        data = [x[:-1] for x in data]
                    for i in range(len(data)):
                        for j in range(len(data[i])):
                            try:
                                data[i][j] = float(data[i][j])
                            except:
                                pass
                    for i, row in enumerate(data[0:50]):
                        for j, col in enumerate(row):
                            self.tableWidget.setItem(i, j, QtGui.QTableWidgetItem(str(col)))

    def pdParse(self):
        global app_state
        print('Parsing loaded data')
        separator = self.lineEdit.text()
        self.tableWidget.clear()
        self.tableWidget.setColumnCount(0)
        self.tableWidget.setRowCount(0)

        ##################################################
        # Parsing with dates
        ##################################################

        if self.checkBox_2.checkState():
            # Parse with headers
            if self.checkBox.checkState():
                headers_row = self.spinBox.value() - 1
                values_row = self.spinBox_2.value() - 1
                headers = app_state[-1][0][headers_row]
                headers_separator = self.lineEdit_8.text()
                headers = headers.split(sep=headers_separator)
                headers = [x for x in headers if len(x) > 0 and x != '\n']

                data = [line.split(separator) for line in app_state[-1][0]][values_row:]

                self.tableWidget.setRowCount(50)
                self.tableWidget.setColumnCount(len(headers))

                if self.lineEdit_2.text() != '0':
                    year = (self.spinBox_3.value() - 1, self.lineEdit_2.text())
                else:
                    year = (self.spinBox_3.value() - 1, 'all')

                if self.lineEdit_3.text() != '0':
                    month = (self.spinBox_4.value() - 1, self.lineEdit_3.text())
                else:
                    month = (self.spinBox_4.value() - 1, 'all')

                if self.lineEdit_4.text() != '0':
                    day = (self.spinBox_5.value() - 1, self.lineEdit_4.text())
                else:
                    day = (self.spinBox_5.value() - 1, 'all')

                if self.lineEdit_5.text() != '0':
                    hour = (self.spinBox_6.value() - 1, self.lineEdit_5.text())
                else:
                    hour = (self.spinBox_6.value() - 1, 'all')

                if self.checkBox_4.checkState():
                    if self.lineEdit_6.text() != '0':
                        minute = (self.spinBox_7.value() - 1, self.lineEdit_6.text())
                    else:
                        minute = (self.spinBox_7.value() - 1, 'all')
                else:
                    minute = None

                if self.checkBox_5.checkState():
                    if self.lineEdit_7.text() != '0':
                        second = (self.spinBox_8.value() - 1, self.lineEdit_7.text())
                    else:
                        second = (self.spinBox_8.value() - 1, 'all')
                else:
                    second = None

                if year[1] != 'all':
                    years = [int(x[year[0]][int(year[1].split('-')[0]) - 1:int(year[1].split('-')[1])]) for x in
                             data]
                else:
                    years = [int(x[year[0]]) for x in data]

                if month[1] != 'all':
                    months = [int(x[month[0]][int(month[1].split('-')[0]) - 1:int(month[1].split('-')[1])]) for x in
                              data]
                else:
                    months = [int(x[month[0]]) for x in data]

                if day[1] != 'all':
                    days = [int(x[day[0]][int(day[1].split('-')[0]) - 1:int(day[1].split('-')[1])]) for x in data]
                else:
                    days = [int(x[day[0]]) for x in data]

                if hour[1] != 'all':
                    hours = [int(x[hour[0]][int(hour[1].split('-')[0]) - 1:int(hour[1].split('-')[1])]) for x in
                             data]
                else:
                    hours = [int(x[hour[0]]) for x in data]

                if minute is None:
                    minutes = None
                else:
                    if minute[1] != 'all':
                        minutes = [int(x[minute[0]][int(minute[1].split('-')[0]) - 1:int(minute[1].split('-')[1])])
                                   for x in data]
                    else:
                        minutes = [int(x[minute[0]]) for x in data]

                if second is None:
                    seconds = None
                else:
                    if second[1] != 'all':
                        seconds = [int(x[second[0]][int(second[1].split('-')[0]) - 1:int(second[1].split('-')[1])])
                                   for x in data]
                    else:
                        seconds = [int(x[second[0]]) for x in data]

                if minutes is None:
                    dates = [
                        datetime.datetime(
                            year=years[i],
                            month=months[i],
                            day=days[i],
                            hour=hours[i])
                        for i in range(len(data))
                        ]
                else:
                    if seconds is None:
                        dates = [
                            datetime.datetime(
                                year=years[i],
                                month=months[i],
                                day=days[i],
                                hour=hours[i],
                                minute=minutes[i])
                            for i in range(len(data))
                            ]
                    else:
                        dates = [
                            datetime.datetime(
                                year=years[i],
                                month=months[i],
                                day=days[i],
                                hour=hours[i],
                                minute=minutes[i],
                                second=seconds[i])
                            for i in range(len(data))
                            ]

                for i, row in enumerate(data[0:50]):
                    for j, col in enumerate(row):
                        self.tableWidget.setItem(i, j, QtGui.QTableWidgetItem(str(col)))

                if data[0][-1] == '\n':
                    data = [x[:-1] for x in data]
                for i in range(len(data)):
                    for j in range(len(data[i])):
                        try:
                            data[i][j] = float(data[i][j])
                        except:
                            pass

                for i in range(len(headers)):
                    self.tableWidget.setHorizontalHeaderItem(i, QtGui.QTableWidgetItem(headers[i]))
                for i in range(50):
                    self.tableWidget.setVerticalHeaderItem(i, QtGui.QTableWidgetItem(str(dates[i])))
                frame = pd.DataFrame(data=data, index=dates)
                frame.index.names = ['Date-time [UTC]']
                frame.columns = headers
                app_state[-1][1] = frame
            # Parse without headers
            else:
                values_row = self.spinBox_2.value() - 1
                data = [line.split(separator) for line in app_state[-1][0]][values_row:]

                self.tableWidget.setRowCount(50)
                self.tableWidget.setColumnCount(len(data[50]))

                if self.lineEdit_2.text() != '0':
                    year = (self.spinBox_3.value() - 1, self.lineEdit_2.text())
                else:
                    year = (self.spinBox_3.value() - 1, 'all')

                if self.lineEdit_3.text() != '0':
                    month = (self.spinBox_4.value() - 1, self.lineEdit_3.text())
                else:
                    month = (self.spinBox_4.value() - 1, 'all')

                if self.lineEdit_4.text() != '0':
                    day = (self.spinBox_5.value() - 1, self.lineEdit_4.text())
                else:
                    day = (self.spinBox_5.value() - 1, 'all')

                if self.lineEdit_5.text() != '0':
                    hour = (self.spinBox_6.value() - 1, self.lineEdit_5.text())
                else:
                    hour = (self.spinBox_6.value() - 1, 'all')

                if self.checkBox_4.checkState():
                    if self.lineEdit_6.text() != '0':
                        minute = (self.spinBox_7.value() - 1, self.lineEdit_6.text())
                    else:
                        minute = (self.spinBox_7.value() - 1, 'all')
                else:
                    minute = None

                if self.checkBox_5.checkState():
                    if self.lineEdit_7.text() != '0':
                        second = (self.spinBox_8.value() - 1, self.lineEdit_7.text())
                    else:
                        second = (self.spinBox_8.value() - 1, 'all')
                else:
                    second = None

                if year[1] != 'all':
                    years = [int(x[year[0]][int(year[1].split('-')[0]) - 1:int(year[1].split('-')[1])]) for x in
                             data]
                else:
                    years = [int(x[year[0]]) for x in data]

                if month[1] != 'all':
                    months = [int(x[month[0]][int(month[1].split('-')[0]) - 1:int(month[1].split('-')[1])]) for x in
                              data]
                else:
                    months = [int(x[month[0]]) for x in data]

                if day[1] != 'all':
                    days = [int(x[day[0]][int(day[1].split('-')[0]) - 1:int(day[1].split('-')[1])]) for x in data]
                else:
                    days = [int(x[day[0]]) for x in data]

                if hour[1] != 'all':
                    hours = [int(x[hour[0]][int(hour[1].split('-')[0]) - 1:int(hour[1].split('-')[1])]) for x in
                             data]
                else:
                    hours = [int(x[hour[0]]) for x in data]

                if minute is None:
                    minutes = None
                else:
                    if minute[1] != 'all':
                        minutes = [int(x[minute[0]][int(minute[1].split('-')[0]) - 1:int(minute[1].split('-')[1])])
                                   for x in data]
                    else:
                        minutes = [int(x[minute[0]]) for x in data]

                if second is None:
                    seconds = None
                else:
                    if second[1] != 'all':
                        seconds = [int(x[second[0]][int(second[1].split('-')[0]) - 1:int(second[1].split('-')[1])])
                                   for x in data]
                    else:
                        seconds = [int(x[second[0]]) for x in data]

                if minutes is None:
                    dates = [
                        datetime.datetime(
                            year=years[i],
                            month=months[i],
                            day=days[i],
                            hour=hours[i])
                        for i in range(len(data))
                        ]
                else:
                    if seconds is None:
                        dates = [
                            datetime.datetime(
                                year=years[i],
                                month=months[i],
                                day=days[i],
                                hour=hours[i],
                                minute=minutes[i])
                            for i in range(len(data))
                            ]
                    else:
                        dates = [
                            datetime.datetime(
                                year=years[i],
                                month=months[i],
                                day=days[i],
                                hour=hours[i],
                                minute=minutes[i],
                                second=seconds[i])
                            for i in range(len(data))
                            ]

                for i, row in enumerate(data[0:50]):
                    for j, col in enumerate(row):
                        self.tableWidget.setItem(i, j, QtGui.QTableWidgetItem(str(col)))

                if data[0][-1] == '\n':
                    data = [x[:-1] for x in data]
                for i in range(len(data)):
                    for j in range(len(data[i])):
                        try:
                            data[i][j] = float(data[i][j])
                        except:
                            pass

                for i in range(50):
                    self.tableWidget.setVerticalHeaderItem(i, QtGui.QTableWidgetItem(str(dates[i])))

                frame = pd.DataFrame(data=data, index=dates)
                frame.index.names = ['Date-time [UTC]']
                app_state[-1][1] = frame
            print(app_state[-1][1].head(n=10))
            app_state[1][0] = frame
            self.PyEVAParseDialogCloseSignal.emit()
            self.close()


class PyEVAPlotSeriesDialog(QtGui.QDialog, Ui_PlotSeriesDialog):

    global app_state

    def __init__(self, parent=None):
        global app_state
        QtGui.QWidget.__init__(self, parent)
        self.setupUi(self)
        data = app_state[1][0].values
        headers = app_state[1][0].columns.values
        index = app_state[1][0].index.values


        # Populate preview table
        self.tableWidget.setRowCount(50)
        self.tableWidget.setColumnCount(len(data[50]))
        for i in range(len(headers)):
            self.tableWidget.setHorizontalHeaderItem(i, QtGui.QTableWidgetItem(headers[i]))
        for i in range(50):
            self.tableWidget.setVerticalHeaderItem(i, QtGui.QTableWidgetItem(str(index[i])))
        for i, row in enumerate(data[0:50]):
            for j, col in enumerate(row):
                self.tableWidget.setItem(i, j, QtGui.QTableWidgetItem(str(col)))

        self.comboBox.clear()
        self.comboBox.addItems(list(headers))

        # Map buttons to functions
        self.pushButton.clicked.connect(self.psdPlot)

    def psdPlot(self):
        global app_state
        data = app_state[1][0]

        # Perform basic missing values handling
        data = data[data[self.comboBox.currentText()] != 999]
        data = data[data[self.comboBox.currentText()] != 999.9]
        data = data[data[self.comboBox.currentText()] != np.nan]
        try:
            data = data[data[self.comboBox.currentText()] != 'NaN']
            data = data[data[self.comboBox.currentText()] != 'None']
            data = data[data[self.comboBox.currentText()] != 'Missing']
            data = data[data[self.comboBox.currentText()] != '']
        except:
            pass

        x_values = pd.to_datetime(data.index)
        y_values = data[self.comboBox.currentText()].values

        with plt.style.context('bmh'):
            plt.figure(figsize=(18, 5))
            plt.subplot(1, 1, 1)
            marker = self.comboBox_2.currentText()
            if marker == 'x' or marker == '+':
                facecolor = 'royalblue'
                edgecolors = 'royalblue'
            else:
                facecolor = 'None'
                edgecolors = 'royalblue'
            plt.scatter(x=x_values, y=y_values, s=self.spinBox.value(),
                        marker=marker, facecolor=facecolor, edgecolors=edgecolors)
            plt.xlabel(self.lineEdit_2.text())
            plt.ylabel(self.lineEdit_3.text())
            plt.title(self.lineEdit.text())
            plt.show()


def main():
    # Initialize global program state object ([0] - GUI, [1] - EVA)
    global app_state

    app_state = [
        ['save_name', 'status_window'],
        ['Series', 'Extremes', 'Fit'],
        'EVA_class',
        ['Raw data', 'Parsed DataFrame']
    ]

    app = QtGui.QApplication(sys.argv)
    coreUI = PyEVAMainWindow()
    coreUI.show()
    sys.exit(app.exec_())

main()
