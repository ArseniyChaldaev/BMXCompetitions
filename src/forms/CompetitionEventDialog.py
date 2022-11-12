import csv

from PyQt5 import QtCore, QtPrintSupport, QtGui
from PyQt5.QtCore import QAbstractTableModel, Qt, QVariant
from PyQt5.QtWidgets import QDialog, QMessageBox, QHeaderView, QFileDialog

from forms.UiCompetitionEventDialog import Ui_CompetitionEventDialog
from models.Competition import getCompetitionById
from utils import DbHelper
from utils.RaceHelper import Race


class CompetitionEventDialog(QDialog):
    def __init__(self, parent=None, competition_id=None):
        super(CompetitionEventDialog, self).__init__(parent)
        self.competition_id = competition_id
        self.ui = Ui_CompetitionEventDialog()
        self.ui.setupUi(self)

        self.buttons = [self.ui.moto1Button, self.ui.moto2Button, self.ui.moto3Button,
                        self.ui.quaterButton, self.ui.halfButton, self.ui.finalButton]

        self.comboBoxes = [self.ui.moto1ComboBox, self.ui.moto2ComboBox, self.ui.moto3ComboBox,
                           self.ui.quaterComboBox, self.ui.halfComboBox, self.ui.finalComboBox]

        self.competition = getCompetitionById(self.competition_id)
        self.raceTypeNumber = 0
        self.race = Race(self.competition_id)

        self.initUi()
        self.initEvents()

    def initEvents(self):
        self.ui.categoryComboBox.currentIndexChanged.connect(self.initUiForCategory)
        for btn in self.buttons:
            btn.setEnabled(False)
            btn.clicked.connect(self.raceButtonClick)
        self.ui.saveButton.clicked.connect(self.saveRace)
        self.ui.generateButton.clicked.connect(self.generateRaces)
        self.ui.resultButton.clicked.connect(self.showResult)
        self.ui.saveFileButton.clicked.connect(self.saveToFile)
        self.ui.printButton.clicked.connect(self.printRace)

    def raceButtonClick(self):
        for i, btn in enumerate(self.buttons):
            if self.sender() == btn:
                self.raceTypeNumber = i + 1
                self.comboBoxes[i].setEnabled(True)
                btn.setChecked(True)
            else:
                self.comboBoxes[i].setEnabled(False)
                btn.setChecked(False)
        self.showRace()

    def initUi(self):
        self.disableRaceControl()
        categories = DbHelper.get_all_from_db("SELECT id, title, min_age, max_age FROM categories")
        for row in categories:
            for gender_id, gender_title in [(1, 'Юноши'), (0, 'Девушки')]:
                self.ui.categoryComboBox.addItem(f'{gender_title} {row[1]}',
                                                 userData=(gender_id, row[0], row[2], row[3]))

    def initUiForCategory(self):
        self.disableRaceControl()
        gender, category_id, min_age, max_age = self.ui.categoryComboBox.currentData()
        self.race.setGenderAndCategory(gender, category_id)
        if (gender, category_id) not in self.race.startList:
            QMessageBox.information(self, 'Сообщение', 'В этой категории нет спортсменов.', QMessageBox.Ok)
            self.race.results = None
            return

        self.enableRaceControl()
        for race_type in range(1, 7):
            if race_type in self.race.currentData:
                self.buttons[race_type - 1].setEnabled(True)
                for race_number in self.race.currentData[race_type].keys():
                    self.comboBoxes[race_type - 1].addItem(f'Заезд {race_number}', userData=race_number)
                self.comboBoxes[race_type - 1].currentIndexChanged.connect(self.showRace)
        self.buttons[0].click()

    def enableRaceControl(self):
        self.ui.resultButton.setEnabled(len(self.race.results) > 0)
        self.ui.saveButton.setEnabled(len(self.race.results) == 0)
        self.ui.generateButton.setEnabled(len(self.race.results) == 0)
        self.ui.saveFileButton.setEnabled(True)
        self.ui.printButton.setEnabled(True)

    def disableRaceControl(self):
        self.ui.resultButton.setEnabled(False)
        self.ui.saveButton.setEnabled(False)
        self.ui.generateButton.setEnabled(False)
        self.ui.saveFileButton.setEnabled(False)
        self.ui.printButton.setEnabled(False)
        for btn in self.buttons:
            btn.setEnabled(False)
        for box in self.comboBoxes:
            box.clear()
            box.setEnabled(False)

    def showRace(self):
        if self.comboBoxes[self.raceTypeNumber - 1].currentIndex() == -1:
            model = SportsmanModel([[]], self)
            self.ui.tableView.setModel(model)
            return
        race_number = self.comboBoxes[self.raceTypeNumber - 1].currentData()
        model = SportsmanModel(self.race.currentData[self.raceTypeNumber][race_number], self)
        model.dataChanged.connect(self.checkCanSave)
        self.ui.tableView.setModel(model)
        self.ui.tableView.resizeColumnsToContents()
        header = self.ui.tableView.horizontalHeader()
        header.setSectionResizeMode(1, QHeaderView.Stretch)
        self.ui.tableView.hideColumn(0)  # hide sportsmen id
        self.ui.tableView.hideColumn(4)  # hide startlist id

    def checkCanSave(self):
        for item in self.ui.tableView.model().getData():
            if not item[3]:
                return
        reply = QMessageBox.question(self, 'Внимание', 'Сохранить заезд?',
                                     QMessageBox.Yes | QMessageBox.No)
        if reply == QMessageBox.Yes:
            self.saveRace()

    def saveRace(self):
        positions = []
        for item in self.ui.tableView.model().getData():
            if not item[3]:
                QMessageBox.information(self, 'Ошибка', 'Заполните все позиции в заезде', QMessageBox.Ok)
                return
            positions.append((item[3], item[4]))
        self.race.save(positions)
        QMessageBox.information(self, 'Уведомление', 'Данные заезда сохранены', QMessageBox.Ok)
        if self.ui.finalButton.isChecked():
            self.generateResults()

    def generateRaces(self):
        self.saveRace()
        if self.race.results:
            return
        max_race_type = 3
        for race_type in self.race.currentData.keys():
            if race_type > max_race_type:
                max_race_type = race_type
            for values in self.race.currentData[race_type].values():
                for item in values:
                    if not item[3]:
                        QMessageBox.information(self, 'Ошибка', 'Заполните и сохраните все позиции в заезда.',
                                                QMessageBox.Ok)
                        return
        self.race.generateRaces(max_race_type)
        self.initUiForCategory()

    def generateResults(self):
        self.race.generateResults()
        self.ui.resultButton.setEnabled(True)

    def showResult(self):
        if not self.race.results:
            return
        self.buttons[self.raceTypeNumber - 1].setChecked(False)
        self.raceTypeNumber = 0
        model = ResultsModel(self.race.results)
        self.ui.tableView.setModel(model)
        self.ui.tableView.resizeColumnsToContents()
        header = self.ui.tableView.horizontalHeader()
        header.setSectionResizeMode(1, QHeaderView.Stretch)
        self.ui.tableView.hideColumn(0)  # hide sportsmen id

    def saveToFile(self):
        if self.raceTypeNumber:
            filename = f'{self.ui.categoryComboBox.currentText()} {self.buttons[self.raceTypeNumber - 1].text()}'
        else:
            filename = f'{self.ui.categoryComboBox.currentText()} {self.ui.resultButton.text()}'
        path, _ = QFileDialog.getSaveFileName(self, 'Save File', filename, 'CSV(*.csv)')
        if not path:
            return
        with open(path, 'w', encoding='utf8', newline='') as f:
            writer = csv.writer(f)
            model = self.ui.tableView.model()
            row_count = model.rowCount(0)
            if self.raceTypeNumber:
                col_count = model.columnCount(0) - 1
            else:
                col_count = model.columnCount(0)

            rowdata = []
            for col in range(1, col_count):
                rowdata.append(model.getHeader()[col])
            writer.writerow(rowdata)

            for row in range(row_count):
                rowdata = []
                for col in range(1, col_count):
                    item = model.getData()[row][col]
                    if item is None:
                        rowdata.append('')
                    else:
                        rowdata.append(item)

                writer.writerow(rowdata)

    def printRace(self):
        dialog = QtPrintSupport.QPrintDialog()
        if dialog.exec_() == QDialog.Accepted:
            self.handlePaintRequest(dialog.printer())

    def handlePaintRequest(self, printer):
        document = QtGui.QTextDocument()
        cursor = QtGui.QTextCursor(document)

        if self.raceTypeNumber:
            txt = f'{self.ui.categoryComboBox.currentText()} {self.buttons[self.raceTypeNumber - 1].text()}'
        else:
            txt = f'{self.ui.categoryComboBox.currentText()} {self.ui.resultButton.text()}'
        cursor.insertText(txt)

        model = self.ui.tableView.model()
        row_count = model.rowCount(0)
        if self.raceTypeNumber:
            col_count = model.columnCount(0) - 1
        else:
            col_count = model.columnCount(0)

        table = cursor.insertTable(row_count + 1, col_count - 1)
        fmt = table.format()
        fmt.setWidth(QtGui.QTextLength(QtGui.QTextLength.PercentageLength, 100))
        table.setFormat(fmt)

        for col in range(1, col_count):
            cursor.insertText(model.getHeader()[col])
            cursor.movePosition(QtGui.QTextCursor.NextCell)

        for row in range(row_count):
            for col in range(1, col_count):
                item = model.getData()[row][col]
                if item is None:
                    cursor.insertText('')
                else:
                    cursor.insertText(str(item))
                cursor.movePosition(QtGui.QTextCursor.NextCell)
        document.print_(printer)


