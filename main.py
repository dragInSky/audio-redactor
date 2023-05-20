from PyQt6 import QtWidgets
from gui.main_window import MainWindow

import sys


def main():
    app = QtWidgets.QApplication([])
    main_window = QtWidgets.QMainWindow()
    ui = MainWindow()
    ui.setup_ui(main_window)
    main_window.show()
    sys.exit(app.exec())


if __name__ == '__main__':
    main()
