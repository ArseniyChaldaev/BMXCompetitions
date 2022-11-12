import sys
import traceback

from PyQt5.QtWidgets import QApplication, QMessageBox

from forms.MainWindow import MainWindow
from utils import DbHelper


def my_excepthook(type, value, trace):
    traceback_formated = traceback.format_exception(type, value, trace)
    traceback_string = ''.join(traceback_formated)
    QMessageBox.question(None, 'Ошибка', traceback_string, QMessageBox.Ok)


if __name__ == '__main__':
    sys.excepthook = my_excepthook
    DbHelper.init_database()
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())
