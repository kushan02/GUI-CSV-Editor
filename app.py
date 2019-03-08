# -*- coding: utf-8 -*-
""" CSV Editor

This project done for the completion of screening task for python, FOSSEE 2019 fellowship.
The task requirement was to implement a fully functional GUI CSV Editor by using Python and PyQT as open source project hosted on github.

Project link on Github: https://github.com/kushan02/fsf_2019_screening_task2

Created On: Mar 4, 2019
Author: Kushan Mehta
Email: kushan.mehta02@gmail.com

Features:
    1. Load a CSV file and view it in table form
    2. Add data to the table as a new blank row
    3. Edit Data in the table
    4. Delete data from the table:
        1) Option to delete whole column or whole row and also individual cells
    5. show/hide Columns: Select which columns should be visible in the desired table
    6. Plot any two columns with following plots in a new tab:
        1) Plot scatter points
        2) Plot scatter points with smooth lines
        3) Plot lines
    7. Ability to add a custom title for the plot on the fly
    8. Ability to flip the X and Y axes on the fly
    9. Save the plot as PNG file
    10. Prompt for saving the file in case any modifications are made to the original file

The below code uses PEP 8 style guide for Python

"""

from PyQt5 import uic
from PyQt5.QtWidgets import QMainWindow, QApplication, QFileDialog, QTableWidgetItem, QDialog, \
    QMessageBox, QVBoxLayout, QCheckBox

import os
import sys
import csv  # Used for manipulating csv files

from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
import matplotlib.pyplot as plt
from scipy.interpolate import make_interp_spline  # Below two libraries are used to plot the smooth curve
import numpy as np


# TODO: Refactor the code to make it efficient and more readable
# TODO: Add requirements.txt file to project


