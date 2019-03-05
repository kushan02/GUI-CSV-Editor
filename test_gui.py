import sys
from PyQt5 import uic
from PyQt5.QtWidgets import QMainWindow, QApplication, QFileDialog, QTableWidget, QTableWidgetItem
import csv


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

        # Flag for not detecting cell state change when opening the file
        self.check_cell_change = True
        # Connect cell change function
        self.csv_data_table.cellChanged.connect(self.cell_change_current)

        self.show()

    def load_csv(self):
        # Disable cell change check to avoid crashes
        self.check_cell_change = False

        csv_file_path = QFileDialog.getOpenFileName(self, "Load CSV File", "", 'CSV(*.csv)')

        # Proceed if and only if a valid file is selected and the file dialog is not cancelled
        if csv_file_path[0]:
            with open(csv_file_path[0], newline='') as csv_file:

                self.csv_data_table.setRowCount(0)
                self.csv_data_table.setColumnCount(0)

                csv_file_read = csv.reader(csv_file, delimiter=',', quotechar='|')

                # Fetch the column headers and move the iterator to actual data
                column_headers = next(csv_file_read)

                for row_data in csv_file_read:
                    row = self.csv_data_table.rowCount()
                    self.csv_data_table.insertRow(row)
                    self.csv_data_table.setColumnCount(len(row_data))
                    for column, stuff in enumerate(row_data):
                        item = QTableWidgetItem(stuff)
                        self.csv_data_table.setItem(row, column, item)

                self.csv_data_table.setHorizontalHeaderLabels(column_headers)

            # Set WordWrap to True to make the cells change height according to content
            # Currently set it to false as it looks very decent and makes cell size uniform throughout
            self.csv_data_table.setWordWrap(False)
            # Uncomment below line to stretch to fill the column width according to content
            # self.csv_data_table.resizeColumnsToContents()
            self.csv_data_table.resizeRowsToContents()

            self.check_cell_change = True

            # Close the start page tab and load the file tab
            self.tabWidget.removeTab(0)
            self.tabWidget.insertTab(1, self.csv_table_tab, "Main Document")

    def cell_change_current(self):
        if self.check_cell_change:
            row = self.csv_data_table.currentRow()
            col = self.csv_data_table.currentColumn()
            value = self.csv_data_table.item(row, col).text()
            print("The current cell is ", row, ", ", col)
            print("In this cell we have: ", value)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = CsvEditor()
    sys.exit(app.exec_())
