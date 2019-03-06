import sys

from PyQt5.QtCore import pyqtSignal
from PyQt5.QtWidgets import QApplication, QLabel, QMainWindow, QPushButton, QAction, QMessageBox, QWidget, QVBoxLayout, \
    QHBoxLayout, QStackedWidget


class StartPage1(QMainWindow):
    clicked = pyqtSignal()

    def __init__(self):
        super().__init__()
        self.init_ui()

    def init_ui(self):
        v_layout = QVBoxLayout()
        h_layout_label = QHBoxLayout()

        welcome_label = QLabel("OTHR CSV Editor's Start Page")

        h_layout_label.addStretch()
        h_layout_label.addWidget(welcome_label)
        h_layout_label.addStretch()

        v_layout.addLayout(h_layout_label)

        open_file_btn = QPushButton("Otherpen File")
        v_layout.addStretch()
        v_layout.addWidget(open_file_btn)
        v_layout.addStretch()

        self.setLayout(v_layout)
        self.setWindowTitle("Start Page")

        # open_file_btn.clicked.connect(CsvEditor.change_start_page_to_home_page)

        open_file_btn.clicked.connect(self.clicked.emit)

        # self.show()


class StartPage(QWidget):
    clicked = pyqtSignal()

    def __init__(self):
        super().__init__()
        self.init_ui()

    def init_ui(self):
        v_layout = QVBoxLayout()
        h_layout_label = QHBoxLayout()

        welcome_label = QLabel("CSV Editor's Start Page")

        h_layout_label.addStretch()
        h_layout_label.addWidget(welcome_label)
        h_layout_label.addStretch()

        v_layout.addLayout(h_layout_label)

        open_file_btn = QPushButton("Open File")
        v_layout.addStretch()
        v_layout.addWidget(open_file_btn)
        v_layout.addStretch()

        self.setLayout(v_layout)
        self.setWindowTitle("Start Page")

        open_file_btn.clicked.connect(CsvEditor.change_start_page_to_home_page)

        # self.show()


class CsvEditor(QMainWindow):

    def __init__(self, window_title="CSV Editor"):
        super(CsvEditor, self).__init__()
        self.setGeometry(100, 100, 500, 300)
        self.setWindowTitle(window_title)

        # CALL THE DESIRED VIEW
        # self.home()
        self.central_widget = QStackedWidget()
        self.setCentralWidget(self.central_widget)

        self.start_page_widget = StartPage()
        self.central_widget.addWidget(self.start_page_widget)

        self.another_widget = StartPage1()
        self.central_widget.addWidget(self.another_widget)

        self.central_widget.setCurrentWidget(self.start_page_widget)

        self.start_page_widget.clicked.connect(self.change_start_page_to_home_page)

    def init_ui(self):
        pass

    def change_start_page_to_home_page(self):
        print("inside the change function")
        # self.test_btn = QPushButton("TEST BTN")
        self.another_widget.show()
        # self.central_widget.setCurrentWidget(self.another_widget)

    def home(self):
        # REQUIRED TO SHOW THE WINDOW
        self.start_page_widget = StartPage()
        self.setCentralWidget(self.start_page_widget)

        self.another_widget = StartPage1()

        # self.show()

    # CHANGE THE DEFAULT BEHAVIOUR OF THE CLOSE WINDOW
    # def closeEvent(self, QCloseEvent):
    #     QCloseEvent.ignore()
    #     self.close_application()

    def close_application(self):
        # ADD CONFIRM POPUP
        choice = QMessageBox.question(self, 'Quit', "Are you sure you want to quit?",
                                      QMessageBox.Yes | QMessageBox.No)
        if choice == QMessageBox.Yes:
            print("Quiting")
            sys.exit()


def run():
    app = QApplication(sys.argv)
    gui = CsvEditor("CSV Editor")
    gui.show()
    sys.exit(app.exec_())


if __name__ == '__main__':
    run()