class CsvEditor(QMainWindow):
    def __init__(self):
        super(CsvEditor, self).__init__()
        # Load the layout file created in QT Creator
        uic.loadUi('mainwindow.ui', self)
        # This is done to ensure that the UX remains consistent (better than writing manual code for UI)
        # and designed in optimal way using QT's own toolset

        self.csv_table_tab = self.main_document_tab
        self.start_page_tab = self.start_tab
        self.plot_page_tab = self.plot_tab

        # Load the Start Page tab on application start
        self.tabWidget.setCurrentIndex(0)

        # Disable the column layout option and enable only when csv is loaded
        self.action_column_layout.setEnabled(False)
        # Disable add data option and enable only when csv is loaded
        self.action_add_data.setEnabled(False)
        self.action_toolbar_add_data.setEnabled(False)
        self.action_edit_data.setEnabled(False)
        self.action_delete_selected.setEnabled(False)
        self.action_toolbar_delete_selected.setEnabled(False)
        self.action_close_file.setEnabled(False)

        # Flag for not detecting cell state change when opening the file
        self.check_cell_change = True

        # Flag for detecting any changes made to file (unsaved state)
        self.file_changed = False

        # Disable save options before loading file
        self.set_save_enabled(False)

        self.csv_data_table.setAlternatingRowColors(True)

        # Disable the plot options by default
        self.set_plot_options(False)

        # Set all the connection of buttons, menu items, toolbar etc to corresponding functions
        self.set_connections()

        # Remove plot and file page tab
        self.tabWidget.removeTab(2)
        self.tabWidget.removeTab(1)

        self.plot_inverted = False
        self.figure = None

        self.column_visibility_dialog_reference = None

        self.set_bottom_toolbar_info(default_values=True)

        # TODO: Add right click context menu for cell items (last stage of project if time permits)

        self.show()

    def set_bottom_toolbar_info(self, default_values=False):
        # Fill the info for the bottom toolbar
        if default_values:
            # self.toolbar_bottom_info.setStyleSheet("QToolBar{border-right:1px solid black;}")
            self.action_toolbar_bottom_column_count.setIconText("Column count -")
            self.action_toolbar_bottom_row_count.setIconText("Row count -")
            self.action_toolbar_bottom_source.setIconText("Source: No Source")
            self.action_toolbar_bottom_column.setIconText("Column -")
            self.action_toolbar_bottom_row.setIconText("Row -")
            self.action_toolbar_bottom_selected_cells.setIconText("Selected Cells -")
            self.action_toolbar_bottom_text_length.setIconText("Text Length -")
            self.cells_selected = []
            self.csv_file_name = 'No Source'
        else:
            self.action_toolbar_bottom_column_count.setIconText(
                "Column count " + str(self.csv_data_table.columnCount()))
            self.action_toolbar_bottom_row_count.setIconText("Row count " + str(self.csv_data_table.rowCount()))
            self.action_toolbar_bottom_source.setIconText("Source: " + self.csv_file_name)
            self.action_toolbar_bottom_column.setIconText("Column " + str(self.csv_data_table.currentColumn() + 1))
            self.action_toolbar_bottom_row.setIconText("Row " + str(self.csv_data_table.currentRow() + 1))
            self.action_toolbar_bottom_selected_cells.setIconText("Selected Cells " + str(len(self.cells_selected)))
        try:
            row = self.csv_data_table.currentRow()
            col = self.csv_data_table.currentColumn()
            value = self.csv_data_table.item(row, col).text()
        except:
            value = ''
        self.action_toolbar_bottom_text_length.setIconText("Text Length " + str(len(value)))

    def set_connections(self):
        # Column layout dialog function
        self.action_column_layout.triggered.connect(self.open_column_layout_dialog)

        # Connect cell change function
        self.csv_data_table.cellChanged.connect(self.cell_change_current)
        self.csv_data_table.itemSelectionChanged.connect(self.cell_selection_changed)

        # Load csv file function
        self.action_load_file.triggered.connect(self.load_csv)
        self.action_toolbar_open_file.triggered.connect(self.load_csv)
        self.btn_load_csv.clicked.connect(self.load_csv)

        # Save csv file function
        self.action_toolbar_save_file.triggered.connect(self.save_file)
        self.action_save_file.triggered.connect(self.save_file)

        # Radiobox for plotting axes flipped or not
        self.radio_plot_xy.toggled.connect(self.flip_plot_axes)

        # Plot toolbar functions
        self.action_toolbar_plot_scatter_points.triggered.connect(self.plot_scatter_points)
        self.action_toolbar_plot_scatter_points_lines.triggered.connect(self.plot_scatter_points_lines)
        self.action_toolbar_plot_lines.triggered.connect(self.plot_lines)
        self.action_plot_scatter_points.triggered.connect(self.plot_scatter_points)
        self.action_plot_scatter_points_lines.triggered.connect(self.plot_scatter_points_lines)
        self.action_plot_lines.triggered.connect(self.plot_lines)

        # Close plot function
        self.btn_close_plot.clicked.connect(self.close_plot_tab)

        # Save plot function
        self.btn_save_plot.clicked.connect(self.save_plot_as_png)
        self.action_save_plot_png.triggered.connect(self.save_plot_as_png)
        self.action_toolbar_save_plot_png.triggered.connect(self.save_plot_as_png)

        # Set plot title
        self.plot_title = 'Plot Title'
        self.btn_set_plot_title.clicked.connect(self.set_plot_title)

        # Add data function
        self.action_add_data.triggered.connect(self.add_blank_data_row)
        self.action_toolbar_add_data.triggered.connect(self.add_blank_data_row)

        # Delete data function
        self.action_toolbar_delete_selected.triggered.connect(self.delete_selection)
        self.action_delete_selected.triggered.connect(self.delete_selection)

        # Edit data menu item function
        self.action_edit_data.triggered.connect(self.edit_current_cell)

        # Close file function
        self.action_close_file.triggered.connect(self.close_file)

    def add_blank_data_row(self):
        last_row_count = self.csv_data_table.rowCount()
        column_count = self.csv_data_table.columnCount()
        self.csv_data_table.insertRow(last_row_count)
        for empty_col in range(0, column_count):
            item = QTableWidgetItem('')
            self.csv_data_table.setItem(last_row_count, empty_col, item)

    def edit_current_cell(self):
        cells = self.csv_data_table.selectionModel().selectedIndexes()
        if len(cells) == 1:
            for cell in sorted(cells):
                r = cell.row()
                c = cell.column()
                self.csv_data_table.editItem(self.csv_data_table.item(r, c))

    def delete_selection(self):
        # TODO: Add undo, redo etc functionality
        # If whole column is selected remove that column completely
        # If whole row is selected remove that row completely
        # Else make the selected cells blank

        selected_columns = sorted(self.selected_columns, reverse=True)
        selected_rows = sorted(self.selected_rows, reverse=True)

        fileChanged = False
        if len(selected_rows) > 0 or len(selected_columns) > 0:
            self.file_changed = True
            self.set_save_enabled(True)

        # delete any fully selected column
        for col in selected_columns:
            self.csv_data_table.removeColumn(col)

        self.selected_columns.clear()

        # delete any fully selected row
        for row in selected_rows:
            self.csv_data_table.removeRow(row)

        self.selected_rows.clear()

        # Now check if any individual cells are to be deleted

        cells = self.csv_data_table.selectionModel().selectedIndexes()

        if len(cells) > 0:
            self.file_changed = True
            self.set_save_enabled(True)

        for cell in sorted(cells):
            r = cell.row()
            c = cell.column()
            self.csv_data_table.item(r, c).setText('')

    def open_column_layout_dialog(self):

        # Create a new instance iff required, else save resources
        if self.column_visibility_dialog_reference is None:
            print("HEADERS", self.column_headers)
            self.column_visibility_dialog_reference = ColumnLayoutDialog()

        self.column_visibility_dialog_reference.add_header_visible_options(self.column_headers_all, self.column_headers)
        self.column_visibility_dialog_reference.setModal(True)

        # invoke exec_() method instead of show to block the main thread till the selection is done
        self.column_visibility_dialog_reference.exec_()

        # Now hide the invisible headers
        self.hide_invisible_headers()

    def hide_invisible_headers(self):
        print("HIDE: ", self.column_headers)
        # Hide all the non selected columns
        col_index = 0
        for header in self.column_headers_all:
            if header in self.column_headers:
                self.csv_data_table.setColumnHidden(col_index, False)
                self.file_changed = True
                self.set_save_enabled(True)
            else:
                self.csv_data_table.setColumnHidden(col_index, True)
            col_index = col_index + 1

    def load_csv(self):

        # if self.file_changed:
        #     self.prompt_save_before_closing()

        # Close any already opened file if any
        self.close_file()

        # Disable cell change check to avoid crashes
        self.check_cell_change = False

        # Set the flag to no changes in current file state
        self.file_changed = False
        self.set_save_enabled(False)

        csv_file_path = QFileDialog.getOpenFileName(self, "Load CSV File", "", 'CSV(*.csv)')

        # Proceed if and only if a valid file is selected and the file dialog is not cancelled
        if csv_file_path[0]:

            # self.csv_file_name = QFileInfo(csv_file_path).fileName()
            # self.csv_file_name = QUrl.fromLocalFile(csv_file_path)

            filepath = os.path.normpath(csv_file_path[0])
            filename = filepath.split(os.sep)
            self.csv_file_name = filename[-1]

            with open(csv_file_path[0], newline='') as csv_file:

                self.csv_data_table.setRowCount(0)
                self.csv_data_table.setColumnCount(0)

                csv_file_read = csv.reader(csv_file, delimiter=',', quotechar='|')

                # Fetch the column headers and move the iterator to actual data
                self.column_headers = next(csv_file_read)

                # A backup to keep a list of all the headers to toogle their view later
                self.column_headers_all = self.column_headers[:]

                for row_data in csv_file_read:
                    row = self.csv_data_table.rowCount()
                    self.csv_data_table.insertRow(row)
                    self.csv_data_table.setColumnCount(len(row_data))
                    for column, stuff in enumerate(row_data):
                        item = QTableWidgetItem(stuff)
                        self.csv_data_table.setItem(row, column, item)

                self.csv_data_table.setHorizontalHeaderLabels(self.column_headers)

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
            self.action_column_layout.setEnabled(True)
            self.action_add_data.setEnabled(True)
            self.action_toolbar_add_data.setEnabled(True)
            self.action_close_file.setEnabled(True)

            self.set_bottom_toolbar_info()

    def save_file(self):

        file_save_path = QFileDialog.getSaveFileName(self, 'Save CSV', "", 'CSV(*.csv)')

        if file_save_path[0]:
            with open(file_save_path[0], 'w', newline="") as csv_file:
                writer = csv.writer(csv_file)
                # Add the header row explicitly
                writer.writerow(self.column_headers)
                for row in range(self.csv_data_table.rowCount()):
                    row_data = []
                    for column in range(self.csv_data_table.columnCount()):

                        # Check if the current column is set to be visible, if not skip it
                        if self.csv_data_table.isColumnHidden(column):
                            continue

                        item = self.csv_data_table.item(row, column)
                        if item is not None:
                            row_data.append(item.text())
                        else:
                            row_data.append('')
                    writer.writerow(row_data)

            # Set the flag to no changes in current file state
            self.file_changed = False
            self.set_save_enabled(False)

            # TODO: add a better variant of message box compared to about like sucess, critical, warning etc according to context
            QMessageBox.about(self, "Success!", "Your file has been saved successfully.")

    def cell_change_current(self):

        # Add exception handling for case when new row is added to unmodified file
        try:
            if self.check_cell_change:
                row = self.csv_data_table.currentRow()
                col = self.csv_data_table.currentColumn()
                value = self.csv_data_table.item(row, col).text()
                print("The current cell is ", row, ", ", col)
                print("In this cell we have: ", value)

                self.set_bottom_toolbar_info()

        except:
            pass
        finally:
            # Set the flag to changes in current file state
            if self.check_cell_change:
                self.file_changed = True
                self.set_save_enabled(True)

    def cell_selection_changed(self):

        # Enable Edit Cell menu if a single cell is selection else disable it
        self.cells_selected = self.csv_data_table.selectionModel().selectedIndexes()
        if len(self.cells_selected) == 1:
            self.action_edit_data.setEnabled(True)
        else:
            self.action_edit_data.setEnabled(False)

        # Enable delete options iff 1 or more cells are selected
        if len(self.cells_selected) >= 1:
            self.action_delete_selected.setEnabled(True)
            self.action_toolbar_delete_selected.setEnabled(True)
        else:
            self.action_delete_selected.setEnabled(False)
            self.action_toolbar_delete_selected.setEnabled(False)

        # Add a way to identify all the currently selected columns
        cols = self.csv_data_table.selectionModel().selectedColumns()
        self.selected_columns = []
        for index in sorted(cols):
            col = index.column()
            self.selected_columns.append(col)
        print(self.selected_columns)

        rows = self.csv_data_table.selectionModel().selectedRows()
        self.selected_rows = []
        for index in sorted(rows):
            row = index.row()
            self.selected_rows.append(row)
        print(self.selected_rows)

        self.set_bottom_toolbar_info()

        # Enable plot toolbars iff exactly 2 columns are selected
        if len(self.selected_columns) == 2:
            self.set_plot_options(True)
        else:
            self.set_plot_options(False)

    def set_plot_options(self, visibility):

        self.action_toolbar_plot_scatter_points.setEnabled(visibility)
        self.action_toolbar_plot_scatter_points_lines.setEnabled(visibility)
        self.action_toolbar_plot_lines.setEnabled(visibility)
        self.action_plot_scatter_points.setEnabled(visibility)
        self.action_plot_scatter_points_lines.setEnabled(visibility)
        self.action_plot_lines.setEnabled(visibility)
        # Enable this option only once the plot is drawn
        self.action_save_plot_png.setEnabled(False)
        self.action_toolbar_save_plot_png.setEnabled(False)

    def set_save_enabled(self, enabled):
        self.action_toolbar_save_file.setEnabled(enabled)
        self.action_save_file.setEnabled(enabled)

    def close_file(self):
        if self.file_changed:
            self.prompt_save_before_closing()

        self.set_bottom_toolbar_info(default_values=True)

        # Disable Column Layout menu option
        self.action_column_layout.setEnabled(False)
        self.action_add_data.setEnabled(False)
        self.column_visibility_dialog_reference = None
        # Disable other file related options
        self.action_toolbar_add_data.setEnabled(False)
        self.action_close_file.setEnabled(False)

        self.column_headers_all = []
        self.column_headers = []

        # Remove plot and file page tab
        try:
            # with each deletion index of the current tab decreases
            self.tabWidget.removeTab(0)
            self.tabWidget.removeTab(0)
            self.tabWidget.removeTab(0)
        except:
            pass

        self.tabWidget.insertTab(0, self.start_page_tab, "Start Page")
        # Disable the column layout option and enable only when csv is loaded
        self.action_column_layout.setEnabled(False)
        # Disable add data option and enable only when csv is loaded
        self.action_add_data.setEnabled(False)
        self.action_toolbar_add_data.setEnabled(False)
        self.action_edit_data.setEnabled(False)
        self.action_delete_selected.setEnabled(False)
        self.action_toolbar_delete_selected.setEnabled(False)
        self.action_close_file.setEnabled(False)
        self.action_save_file.setEnabled(False)

        self.set_plot_options(False)

        # If user selected not to save changes, in this case var wont change to false withing prompt funtion
        self.file_changed = False
        self.set_save_enabled(False)

    def prompt_save_before_closing(self):
        if self.file_changed:
            choice = QMessageBox.question(self, 'Save File', "Do you want to save file before quiting?",
                                          QMessageBox.Yes | QMessageBox.No)
            if choice == QMessageBox.Yes:
                self.save_file()

    def closeEvent(self, QCloseEvent):
        self.prompt_save_before_closing()
        # QCloseEvent.ignore()
        # self.close_application()

    def plot_scatter_points(self):
        self.plot(1)

    def plot_scatter_points_lines(self):
        self.plot(2)

    def plot_lines(self):
        self.plot(3)

    def set_plot_title(self):
        plot_title = self.input_plot_title.text()
        if plot_title:
            self.plot_title = self.input_plot_title.text()
            # Redraw the plot with given title
            if not self.plot_inverted:
                self.draw_plot(self.data_x_axis, self.data_y_axis, self.label_x_axis, self.label_y_axis,
                               self.plot_inverted)
            else:
                self.draw_plot(self.data_y_axis, self.data_x_axis, self.label_y_axis, self.label_x_axis,
                               self.plot_inverted)
        else:
            QMessageBox.about(self, "Error!", "Please enter a title to set in the plot")

    def plot(self, plotType):

        # Build plotting data
        # TODO: Try to improve time complexity of the building up of plotting data
        self.data_x_axis = []
        self.data_y_axis = []
        for i in range(0, self.csv_data_table.rowCount()):
            value = self.csv_data_table.item(i, self.selected_columns[0]).text()
            self.data_x_axis.append(value)
            value = self.csv_data_table.item(i, self.selected_columns[1]).text()
            self.data_y_axis.append(value)

        self.label_x_axis = self.csv_data_table.horizontalHeaderItem(self.selected_columns[0]).text()
        self.label_y_axis = self.csv_data_table.horizontalHeaderItem(self.selected_columns[1]).text()
        print(self.data_x_axis, self.data_y_axis)

        # Avoid duplication of resources if already allocated
        if self.figure is None:
            self.figure = plt.figure()
            self.canvas = FigureCanvas(self.figure)

            # self.plot_frame_horizontal.addStretch()
            self.plot_frame_horizontal.addWidget(self.canvas)
            # self.plot_frame_horizontal.addStretch()

        # Ensures only 2 tabs at max are open at a time - file and plot tabs respectively
        if self.tabWidget.count() == 1:
            self.tabWidget.insertTab(1, self.plot_page_tab, "Plot")

        self.tabWidget.setCurrentIndex(1)

        # Set plot type (1,2,3 => order according to scatter, scatter-line, line)
        self.plotType = plotType

        self.draw_plot(self.data_x_axis, self.data_y_axis, self.label_x_axis, self.label_y_axis, self.plot_inverted)

    def flip_plot_axes(self):
        self.plot_inverted = not self.plot_inverted
        print("invert = ", self.plot_inverted)
        if not self.plot_inverted:
            self.draw_plot(self.data_x_axis, self.data_y_axis, self.label_x_axis, self.label_y_axis, self.plot_inverted)
        else:
            self.draw_plot(self.data_y_axis, self.data_x_axis, self.label_y_axis, self.label_x_axis, self.plot_inverted)

    def draw_plot(self, data_x_axis, data_y_axis, label_x_axis, label_y_axis, flipped=False):

        # Flipped tells us whether to invert the current x, y axis
        self.figure.clear()

        # Fix for plot having cutoff text or labels
        self.figure.tight_layout()
        self.figure.subplots_adjust(left=0.1, right=0.9, bottom=0.3, top=0.9)

        self.figure.suptitle(self.plot_title)

        ax = self.figure.add_subplot(111)

        # Add another argument fontsize = 10 to change the fontsize of the labels

        ax.set_xlabel(label_x_axis)
        ax.set_ylabel(label_y_axis)

        if self.plotType == 1:
            print("plotType = 1")
            ax.plot(data_x_axis, data_y_axis)
        elif self.plotType == 2:

            # SMOOTH CURVE CURRENTLY WORKS ONLY WIHT INTEGRAL VALUES
            # TODO: Understand in a better way what exactly is expected in smooth curve plotting

            print("plotType = 2")

            # Try block is added as as of now smoth line can be plotting only if the data consists entirely of numeric value

            # Smoothen the curve points
            try:
                for i in range(0, len(data_x_axis)):
                    data_x_axis[i] = int(data_x_axis[i])
                    data_y_axis[i] = int(data_y_axis[i])

                print(data_x_axis, data_y_axis)

                data_x_axis = sorted(data_x_axis)
                data_y_axis = sorted(data_y_axis)

                T = np.array(data_x_axis)
                power = np.array(data_y_axis)

                xnew = np.linspace(T.min(), T.max(),
                                   300)  # 300 represents number of points to make between T.min and T.max

                spl = make_interp_spline(T, power, k=3)  # BSpline object
                power_smooth = spl(xnew)

                ax.plot(xnew, power_smooth)
            except:
                ax.plot(data_x_axis, data_y_axis)

            # ax.plot(data_x_axis, data_y_axis)

        else:
            print("plotType = 3")
            ax.scatter(data_x_axis, data_y_axis)

        self.canvas.draw()
        # Enable the option as plot is now drawn
        self.action_save_plot_png.setEnabled(True)
        self.action_toolbar_save_plot_png.setEnabled(True)

    def save_plot_as_png(self):

        file_save_path = QFileDialog.getSaveFileName(self, 'Save Plot PNG', "", "PNG (*.png)|*.png")

        if file_save_path[0]:
            self.figure.savefig(file_save_path[0], bbox_inches='tight')
            QMessageBox.about(self, "Success!", "Your plot has been saved as png image successfully.")

    def close_plot_tab(self):
        # Temporary tab reference is kept to avoid garbage collection of the UI of tab
        tmp_tab_reference = self.plot_page_tab
        self.tabWidget.removeTab(1)
        self.tabWidget.setCurrentIndex(0)
        self.plot_page_tab = tmp_tab_reference


class ColumnLayoutDialog(QDialog):
    def __init__(self):
        super(ColumnLayoutDialog, self).__init__()
        uic.loadUi('contentlayoutdialog.ui', self)

        self.visible_headers_list = []

        self.btn_save_header_view.clicked.connect(self.save_header_list)

    def add_header_visible_options(self, header_list, visible_list):

        layout = QVBoxLayout()
        for header in header_list:
            check_box = QCheckBox(header)
            if self.visible_headers_list:
                if header in self.visible_headers_list:
                    check_box.setChecked(True)
                else:
                    check_box.setChecked(False)
            else:
                check_box.setChecked(True)
            layout.addWidget(check_box)

        self.column_layout_list_scroll_area.setLayout(layout)
        self.visible_headers_list = visible_list

    def save_header_list(self):
        self.visible_headers_list.clear()

        check_box_list = self.column_layout_list_scroll_area.findChildren(QCheckBox)
        for loop in range(len(check_box_list)):
            if check_box_list[loop].isChecked():
                self.visible_headers_list.append(check_box_list[loop].text())
        print(self.visible_headers_list)

    def get_visible_header_list(self):
        return self.get_visible_header_list


if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = CsvEditor()
    sys.exit(app.exec_())
