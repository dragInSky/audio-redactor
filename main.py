from PyQt6 import QtWidgets
from gui.main_window import UiMainWindow

import sys


def main():
    app = QtWidgets.QApplication(sys.argv)
    main_window = QtWidgets.QMainWindow()
    ui = UiMainWindow()
    ui.setup_ui(main_window)
    main_window.show()
    sys.exit(app.exec())

    # res_sound = audio_operations.reverse(sound1)
    # audio_operations.export(res_sound, "output/volume.mp3", "mp3")


if __name__ == '__main__':
    main()
