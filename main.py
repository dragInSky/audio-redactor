from PyQt6 import QtWidgets
from gui.main_window import UiMainWindow
from operations_history import history_handler

import sys


def main():
    history_handler.clear_history()
    app = QtWidgets.QApplication(sys.argv)
    main_window = QtWidgets.QMainWindow()
    ui = UiMainWindow()
    ui.setup_ui(main_window)
    main_window.show()
    sys.exit(app.exec())

    # sound1 = audio_operations.sound_from_file("sample_data/s1.wav", "wav")
    # sound2 = audio_operations.sound_from_file("sample_data/s2.wav", "wav")
    # sound1_mp3 = audio_operations.sound_from_file("sample_data/sample-3s.mp3", "mp3")
    # sound2_mp3 = audio_operations.sound_from_file("sample_data/sample-6s.mp3", "mp3")
    #
    # res_sound = audio_operations.reverse(sound1)
    # audio_operations.export(res_sound, "output/volume.mp3", "mp3")


if __name__ == '__main__':
    main()
