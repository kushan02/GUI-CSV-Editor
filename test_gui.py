import sys
from PyQt5 import uic
from PyQt5.QtWidgets import QMainWindow, QApplication

class CsvEditor(QMainWindow):
    def __init__(self):
        super(CsvEditor, self).__init__()
        uic.loadUi('mainwindow.ui', self)
        self.show()

if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = CsvEditor()
    sys.exit(app.exec_())
