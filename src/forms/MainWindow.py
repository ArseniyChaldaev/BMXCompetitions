import csv
from datetime import datetime

from PyQt5 import QtPrintSupport, QtWidgets, QtGui
from PyQt5.QtGui import QImage, QPixmap
from PyQt5.QtWidgets import QMainWindow, QTableWidgetItem, QAbstractItemView, QLabel, QHeaderView, QMessageBox
from PyQt5.QtWidgets import QFileDialog

import utils.DbHelper as DbHelper
from GlobalVars import DEFAULT_IMAGE_PATH
from forms.CompetitionDialog import CompetitionDialog
from forms.CompetitionEventDialog import CompetitionEventDialog
from forms.SportsmanDialog import SportsmanDialog
from forms.UiMainWindow import Ui_MainWindow
from models.Competition import getCompetitions, deleteCompetition, getCompetitionTypes, getCities
from models.Event import getAllResults
from models.Sportsman import getSportsmen, deleteSportsmen


class MainWindow(QMainWindow):
    def __init__(self):
        super(MainWindow, self).__init__()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)

        # Sportsmen's tab
        self.sportsmen = None
        self.categories = DbHelper.get_all_from_db("SELECT id, title, min_age, max_age FROM categories")

        self.initSportsmenTab()
        self.initSportsmenTabEvents()

        # Competition's tab
        self.competitions = None
        self.competitionTypes = getCompetitionTypes()

        self.initCompetitionsTab()
        self.initCompetitionsTabEvents()

        # Result's tab
        self.initResultsTab()
        self.initResultsTabEvents()

        self.ui.tabWidget.currentChanged.connect(self.tabChanged)

    def initSportsmenTab(self):
        self.initSportsmenFilters()

        self.ui.spotrsmenTable.setColumnCount(6)
        self.ui.spotrsmenTable.setHorizontalHeaderLabels(['Фото', 'Фамилия Имя', 'Пол', 'День Рождения', 'Очки', 'Id'])
        self.ui.spotrsmenTable.setEditTriggers(QAbstractItemView.NoEditTriggers)
        self.ui.spotrsmenTable.setSelectionBehavior(QAbstractItemView.SelectRows)
        self.ui.spotrsmenTable.setSortingEnabled(True)
        self.ui.spotrsmenTable.hideColumn(5)
        self.ui.spotrsmenTable.verticalHeader().setVisible(False)

        self.loadSportsmenData()

    def initSportsmenTabEvents(self):
        self.ui.deleteSportsmanButton.clicked.connect(self.deleteSportsman)
        self.ui.editSportsmanButton.clicked.connect(self.editSportsman)
        self.ui.addSportsmanButton.clicked.connect(self.openSportsmanDialog)
        self.ui.genderComboBox.currentIndexChanged.connect(self.loadSportsmenData)
        self.ui.categoryComboBox.currentIndexChanged.connect(self.loadSportsmenData)

    def initSportsmenFilters(self):
        self.ui.genderComboBox.addItems(['Все', 'Девушки', 'Юноши'])
        self.ui.categoryComboBox.addItem('Все')
        for row in self.categories:
            self.ui.categoryComboBox.addItem(row[1], userData=row)

    def editSportsman(self):
        row_id = self.ui.spotrsmenTable.currentIndex().row()
        if row_id > -1:
            sportsman_id = self.ui.spotrsmenTable.item(row_id, 5).text()
            self.openSportsmanDialog(sportsman_id)
        else:
            QMessageBox.question(self, 'Сообщение', 'Пожалуйста выберите спортсмена, которого хотите отредактировать.',
                                 QMessageBox.Ok)

    def deleteSportsman(self):
        row_id = self.ui.spotrsmenTable.currentIndex().row()
        if row_id > -1:
            sportsman_id = self.ui.spotrsmenTable.item(row_id, 5).text()
            reply = QMessageBox.question(self, 'Внимание', 'Вы уверены, что хотите удалить спортсмена?',
                                         QMessageBox.Yes | QMessageBox.No)
            if reply == QMessageBox.No:
                return
            deleteSportsmen(sportsman_id)
            self.loadSportsmenData()
        else:
            QMessageBox.question(self, 'Сообщение', 'Пожалуйста выберите спортсмена, которого хотите удалить.',
                                 QMessageBox.Ok)

    def openSportsmanDialog(self, sportsman_id=None):
        dlg = SportsmanDialog(self, sportsman_id)
        dlg.exec()
        self.loadSportsmenData()

    def loadSportsmenData(self):
        gender, category_ages = None, None
        if self.ui.genderComboBox.currentIndex() > 0:
            gender = self.ui.genderComboBox.currentIndex() - 1
        if self.ui.categoryComboBox.currentIndex() > 0:
            category = self.ui.categoryComboBox.currentData()
            category_ages = (category[2], category[3])
        self.sportsmen = getSportsmen(gender, category_ages)

        self.ui.spotrsmenTable.setRowCount(len(self.sportsmen))
        for i, sportsman in enumerate(self.sportsmen):
            self.ui.spotrsmenTable.setCellWidget(i, 0, self.getImageLabel(sportsman.photo))
            self.ui.spotrsmenTable.setItem(i, 1, QTableWidgetItem(' '.join([sportsman.surname, sportsman.name])))
            self.ui.spotrsmenTable.setItem(i, 2, QTableWidgetItem('Юноша' if sportsman.gender else 'Девушка'))
            self.ui.spotrsmenTable.setItem(i, 3, QTableWidgetItem(sportsman.birthday))
            self.ui.spotrsmenTable.setItem(i, 4, QTableWidgetItem(str(sportsman.score)))
            self.ui.spotrsmenTable.setItem(i, 5, QTableWidgetItem(str(sportsman.unique_id)))

        self.ui.spotrsmenTable.resizeColumnsToContents()
        self.ui.spotrsmenTable.resizeRowsToContents()
        header = self.ui.spotrsmenTable.horizontalHeader()
        header.setSectionResizeMode(1, QHeaderView.Stretch)

    def getImageLabel(self, image_data):
        if image_data:
            img = QImage.fromData(image_data)
            pixmap = QPixmap.fromImage(img)
        else:
            pixmap = QPixmap(DEFAULT_IMAGE_PATH)

        imageLabel = QLabel(self)
        imageLabel.setText('')
        imageLabel.setFixedSize(100, 100)
        imageLabel.setScaledContents(True)
        imageLabel.setPixmap(pixmap)
        return imageLabel

    def initCompetitionsTab(self):
        self.initCompetitionsFilters()

        self.ui.competitionTable.setColumnCount(5)
        self.ui.competitionTable.setHorizontalHeaderLabels(['Название', 'Город', 'Дата', 'Категория', 'Id'])
        self.ui.competitionTable.setEditTriggers(QAbstractItemView.NoEditTriggers)
        self.ui.competitionTable.setSelectionBehavior(QAbstractItemView.SelectRows)
        self.ui.competitionTable.setSortingEnabled(True)
        self.ui.competitionTable.hideColumn(4)
        self.ui.competitionTable.verticalHeader().setVisible(False)

        self.loadCompetitionsData()

    def initCompetitionsFilters(self):
        self.ui.compCategoryComboBox.addItem('Все')
        for type_id, title in self.competitionTypes:
            self.ui.compCategoryComboBox.addItem(title, userData=type_id)

        self.ui.cityComboBox.addItem('Все')
        for city, in getCities():
            self.ui.cityComboBox.addItem(str(city), userData=city)

        self.ui.yearComboBox.addItem('Все')
        current_year = datetime.now().year
        for year in range(current_year, current_year - 5, -1):
            self.ui.yearComboBox.addItem(str(year), userData=year)

    def loadCompetitionsData(self):
        type_id, city, year = None, None, None
        if self.ui.compCategoryComboBox.currentIndex() > 0:
            type_id = self.ui.compCategoryComboBox.currentData()
        if self.ui.cityComboBox.currentIndex() > 0:
            city = self.ui.cityComboBox.currentData()
        if self.ui.yearComboBox.currentIndex() > 0:
            year = self.ui.yearComboBox.currentData()

        self.competitions = getCompetitions(type_id, city, year)

        self.ui.competitionTable.setRowCount(len(self.competitions))
        for i, competition in enumerate(self.competitions):
            self.ui.competitionTable.setItem(i, 0, QTableWidgetItem(competition.title))
            self.ui.competitionTable.setItem(i, 1, QTableWidgetItem(competition.city))
            self.ui.competitionTable.setItem(i, 2, QTableWidgetItem(competition.date))
            for type_id, title in self.competitionTypes:
                if type_id == competition.type_id:
                    self.ui.competitionTable.setItem(i, 3, QTableWidgetItem(title))
                    break
            self.ui.competitionTable.setItem(i, 4, QTableWidgetItem(str(competition.unique_id)))

        self.ui.competitionTable.resizeColumnsToContents()
        self.ui.competitionTable.resizeRowsToContents()
        header = self.ui.competitionTable.horizontalHeader()
        header.setSectionResizeMode(0, QHeaderView.Stretch)

    def initCompetitionsTabEvents(self):
        self.ui.deleteCompetitionButton.clicked.connect(self.deleteCompetition)
        self.ui.editCompetitionButton.clicked.connect(self.editCompetition)
        self.ui.addCompetitionButton.clicked.connect(self.openCompetitionDialog)
        self.ui.startEventButton.clicked.connect(self.openEventDialog)
        self.ui.compCategoryComboBox.currentIndexChanged.connect(self.loadCompetitionsData)
        self.ui.cityComboBox.currentIndexChanged.connect(self.loadCompetitionsData)
        self.ui.yearComboBox.currentIndexChanged.connect(self.loadCompetitionsData)

    def openEventDialog(self):
        row_id = self.ui.competitionTable.currentIndex().row()
        if row_id > -1:
            competition_id = self.ui.competitionTable.item(row_id, 4).text()
            dlg = CompetitionEventDialog(self, competition_id)
            dlg.exec()
            self.loadCompetitionsData()
        else:
            QMessageBox.question(self, 'Сообщение', 'Пожалуйста выберите соревнование, которого хотите начать.',
                                 QMessageBox.Ok)

    def openCompetitionDialog(self, competition_id=None):
        dlg = CompetitionDialog(self, competition_id)
        dlg.exec()
        self.loadCompetitionsData()

    def editCompetition(self):

        row_id = self.ui.competitionTable.currentIndex().row()
        if row_id > -1:
            competition_id = self.ui.competitionTable.item(row_id, 4).text()
            self.openCompetitionDialog(competition_id)
        else:
            QMessageBox.question(self, 'Сообщение',
                                 'Пожалуйста выберите соревнование, которого хотите отредактировать.',
                                 QMessageBox.Ok)

    def deleteCompetition(self):
        try:
            row_id = self.ui.competitionTable.currentIndex().row()
            if row_id > -1:
                competition_id = self.ui.competitionTable.item(row_id, 4).text()
                reply = QMessageBox.question(self, 'Внимание', 'Вы уверены, что хотите удалить соревнование?',
                                             QMessageBox.Yes | QMessageBox.No)
                if reply == QMessageBox.No:
                    return
                deleteCompetition(competition_id)
                self.loadCompetitionsData()
            else:
                QMessageBox.question(self, 'Сообщение', 'Пожалуйста выберите соревнование, которого хотите удалить.',
                                     QMessageBox.Ok)
        except Exception as ex:
            print(ex)

    def initResultsTab(self):
        for row in self.categories:
            for gender_id, gender_title in [(1, 'Юноши'), (0, 'Девушки')]:
                self.ui.resultCategoryComboBox.addItem(f'{gender_title} {row[1]}', userData=(gender_id, row[0]))
        current_year = datetime.now().year
        for year in range(current_year, current_year - 5, -1):
            self.ui.resultYearComboBox.addItem(str(year), userData=year)

        self.loadResultsData()

    def initResultsTabEvents(self):
        self.ui.printResultButton.clicked.connect(self.printResults)
        self.ui.saveResultButton.clicked.connect(self.saveResults)
        self.ui.resultCategoryComboBox.currentIndexChanged.connect(self.loadResultsData)
        self.ui.resultYearComboBox.currentIndexChanged.connect(self.loadResultsData)

    def loadResultsData(self):
        gender, category_id = self.ui.resultCategoryComboBox.currentData()
        year = self.ui.resultYearComboBox.currentData()
        data, header = getAllResults(year, gender, category_id)

        self.ui.resultTable.setColumnCount(len(header))
        self.ui.resultTable.setHorizontalHeaderLabels(header)
        self.ui.resultTable.setEditTriggers(QAbstractItemView.NoEditTriggers)
        self.ui.resultTable.setSortingEnabled(True)

        self.ui.resultTable.setRowCount(len(data))
        for i in range(len(data)):
            for j in range(len(data[i])):
                self.ui.resultTable.setItem(i, j, QTableWidgetItem(str(data[i][j])))

        self.ui.resultTable.resizeColumnsToContents()
        self.ui.resultTable.resizeRowsToContents()
        header = self.ui.resultTable.horizontalHeader()
        header.setSectionResizeMode(0, QHeaderView.Stretch)

    def printResults(self):
        dialog = QtPrintSupport.QPrintDialog()
        if dialog.exec_() == QtWidgets.QDialog.Accepted:
            self.handlePaintRequest(dialog.printer())

    def handlePaintRequest(self, printer):
        document = QtGui.QTextDocument()
        cursor = QtGui.QTextCursor(document)
        year = self.ui.resultYearComboBox.currentData()
        cursor.insertText(f"Результаты за {year}. Категория: {self.ui.resultCategoryComboBox.currentText()} \r\n")
        table = cursor.insertTable(self.ui.resultTable.rowCount() + 1, self.ui.resultTable.columnCount())
        fmt = table.format()
        fmt.setWidth(QtGui.QTextLength(QtGui.QTextLength.PercentageLength, 100))
        table.setFormat(fmt)

        for col in range(table.columns()):
            cursor.insertText(self.ui.resultTable.horizontalHeaderItem(col).text())
            cursor.movePosition(QtGui.QTextCursor.NextCell)

        for row in range(table.rows() - 1):
            for col in range(table.columns()):
                cursor.insertText(self.ui.resultTable.item(row, col).text())
                cursor.movePosition(QtGui.QTextCursor.NextCell)
        document.print_(printer)

    def saveResults(self):
        path, _ = QFileDialog.getSaveFileName(self, 'Save File', self.ui.resultCategoryComboBox.currentText(),
                                              'CSV(*.csv)')
        if not path:
            return
        with open(path, 'w', encoding='utf8', newline='') as f:
            writer = csv.writer(f)
            row_count, col_count = self.ui.resultTable.rowCount(), self.ui.resultTable.columnCount()

            rowdata = []
            for col in range(col_count):
                rowdata.append(self.ui.resultTable.horizontalHeaderItem(col).text())
            writer.writerow(rowdata)

            for row in range(row_count):
                rowdata = []
                for col in range(col_count):
                    rowdata.append(self.ui.resultTable.item(row, col).text())
                writer.writerow(rowdata)

    def tabChanged(self):
        idx = self.ui.tabWidget.currentIndex()
        if idx == 0:
            self.loadSportsmenData()
        elif idx == 1:
            self.loadCompetitionsData()
        elif idx == 2:
            self.loadResultsData()