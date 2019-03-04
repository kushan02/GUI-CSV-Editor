import sys
from PyQt5.QtWidgets import QApplication, QLabel, QMainWindow, QPushButton, QAction, QMessageBox


class CsvEditor(QMainWindow):

    def __init__(self, windowTitle="CSV Editor"):
        super(CsvEditor, self).__init__()
        self.setGeometry(100, 100, 500, 300)
        self.setWindowTitle(windowTitle)

        # CALL THE DESIRED VIEW
        self.home()

    def home(self):
        # REQUIRED TO SHOW THE WINDOW
        self.show()

    # CHANGE THE DEFAULT BEHAVIOUR OF THE CLOSE WINDOW
    def closeEvent(self, QCloseEvent):
        QCloseEvent.ignore()
        self.close_application()

    def close_application(self):
        # ADD CONFIRM POPUP
        choice = QMessageBox.question(self, 'Quit', "Are you sure you want to quit?",
                                      QMessageBox.Yes | QMessageBox.No)
        if choice == QMessageBox.Yes:
            print("Quiting")
            sys.exit()


def run():
    app = QApplication(sys.argv)
    GUI = CsvEditor("CSV Editor")
    sys.exit(app.exec_())


if __name__ == '__main__':
    run()
