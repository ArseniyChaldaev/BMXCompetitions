from PyQt5.QtCore import QDate
from PyQt5.QtWidgets import QDialog, QDialogButtonBox

from forms.UiCompetitionDialog import Ui_CompetitionDialog
from models.Competition import getCompetitionById, getCompetitionTypes


class CompetitionDialog(QDialog):
    def __init__(self, parent=None, competition_id=None):
        super(CompetitionDialog, self).__init__(parent)
        self.competition_id = competition_id
        self.ui = Ui_CompetitionDialog()
        self.ui.setupUi(self)
        self.initEvents()

        self.competition = getCompetitionById(self.competition_id)
        self.initUi()

    def initEvents(self):
        saveButton = self.ui.buttonBox.button(QDialogButtonBox.Save)
        saveButton.setText('Сохранить')
        saveButton.clicked.connect(self.save)
        cancelButton = self.ui.buttonBox.button(QDialogButtonBox.Cancel)
        cancelButton.setText('Отмена')
        cancelButton.clicked.connect(self.close)

    def initUi(self):
        try:
            for type_id, title in getCompetitionTypes():
                self.ui.categoryComboBox.addItem(title, userData=type_id)

            self.ui.nameEdit.setText(self.competition.title)
            self.ui.cityEdit.setText(self.competition.city)
            index = self.ui.categoryComboBox.findData(self.competition.type_id)
            self.ui.categoryComboBox.setCurrentIndex(index)
            self.ui.dateEdit.setDate(QDate.fromString(self.competition.date, "dd.MM.yyyy"))
            if self.competition_id:
                self.setWindowTitle(self.competition.title)
        except Exception as ex:
            print(ex)

    def save(self):
        self.competition.unique_id = self.competition_id
        self.competition.title = self.ui.nameEdit.text()
        self.competition.city = self.ui.cityEdit.text()
        self.competition.date = self.ui.dateEdit.text()
        self.competition.type_id = self.ui.categoryComboBox.currentData()
        self.competition.save()
        self.close()
