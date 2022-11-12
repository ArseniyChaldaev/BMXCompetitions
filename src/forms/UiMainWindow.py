# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'gui/main_window.ui'
#
# Created by: PyQt5 UI code generator 5.15.7
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(800, 600)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Maximum, QtWidgets.QSizePolicy.Maximum)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(MainWindow.sizePolicy().hasHeightForWidth())
        MainWindow.setSizePolicy(sizePolicy)
        MainWindow.setLayoutDirection(QtCore.Qt.LeftToRight)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.horizontalLayout = QtWidgets.QHBoxLayout(self.centralwidget)
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.verticalLayout = QtWidgets.QVBoxLayout()
        self.verticalLayout.setObjectName("verticalLayout")
        self.tabWidget = QtWidgets.QTabWidget(self.centralwidget)
        self.tabWidget.setObjectName("tabWidget")
        self.tab = QtWidgets.QWidget()
        self.tab.setObjectName("tab")
        self.horizontalLayout_3 = QtWidgets.QHBoxLayout(self.tab)
        self.horizontalLayout_3.setObjectName("horizontalLayout_3")
        self.verticalLayout_2 = QtWidgets.QVBoxLayout()
        self.verticalLayout_2.setObjectName("verticalLayout_2")
        self.horizontalLayout_2 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")
        spacerItem = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout_2.addItem(spacerItem)
        self.label = QtWidgets.QLabel(self.tab)
        self.label.setObjectName("label")
        self.horizontalLayout_2.addWidget(self.label)
        self.genderComboBox = QtWidgets.QComboBox(self.tab)
        self.genderComboBox.setObjectName("genderComboBox")
        self.horizontalLayout_2.addWidget(self.genderComboBox)
        self.label_2 = QtWidgets.QLabel(self.tab)
        self.label_2.setObjectName("label_2")
        self.horizontalLayout_2.addWidget(self.label_2)
        self.categoryComboBox = QtWidgets.QComboBox(self.tab)
        self.categoryComboBox.setObjectName("categoryComboBox")
        self.horizontalLayout_2.addWidget(self.categoryComboBox)
        self.addSportsmanButton = QtWidgets.QPushButton(self.tab)
        self.addSportsmanButton.setObjectName("addSportsmanButton")
        self.horizontalLayout_2.addWidget(self.addSportsmanButton)
        self.editSportsmanButton = QtWidgets.QPushButton(self.tab)
        self.editSportsmanButton.setObjectName("editSportsmanButton")
        self.horizontalLayout_2.addWidget(self.editSportsmanButton)
        self.deleteSportsmanButton = QtWidgets.QPushButton(self.tab)
        self.deleteSportsmanButton.setObjectName("deleteSportsmanButton")
        self.horizontalLayout_2.addWidget(self.deleteSportsmanButton)
        self.verticalLayout_2.addLayout(self.horizontalLayout_2)
        self.spotrsmenTable = QtWidgets.QTableWidget(self.tab)
        self.spotrsmenTable.setMaximumSize(QtCore.QSize(16777215, 16777215))
        self.spotrsmenTable.setObjectName("spotrsmenTable")
        self.spotrsmenTable.setColumnCount(0)
        self.spotrsmenTable.setRowCount(0)
        self.verticalLayout_2.addWidget(self.spotrsmenTable)
        self.horizontalLayout_3.addLayout(self.verticalLayout_2)
        self.tabWidget.addTab(self.tab, "")
        self.tab_2 = QtWidgets.QWidget()
        self.tab_2.setObjectName("tab_2")
        self.horizontalLayout_5 = QtWidgets.QHBoxLayout(self.tab_2)
        self.horizontalLayout_5.setObjectName("horizontalLayout_5")
        self.verticalLayout_3 = QtWidgets.QVBoxLayout()
        self.verticalLayout_3.setObjectName("verticalLayout_3")
        self.horizontalLayout_4 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_4.setObjectName("horizontalLayout_4")
        spacerItem1 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout_4.addItem(spacerItem1)
        self.label_3 = QtWidgets.QLabel(self.tab_2)
        self.label_3.setObjectName("label_3")
        self.horizontalLayout_4.addWidget(self.label_3)
        self.compCategoryComboBox = QtWidgets.QComboBox(self.tab_2)
        self.compCategoryComboBox.setObjectName("compCategoryComboBox")
        self.horizontalLayout_4.addWidget(self.compCategoryComboBox)
        self.label_5 = QtWidgets.QLabel(self.tab_2)
        self.label_5.setObjectName("label_5")
        self.horizontalLayout_4.addWidget(self.label_5)
        self.cityComboBox = QtWidgets.QComboBox(self.tab_2)
        self.cityComboBox.setObjectName("cityComboBox")
        self.horizontalLayout_4.addWidget(self.cityComboBox)
        self.label_4 = QtWidgets.QLabel(self.tab_2)
        self.label_4.setObjectName("label_4")
        self.horizontalLayout_4.addWidget(self.label_4)
        self.yearComboBox = QtWidgets.QComboBox(self.tab_2)
        self.yearComboBox.setObjectName("yearComboBox")
        self.horizontalLayout_4.addWidget(self.yearComboBox)
        self.startEventButton = QtWidgets.QPushButton(self.tab_2)
        self.startEventButton.setObjectName("startEventButton")
        self.horizontalLayout_4.addWidget(self.startEventButton)
        self.addCompetitionButton = QtWidgets.QPushButton(self.tab_2)
        self.addCompetitionButton.setObjectName("addCompetitionButton")
        self.horizontalLayout_4.addWidget(self.addCompetitionButton)
        self.editCompetitionButton = QtWidgets.QPushButton(self.tab_2)
        self.editCompetitionButton.setObjectName("editCompetitionButton")
        self.horizontalLayout_4.addWidget(self.editCompetitionButton)
        self.deleteCompetitionButton = QtWidgets.QPushButton(self.tab_2)
        self.deleteCompetitionButton.setObjectName("deleteCompetitionButton")
        self.horizontalLayout_4.addWidget(self.deleteCompetitionButton)
        self.verticalLayout_3.addLayout(self.horizontalLayout_4)
        self.competitionTable = QtWidgets.QTableWidget(self.tab_2)
        self.competitionTable.setObjectName("competitionTable")
        self.competitionTable.setColumnCount(0)
        self.competitionTable.setRowCount(0)
        self.verticalLayout_3.addWidget(self.competitionTable)
        self.horizontalLayout_5.addLayout(self.verticalLayout_3)
        self.tabWidget.addTab(self.tab_2, "")
        self.tab_3 = QtWidgets.QWidget()
        self.tab_3.setObjectName("tab_3")
        self.horizontalLayout_7 = QtWidgets.QHBoxLayout(self.tab_3)
        self.horizontalLayout_7.setObjectName("horizontalLayout_7")
        self.verticalLayout_4 = QtWidgets.QVBoxLayout()
        self.verticalLayout_4.setObjectName("verticalLayout_4")
        self.horizontalLayout_6 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_6.setObjectName("horizontalLayout_6")
        spacerItem2 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout_6.addItem(spacerItem2)
        self.label_6 = QtWidgets.QLabel(self.tab_3)
        self.label_6.setObjectName("label_6")
        self.horizontalLayout_6.addWidget(self.label_6)
        self.resultYearComboBox = QtWidgets.QComboBox(self.tab_3)
        self.resultYearComboBox.setObjectName("resultYearComboBox")
        self.horizontalLayout_6.addWidget(self.resultYearComboBox)
        self.label_7 = QtWidgets.QLabel(self.tab_3)
        self.label_7.setObjectName("label_7")
        self.horizontalLayout_6.addWidget(self.label_7)
        self.resultCategoryComboBox = QtWidgets.QComboBox(self.tab_3)
        self.resultCategoryComboBox.setObjectName("resultCategoryComboBox")
        self.horizontalLayout_6.addWidget(self.resultCategoryComboBox)
        self.printResultButton = QtWidgets.QPushButton(self.tab_3)
        self.printResultButton.setObjectName("printResultButton")
        self.horizontalLayout_6.addWidget(self.printResultButton)
        self.saveResultButton = QtWidgets.QPushButton(self.tab_3)
        self.saveResultButton.setObjectName("saveResultButton")
        self.horizontalLayout_6.addWidget(self.saveResultButton)
        self.verticalLayout_4.addLayout(self.horizontalLayout_6)
        self.resultTable = QtWidgets.QTableWidget(self.tab_3)
        self.resultTable.setObjectName("resultTable")
        self.resultTable.setColumnCount(0)
        self.resultTable.setRowCount(0)
        self.verticalLayout_4.addWidget(self.resultTable)
        self.horizontalLayout_7.addLayout(self.verticalLayout_4)
        self.tabWidget.addTab(self.tab_3, "")
        self.verticalLayout.addWidget(self.tabWidget)
        self.horizontalLayout.addLayout(self.verticalLayout)
        MainWindow.setCentralWidget(self.centralwidget)

        self.retranslateUi(MainWindow)
        self.tabWidget.setCurrentIndex(0)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "Система учета спортсменов и результатов соревнований по велоспорту BMX"))
        self.label.setText(_translate("MainWindow", "Пол"))
        self.label_2.setText(_translate("MainWindow", "Категория"))
        self.addSportsmanButton.setText(_translate("MainWindow", "Добавить"))
        self.editSportsmanButton.setText(_translate("MainWindow", "Редактировать"))
        self.deleteSportsmanButton.setText(_translate("MainWindow", "Удалить"))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab), _translate("MainWindow", "Список спортсменов"))
        self.label_3.setText(_translate("MainWindow", "Категория"))
        self.label_5.setText(_translate("MainWindow", "Город"))
        self.label_4.setText(_translate("MainWindow", "Год"))
        self.startEventButton.setText(_translate("MainWindow", "Начать соревнование"))
        self.addCompetitionButton.setText(_translate("MainWindow", "Добавить"))
        self.editCompetitionButton.setText(_translate("MainWindow", "Редактировать"))
        self.deleteCompetitionButton.setText(_translate("MainWindow", "Удалить"))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab_2), _translate("MainWindow", "Список соревнований"))
        self.label_6.setText(_translate("MainWindow", "Год"))
        self.label_7.setText(_translate("MainWindow", "Категория"))
        self.printResultButton.setText(_translate("MainWindow", "Печать"))
        self.saveResultButton.setText(_translate("MainWindow", "Сохранить"))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab_3), _translate("MainWindow", "Рейтинг спортсменов "))


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(MainWindow)
    MainWindow.show()
    sys.exit(app.exec_())