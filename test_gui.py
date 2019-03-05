import sys
from PyQt5 import uic
from PyQt5.QtWidgets import QMainWindow, QApplication


class CsvEditor(QMainWindow):
    def __init__(self):
        super(CsvEditor, self).__init__()
        uic.loadUi('mainwindow.ui', self)

        self.csv_table_tab = self.main_document_tab
        self.start_page_tab = self.start_tab
        self.tabWidget.removeTab(1)

        # Load the Start Page tab on application start
        self.tabWidget.setCurrentIndex(0)

        self.btn_load_csv.clicked.connect(self.load_csv)

        self.show()

    def load_csv(self):
        print("loading csv")
        # Close the start page tab and load the file tab
        self.tabWidget.removeTab(0)
        self.tabWidget.insertTab(1, self.csv_table_tab, "Main Document")


if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = CsvEditor()
    sys.exit(app.exec_())
