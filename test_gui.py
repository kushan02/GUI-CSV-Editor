import sys
from PyQt5 import uic
from PyQt5.QtWidgets import QMainWindow, QApplication, QFileDialog, QTableWidget, QTableWidgetItem, QDialog
import csv


class ColumnLayoutDialog(QDialog):
    def __init__(self):
        super(ColumnLayoutDialog, self).__init__()
        uic.loadUi('contentlayoutdialog.ui', self)

        self.show()


class CsvEditor(QMainWindow):
    def __init__(self):
        super(CsvEditor, self).__init__()
        # Load the layout file created in QT Creator
        uic.loadUi('mainwindow.ui', self)
        # This is done to ensure that the UX remains consistent (better than writing manual code for UI)
        # and designed in optimal way using QT's own toolset

        self.csv_table_tab = self.main_document_tab
        self.start_page_tab = self.start_tab

        self.tabWidget.removeTab(1)

        # Load the Start Page tab on application start
        self.tabWidget.setCurrentIndex(0)

        self.btn_load_csv.clicked.connect(self.load_csv)

        # Disable the column layout option and enable only when csv is loaded

        self.action_column_layout.triggered.connect(self.open_column_layout_dialog)
        self.action_column_layout.setDisabled(True)

        # Flag for not detecting cell state change when opening the file
        self.check_cell_change = True
        # Connect cell change function
        self.csv_data_table.cellChanged.connect(self.cell_change_current)
        self.csv_data_table.setAlternatingRowColors(True)

        self.csv_data_table.itemSelectionChanged.connect(self.cell_selection_changed)

        # Disable the plot options by default
        self.set_toolbar_plots(False)

        self.show()

    def open_column_layout_dialog(self):
        self.column_layout_dialog = ColumnLayoutDialog()
        self.column_layout_dialog.setModal(True)

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

            # Enable Column Layout menu option
            self.action_column_layout.setDisabled(False)

            # TODO: Add checkbox for each column header to toogle its visibility in the table

    def cell_change_current(self):
        if self.check_cell_change:
            row = self.csv_data_table.currentRow()
            col = self.csv_data_table.currentColumn()
            value = self.csv_data_table.item(row, col).text()
            print("The current cell is ", row, ", ", col)
            print("In this cell we have: ", value)

    def cell_selection_changed(self):
        print("selection changed")
        # Add a way to identify all the currently selected columns
        cols = self.csv_data_table.selectionModel().selectedColumns()
        self.selected_columns = []
        for index in sorted(cols):
            col = index.column()
            self.selected_columns.append(col)
        print(self.selected_columns)

        # Enable plot toolbars iff exactly 2 columns are selected
        if len(self.selected_columns) == 2:
            self.set_toolbar_plots(True)
        else:
            self.set_toolbar_plots(False)

        # TODO: Add delete action behaviour for individual cells, mulitple cells, columns and rows

    def set_toolbar_plots(self, visibility):
        self.action_toolbar_plot_scatter_points.setEnabled(visibility)
        self.action_toolbar_plot_scatter_points_lines.setEnabled(visibility)
        self.action_toolbar_plot_lines.setEnabled(visibility)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = CsvEditor()
    sys.exit(app.exec_())
