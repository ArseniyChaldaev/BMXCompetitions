from PyQt5.QtCore import QDate
from PyQt5.QtGui import QPixmap, QImage
from PyQt5.QtWidgets import QDialog, QFileDialog, QDialogButtonBox

from forms.UiSportsmanDialog import Ui_SportsmanDialog
from models.Sportsman import getSportsmanById


class SportsmanDialog(QDialog):
    def __init__(self, parent=None, sportsman_id=None):
        super(SportsmanDialog, self).__init__(parent)
        self.sportsman_id = sportsman_id
        self.ui = Ui_SportsmanDialog()
        self.ui.setupUi(self)
        self.initEvents()

        self.sportsman = getSportsmanById(self.sportsman_id)
        self.initUi()

    def initEvents(self):
        self.ui.changePhotoButton.clicked.connect(self.changePhoto)
        saveButton = self.ui.buttonBox.button(QDialogButtonBox.Save)
        saveButton.clicked.connect(self.save)
        saveButton.setText('Сохранить')
        cancelButton = self.ui.buttonBox.button(QDialogButtonBox.Cancel)
        cancelButton.clicked.connect(self.close)
        cancelButton.setText('Отмена')

    def initUi(self):
        try:
            self.ui.nameEdit.setText(self.sportsman.name)
            self.ui.surnameEdit.setText(self.sportsman.surname)
            if self.sportsman.gender == 1:
                self.ui.maleRadioButton.setChecked(True)
            else:
                self.ui.femaleRadioButton.setChecked(True)
            self.ui.dateEdit.setDate(QDate.fromString(self.sportsman.birthday, "dd.MM.yyyy"))
            self.setProfileImage()
            if self.sportsman_id:
                self.setWindowTitle(' '.join([self.sportsman.surname, self.sportsman.name]))
        except Exception as ex:
            print(ex)

    def setProfileImage(self):
        image = QImage.fromData(self.sportsman.photo)
        self.ui.photoLabel.setPixmap(QPixmap.fromImage(image))

    def changePhoto(self):
        filename, _ = QFileDialog.getOpenFileName(self, 'Выберите картинку', filter='Image files (*.jpg, *.gif, *.png)')
        if filename:
            self.sportsman.setPhoto(filename)
            self.setProfileImage()

    def save(self):
        self.sportsman.unique_id = self.sportsman_id
        self.sportsman.name = self.ui.nameEdit.text()
        self.sportsman.surname = self.ui.surnameEdit.text()
        self.sportsman.birthday = self.ui.dateEdit.text()
        self.sportsman.gender = int(self.ui.maleRadioButton.isChecked())
        self.sportsman.year = self.ui.dateEdit.date().year()
        self.sportsman.save()
        self.close()
