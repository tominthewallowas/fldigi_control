#!/usr/bin/env python3

# Filename: fldigi_control_mxe.py

"""
    Fldigi Control Maintenance is a GUI program to maintain entries for the companion program Fldigi Control.
    The program utilizes the PyQt5 widget library instead of PySide2 so it will work on a Raspberry Pi 4.
    Author: Tom Bingham
    Email: <my first name> at wb7eux period radio
    Date: 2/22/2021
"""

import sys

from PyQt5.QtWidgets import (QApplication, QMainWindow, QWidget,
                             QLineEdit, QPushButton, QVBoxLayout,
                             QHBoxLayout, QFormLayout, QTextEdit,
                             QWidget, QComboBox, QCheckBox,
                             QTableWidget, QTableWidgetItem, QButtonGroup,
                             QTimeEdit)
from PyQt5.QtCore import (QDateTime, QTime)

import app_constants as ac
from sqlitedb import SQLiteDB
from sql_statements import retrieveSQL

__version__ = '0.1'
__author__ = 'Tom Bingham'

# Global constant to handle errors
ERROR_MSG = 'ERROR'

class FCMUi(QMainWindow):
    """Fldigi Control Maintenance View (GUI)."""

    def __init__(self):
        """View initializer"""
        super().__init__()
        self.setWindowTitle('Fldigi Controller Maintenance')
        self.db = SQLiteDB(db_type="fldigi_control.db")
        self.setInitialWindowValues()
        self.setInitialFormValues()
        self.setInitialButtonValues()
        self.setInitialProgramsTableValues()
        self.setInitialAppValues()
        self.setupMethods()
        self.loadComboBoxes()
        self.loadProgramsTable()

    def setInitialAppValues(self):
        ''' Catch all for various application values. '''
        self.setFieldStatus(status=ac.DISABLE)
        self.setButtonStatus(ac.APP_STARTUP)
        self.dbPending = ac.DBPENDING_NONE
        self.primary_key = None

    def setInitialButtonValues(self):
        ''' Setup a button bar and related button group. '''
        self.buttonLayout = QHBoxLayout()
        self.generalLayout.addLayout(self.buttonLayout)
        self.buttonGroup = QButtonGroup()
        self.addPushButtons(self.buttonGroup)

    def setInitialFormValues(self):
        ''' Setup a form for data entry. '''
        self.frmLayout = QFormLayout()
        self.generalLayout.addLayout(self.frmLayout)
        self.createFormFields()

    def setInitialWindowValues(self):
        ''' Setup the basic window system. '''
        self.generalLayout = QVBoxLayout()
        self.centralwidget = QWidget(self)
        self.setCentralWidget(self.centralwidget)
        self.centralwidget.setLayout(self.generalLayout)

    def setInitialProgramsTableValues(self):
        ''' Setup a table to contain data specific to Fldigi Control values. '''
        self.tblPrograms = QTableWidget(self.centralwidget)
        self.hboxTable = QHBoxLayout()
        self.hboxTable.addWidget(self.tblPrograms)
        self.generalLayout.addLayout(self.hboxTable)
        self.tblPrograms.setEnabled(True)
        self.tblPrograms.setColumnCount(0)
        self.tblPrograms.setRowCount(0)
        self.tblPrograms.horizontalHeader().setVisible(True)
        self.tblPrograms.verticalHeader().setVisible(False)
        headerLabels =["Id", "Program", "Station", "Freq", "Mode", "BW", "Modem", "Cntr", "Day", "UTC Time", "Active", "Notes"]
        self.tblPrograms.setColumnCount(len(headerLabels))
        self.tblPrograms.setHorizontalHeaderLabels(headerLabels)
        #The following column widths follow headerLabels coded above. Id column is set to zero to hide it.
        self.tblPrograms.setColumnWidth(0, 0)
        self.tblPrograms.setColumnWidth(1, 200)
        self.tblPrograms.setColumnWidth(2, 100)
        self.tblPrograms.setColumnWidth(3, 100)
        self.tblPrograms.setColumnWidth(4, 100)
        self.tblPrograms.setColumnWidth(5, 100)
        self.tblPrograms.setColumnWidth(6, 100)
        self.tblPrograms.setColumnWidth(7, 100)
        self.tblPrograms.setColumnWidth(8, 100)
        self.tblPrograms.setColumnWidth(9, 100)
        self.tblPrograms.setColumnWidth(10, 100)
        self.tblPrograms.setColumnWidth(11, 200)

    def loadComboBoxes(self):
        values = []
        select_constants = [ac.RADIO_FREQUENCIES, ac.CENTER_DATA_FREQUENCIES, ac.MODES, ac.MODEMS, ac.RADIO_STATIONS, ac.BANDWIDTHS]
        combo_boxes = [self.frmComboFreq, self.frmComboCenterFreq, self.frmComboMode, self.frmComboModem, self.frmComboStation, self.frmComboBandwidth]

        for index, select_constant in enumerate(select_constants):
            result = self.db.select(retrieveSQL(select_constant))
            combo_boxes[index].addItems([x[0] for x in result])
        
        self.frmComboDOW.addItems(('Sun', 'Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat'))

    def loadProgramsTable(self):
        ''' Load the table from the database. '''
        self.tblPrograms.setRowCount(0)
        self.dbPending = ac.DBPENDING_SELECT
        result = self.handleDatabaseRequest()
        self.tblPrograms.setRowCount(len(result))
        self.tblPrograms.setSortingEnabled(ac.DISABLE)
        for record in enumerate(result):
            for item in enumerate(record[1]):
                self.tblPrograms.setItem(int(record[0]), int(item[0]), QTableWidgetItem(str(item[1])))
                
    def setupMethods(self):
        '''Uses the button group to connect a button via its constant to a method director.'''
        self.buttonGroup.buttonClicked[int].connect(self.methodDirector)
        self.tblPrograms.clicked.connect(self.tblProgramsClicked)
        self.frmComboFreq.currentIndexChanged[str].connect(self.handleComboBox)

    def handleComboBox(self):
        self.frmComboFreq.currentData()

    def methodDirector(self, buttonid):
        '''Identifies a button and its related method using a constant and the button id.'''
        if buttonid == ac.PUSHBUTTON_QUIT:
            self.close()
        elif buttonid == ac.PUSHBUTTON_ADD:
            self.addButtonAction()
        elif buttonid == ac.PUSHBUTTON_CANCEL:
            self.cancelButtonAction()
        elif buttonid == ac.PUSHBUTTON_SAVE:
            self.saveButtonAction()
        elif buttonid == ac.PUSHBUTTON_EDIT:
            self.editButtonAction()
        elif buttonid == ac.PUSHBUTTON_DELETE:
            self.deleteButtonAction()

    def tblProgramsClicked(self):
        self.clearFields()
        '''Note the explicit creation of a tuple in the next line. This is to keep Sqlite happy.'''
        self.primary_key = (self.tblPrograms.item(self.tblPrograms.currentRow(), 0).text(), )
        self.setButtonStatus(ac.APP_LISTCHANGE)
    
    def deleteButtonAction(self):
        ''' Set the database pending value, handle the database action, and set button status. '''
        self.dbPending = ac.DBPENDING_DELETE
        self.handleDatabaseRequest()
        self.setButtonStatus(status=ac.APP_DELETE)

    def editButtonAction(self):
        ''' Set the database pending value, handle the database action, and set button status. '''
        self.dbPending = ac.DBPENDING_UPDATE
        self.setFieldStatus(status=ac.ENABLE)
        self.setButtonStatus(ac.APP_EDIT)
        tabledata = self.extractTableData()
        self.populateFields(tabledata)
        self.frmFieldProgram.setFocus()

    def populateFields(self, tabledata):
        self.primary_key = tabledata[0]
        tabledata = tabledata[1:]
        fieldlist = [self.frmFieldProgram, self.frmComboStation, self.frmComboFreq, self.frmComboMode, self.frmComboBandwidth, self.frmComboModem,  self.frmComboCenterFreq, self.frmComboDOW, self.frmUTCTimeEdit, self.frmCheckBoxActive, self.frmTextEditNotes]

        for list_index, item in enumerate(fieldlist):
            if isinstance(item, QCheckBox):
                if tabledata[list_index] == "Yes":
                    item.setChecked(True)
                else:
                    item.setChecked(False)
            elif isinstance(item, QComboBox):
                item.setCurrentIndex(item.findText(tabledata[list_index]))
            elif isinstance(item, QTimeEdit):
                self.frmUTCTimeEdit.setTime(QTime.fromString(tabledata[list_index], 'hh:mm'))
            elif isinstance(item, QLineEdit) or isinstance(item, QTextEdit):
                item.setText(tabledata[list_index])

    def extractTableData(self):
        '''This method primarily gathers data from the Program table widget and places the data into a list which is returned.'''
        tabledata = []
        for column_number in range(0, self.tblPrograms.columnCount()):
            tabledata.append(self.tblPrograms.item(self.tblPrograms.currentRow(), column_number).text())
        return tabledata

    def saveButtonAction(self):
        ''' Set the database pending value, handle the database action, and set button status. '''
        self.setButtonStatus(status=ac.APP_SAVE)
        self.handleDatabaseRequest()
        self.clearFields()

    def handleDatabaseRequest(self):
        result = None
        field_data = None
        if self.dbPending == ac.DBPENDING_SELECT:
            result = self.db.select(retrieveSQL(ac.SQL_SELECT_ALL))
        elif self.dbPending == ac.DBPENDING_INSERT:
            field_data = self.extractFieldData()
            self.db.insertData(retrieveSQL(ac.SQL_INSERT), (field_data, ))
            self.loadProgramsTable()
        elif self.dbPending == ac.DBPENDING_DELETE:
            self.db.deleteRow(retrieveSQL(ac.SQL_DELETE), (self.primary_key))
            self.loadProgramsTable()
        elif self.dbPending == ac.DBPENDING_UPDATE:
            field_data = self.extractFieldData()
            field_data.append(self.primary_key)
            self.db.updateData(retrieveSQL(ac.SQL_UPDATE), field_data)
            self.loadProgramsTable()
        return result

    def extractFieldData(self):
        fielddata = []
        fieldList = [self.frmFieldProgram, self.frmComboStation, self.frmComboFreq, self.frmComboMode, self.frmComboBandwidth, self.frmComboModem,  self.frmComboCenterFreq, self.frmComboDOW, self.frmUTCTimeEdit, self.frmCheckBoxActive, self.frmTextEditNotes]
        for item in fieldList:
            item_text = ''
            if isinstance(item, QCheckBox):
                item_text = "Yes" if item.isChecked() else "No"
            elif isinstance(item, QTextEdit):
                item_text = item.toPlainText()
            elif isinstance(item, QComboBox):
                item_text = item.currentText()
            elif isinstance(item, QLineEdit):
                item_text = item.displayText()
            elif isinstance(item, QTimeEdit):
                item_text = item.time().toString('hh:mm')
            fielddata.append(item_text)
        return fielddata

    def cancelButtonAction(self):
        '''Perform actions related to the cancel button click.'''
        self.dbPending = ac.DBPENDING_NONE
        self.clearFields()
        self.setFieldStatus(ac.DISABLE)
        self.setButtonStatus(ac.APP_CANCEL)

    def addButtonAction(self):
        '''Perform actions related to the add button click.'''
        self.dbPending = ac.DBPENDING_INSERT
        self.clearFields()
        self.setFieldStatus(status=ac.ENABLE)
        self.setButtonStatus(status=ac.APP_ADD)
        self.frmFieldProgram.setFocus()

    def setButtonStatus(self, status=0):
        '''Set buttons on or off depending on the state of the app.'''
        # Set default status of all buttons which all but the quit are disabled.
        self.btnAdd.setEnabled(False)
        self.btnEdit.setEnabled(False)
        self.btnCancel.setEnabled(False)
        self.btnSave.setEnabled(False)
        self.btnDelete.setEnabled(False)
        self.btnQuit.setEnabled(True)

        # Now, using the status word, set buttons on or off.
        if status in (ac.APP_STARTUP, ac.APP_SAVE):
            self.btnAdd.setEnabled(True)
        elif status == ac.APP_LISTCHANGE:
            self.btnAdd.setEnabled(True)
            self.btnEdit.setEnabled(True)
            self.btnDelete.setEnabled(True)
        elif status == ac.APP_ADD:
            self.btnAdd.setEnabled(False)
            self.btnCancel.setEnabled(True)
            self.btnSave.setEnabled(True)
        elif status == ac.APP_CANCEL:
            self.btnAdd.setEnabled(True)
        elif status == ac.APP_DELETE:
            self.btnAdd.setEnabled(True)
        elif status == ac.APP_EDIT:
            self.btnCancel.setEnabled(True)
            self.btnSave.setEnabled(True)

        
    def setFieldStatus(self, status):
        '''Turns data fields on or off.'''
        self.frmFieldProgram.setEnabled(status)
        self.frmCheckBoxActive.setEnabled(status)
        self.frmTextEditNotes.setEnabled(status)
        self.frmComboFreq.setEnabled(status)
        self.frmComboMode.setEnabled(status)
        self.frmComboCenterFreq.setEnabled(status)
        self.frmComboModem.setEnabled(status)
        self.frmComboStation.setEnabled(status)
        self.frmUTCTimeEdit.setEnabled(status)
        self.frmComboBandwidth.setEnabled(status)
        self.frmComboDOW.setEnabled(status)

    def clearFields(self):
        '''Clear all fields of any information.'''
        self.frmFieldProgram.setText("")
        self.frmCheckBoxActive.setChecked(True)
        self.frmTextEditNotes.setText("")

    def addPushButtons(self, buttonGroup):
        self.btnAdd = QPushButton("&Add", self.centralwidget)
        self.buttonLayout.addWidget(self.btnAdd)
        buttonGroup.addButton(self.btnAdd, ac.PUSHBUTTON_ADD) 
        self.btnEdit = QPushButton("&Edit", self.centralwidget)
        self.buttonLayout.addWidget(self.btnEdit)
        buttonGroup.addButton(self.btnEdit, ac.PUSHBUTTON_EDIT) 
        self.btnCancel = QPushButton("&Cancel", self.centralwidget)
        self.buttonLayout.addWidget(self.btnCancel)
        buttonGroup.addButton(self.btnCancel, ac.PUSHBUTTON_CANCEL) 
        self.btnSave = QPushButton("&Save", self.centralwidget)
        self.buttonLayout.addWidget(self.btnSave)
        buttonGroup.addButton(self.btnSave, ac.PUSHBUTTON_SAVE) 
        self.btnDelete = QPushButton("&Delete", self.centralwidget)
        self.buttonLayout.addWidget(self.btnDelete)
        buttonGroup.addButton(self.btnDelete, ac.PUSHBUTTON_DELETE) 
        self.btnQuit = QPushButton("&Quit", self.centralwidget)
        self.buttonLayout.addWidget(self.btnQuit)
        buttonGroup.addButton(self.btnQuit, ac.PUSHBUTTON_QUIT) 

    def createFormFields(self):
        self.frmFieldProgram = QLineEdit(self.centralwidget)
        self.frmLayout.addRow("Program:", self.frmFieldProgram)

        self.frmComboStation = QComboBox(self.centralwidget)
        self.frmLayout.addRow("Station:", self.frmComboStation)
        self.frmComboFreq = QComboBox(self.centralwidget)
        self.frmLayout.addRow("Station Frequency:", self.frmComboFreq)
        self.frmComboMode = QComboBox(self.centralwidget)
        self.frmLayout.addRow("Modulation Mode:", self.frmComboMode)
        self.frmComboBandwidth = QComboBox(self.centralwidget)
        self.frmLayout.addRow("Bandwidth:", self.frmComboBandwidth)
        self.frmComboModem = QComboBox(self.centralwidget)
        self.frmLayout.addRow("Modem:", self.frmComboModem)
        self.frmComboCenterFreq = QComboBox(self.centralwidget)
        self.frmLayout.addRow("Center Frequency:", self.frmComboCenterFreq)
        #Day of Week = DOW
        self.frmComboDOW = QComboBox(self.centralwidget)
        self.frmLayout.addRow("UTC Day of Week:", self.frmComboDOW)
        
        self.frmUTCTimeEdit = QTimeEdit(self.centralwidget)
        self.frmLayout.addRow("UTC Time:", self.frmUTCTimeEdit)
        self.frmUTCTimeEdit.setDisplayFormat('hh:mm')
        utctime = QTime.fromString('00:00', 'hh:mm')
        self.frmUTCTimeEdit.setTime(utctime)

        self.frmCheckBoxActive = QCheckBox(self.centralwidget)
        self.frmCheckBoxActive.setChecked(True)
        self.frmLayout.addRow("Active:", self.frmCheckBoxActive)
        self.frmTextEditNotes = QTextEdit(self.centralwidget)
        self.frmLayout.addRow("Notes:", self.frmTextEditNotes)

def main():
    """Main function."""
    fcm = QApplication(sys.argv)
    view = FCMUi()
    view.resize(1300, 1000)
    view.show()
    sys.exit(fcm.exec())

if __name__ == '__main__':
    main()