class SportsmanModel(QAbstractTableModel):
    def __init__(self, data, parent_widget):
        super(SportsmanModel, self).__init__()
        self._data = data
        self._headerData = ['', 'Фамилия Имя', 'Стартовая позиция', 'Позиция на финише', '']
        self._parentWidget = parent_widget

    def data(self, index, role):
        if role == Qt.DisplayRole:
            return self._data[index.row()][index.column()]

    def rowCount(self, index):
        return len(self._data)

    def columnCount(self, index):
        return len(self._data[0])

    def headerData(self, col, orientation, role):
        if orientation == Qt.Horizontal and role == Qt.DisplayRole:
            return QVariant(self._headerData[col])
        return QVariant()

    def setData(self, index, value, role=QtCore.Qt.EditRole):
        if role == QtCore.Qt.EditRole:
            row = index.row()
            column = index.column()
            if self.isValid(row, value):
                self._data[row][column] = value
                self.dataChanged.emit(index, index)
                return True
            return False
        return QtCore.QAbstractTableModel.setData(self, index, value, role)

    def getData(self):
        return self._data

    def getHeader(self):
        return self._headerData

    def flags(self, index):
        original_flags = super(SportsmanModel, self).flags(index)
        if self._parentWidget.race.results:
            return original_flags
        if index.column() == 3:
            return original_flags | QtCore.Qt.ItemIsEditable | QtCore.Qt.ItemIsEnabled | QtCore.Qt.ItemIsSelectable
        else:
            return original_flags

    def isValid(self, row, value):
        if not value.isdigit():
            self.showErrorMessage('Позиция на финише должна быть числом.')
            return False
        num = int(value)
        if num < 1 or num > len(self._data):
            self.showErrorMessage('Позиция на финише должна быть меньше или равна количеству спортсменов и больше 0.')
            return False
        for i, item in enumerate(self._data):
            if item[3]:
                if int(item[3]) == num and i != row:
                    self.showErrorMessage('Позиция на финише должна должна быть уникальной.')
                    return False
        return True

    def showErrorMessage(self, message):
        if self._parentWidget:
            QMessageBox.information(self._parentWidget, 'Ошибка', message, QMessageBox.Ok)


class ResultsModel(QAbstractTableModel):
    def __init__(self, data, parentWidget=None):
        super(ResultsModel, self).__init__()
        self._data = data
        self._headerData = ['id', 'Фамилия Имя', 'Место', 'Очки']
        self._parentWidget = parentWidget

    def data(self, index, role):
        if role == Qt.DisplayRole:
            return self._data[index.row()][index.column()]

    def getData(self):
        return self._data

    def getHeader(self):
        return self._headerData

    def rowCount(self, index):
        return len(self._data)

    def columnCount(self, index):
        return len(self._data[0])

    def headerData(self, col, orientation, role):
        if orientation == Qt.Horizontal and role == Qt.DisplayRole:
            return QVariant(self._headerData[col])
        return QVariant()
