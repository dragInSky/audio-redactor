import globals

from PyQt6 import QtCore, QtWidgets
from PyQt6.QtWidgets import QPushButton, QRadioButton
from PyQt6 import QtGui

from pathlib import Path
from playsound import playsound

from gui import history_window
from history import history_handler
from audio import audio_redactor


class MainWindow:
    def __init__(self):
        self.central_widget = None
        self.grid_layout = None
        self.vertical_layout_widget = None
        self.history_text = None

        self.speed = globals.SPEED
        self.volume = globals.VOLUME

        self.cut_from = 0
        self.cut_to = 0
        self.fragment_cut_from = 0
        self.fragment_cut_to = 0

        self.append_file_name = ''
        self.overlay_file_name = ''
        self.export_folder_name = ''
        self.format = 'wav'

        self.search_path = str(Path.home())

        self.audio_redactor = audio_redactor.AudioRedactor()

    def setup_ui(self, main_window):
        main_window.setObjectName("main_window")
        main_window.resize(800, 600)

        self.central_widget = QtWidgets.QWidget(parent=main_window)
        self.central_widget.setObjectName("central_widget")

        self.vertical_layout_widget = QtWidgets.QWidget(parent=self.central_widget)
        self.vertical_layout_widget.setGeometry(QtCore.QRect(400, 0, 400, 600))
        self.vertical_layout_widget.setObjectName("vertical_layout_widget")

        background_layout = QtWidgets.QWidget(parent=self.vertical_layout_widget)
        background_layout.setGeometry(QtCore.QRect(0, 0, 400, 600))
        QtGui.QImageReader.setAllocationLimit(256)
        background_layout.setStyleSheet("border-image: url(resources/hello.jpg);")

        self.grid_layout = QtWidgets.QGridLayout(self.vertical_layout_widget)
        self.grid_layout.setContentsMargins(0, 0, 0, 0)
        self.grid_layout.setSpacing(15)
        self.grid_layout.setObjectName("grid_layout")

        self.history_text = history_window.setup_history_layout(self.central_widget)

        self.setup_import_layout()
        self.setup_reverse_layout()
        self.setup_speed_layout()
        self.setup_volume_layout()
        self.setup_cut_layout()
        self.setup_fragment_cut_layout()
        self.setup_append_layout()
        self.setup_overlay_layout()
        self.setup_export_layout()
        self.setup_export_settings_layout()
        self.setup_state_layout()
        self.setup_play_layout()

        self.check_box_reverse.setDisabled(True)
        self.check_box_speed.setDisabled(True)
        self.check_box_volume.setDisabled(True)
        self.button_cut.setDisabled(True)
        self.button_fragment.setDisabled(True)
        self.button_export.setDisabled(True)
        self.button_play.setDisabled(True)

        main_window.setCentralWidget(self.central_widget)

        main_window.setWindowTitle("audio redactor")

        QtCore.QMetaObject.connectSlotsByName(main_window)

    def setup_import_layout(self):
        horizontal_layout = QtWidgets.QHBoxLayout()
        horizontal_layout.setObjectName("horizontal_layout_import")

        self.line_edit_import = QtWidgets.QLineEdit(parent=self.vertical_layout_widget)
        self.line_edit_import.setObjectName("line_edit_path_import")
        self.line_edit_import.setPlaceholderText('входной файл')
        self.line_edit_import.setReadOnly(True)
        horizontal_layout.addWidget(self.line_edit_import)

        self.push_button_import = QtWidgets.QPushButton(parent=self.vertical_layout_widget)
        self.push_button_import.setObjectName("push_button_path_import")
        horizontal_layout.addWidget(self.push_button_import)
        self.push_button_import.setText("выбрать файл")

        def import_sound():
            file_name, _ = QtWidgets.QFileDialog.getOpenFileName(
                None, 'Single File', self.search_path, 'Sound files(*.wav *.mp3)'
            )

            if file_name != '':
                self.search_path = file_name

                self.line_edit_import.setText(file_name)
                self.audio_redactor.set_sound(file_name, file_name.split('/')[-1].split('.')[-1])
                self.check_box_reverse.setDisabled(False)
                self.check_box_speed.setDisabled(False)
                self.check_box_volume.setDisabled(False)
                self.button_cut.setDisabled(False)
                self.button_fragment.setDisabled(False)
                self.button_export.setDisabled(False)
                self.button_play.setDisabled(False)

                self.history_text = history_window.history_update(self.history_text)
                self.state_update()
            else:
                self.check_box_reverse.setDisabled(True)
                self.check_box_speed.setDisabled(True)
                self.check_box_volume.setDisabled(True)
                self.button_cut.setDisabled(True)
                self.button_fragment.setDisabled(True)
                self.button_export.setDisabled(True)
                self.button_play.setDisabled(True)

        self.push_button_import.clicked.connect(import_sound)

        self.grid_layout.addLayout(horizontal_layout, 0, 0, 1, 1)

    def setup_reverse_layout(self):
        self.check_box_reverse = QtWidgets.QCheckBox(parent=self.vertical_layout_widget)
        self.check_box_reverse.setObjectName("check_box_reverse")
        self.check_box_reverse.setText("reverse")

        def reverse_apply():
            self.audio_redactor.reverse()
            self.history_text = history_window.history_update(self.history_text)

        self.check_box_reverse.stateChanged.connect(reverse_apply)

        self.grid_layout.addWidget(self.check_box_reverse, 1, 0, 1, 1)

    def speed_change_event(self, value: float):
        self.speed = value
        if self.check_box_speed.isChecked():
            self.audio_redactor.refresh_speed()
            self.audio_redactor.change_speed(self.speed)
            self.history_text = history_window.history_update(self.history_text)

    def setup_speed_layout(self):
        horizontal_layout = QtWidgets.QHBoxLayout()
        horizontal_layout.setObjectName("horizontal_layout_speed")

        self.check_box_speed = QtWidgets.QCheckBox(parent=self.vertical_layout_widget)
        self.check_box_speed.setObjectName("check_box_speed")
        self.check_box_speed.setText("speed")

        horizontal_layout.addWidget(self.check_box_speed)

        def speed_apply():
            if self.check_box_speed.isChecked():
                self.audio_redactor.change_speed(self.speed)
            else:
                self.audio_redactor.refresh_speed()

            self.history_text = history_window.history_update(self.history_text)

        self.check_box_speed.stateChanged.connect(speed_apply)

        self.double_spin_box_speed = QtWidgets.QDoubleSpinBox(parent=self.vertical_layout_widget)
        self.double_spin_box_speed.setMinimum(0.1)
        self.double_spin_box_speed.setMaximum(10.0)
        self.double_spin_box_speed.setSingleStep(0.1)
        self.double_spin_box_speed.setValue(1)
        self.double_spin_box_speed.setObjectName("double_spin_box_speed")

        self.double_spin_box_speed.valueChanged.connect(self.speed_change_event)

        horizontal_layout.addWidget(self.double_spin_box_speed)

        self.grid_layout.addLayout(horizontal_layout, 2, 0, 1, 1)

    def volume_change_event(self, value: float):
        self.volume = value
        if self.check_box_volume.isChecked():
            self.audio_redactor.silent_refresh_volume()
            self.audio_redactor.change_volume(self.volume)
            self.history_text = history_window.history_update(self.history_text)

    def setup_volume_layout(self):
        horizontal_layout = QtWidgets.QHBoxLayout()
        horizontal_layout.setObjectName("horizontal_layout_volume")

        self.check_box_volume = QtWidgets.QCheckBox(parent=self.vertical_layout_widget)
        self.check_box_volume.setObjectName("check_box_volume")
        self.check_box_volume.setText("volume")

        horizontal_layout.addWidget(self.check_box_volume)

        def volume_apply():
            if self.check_box_volume.isChecked():
                self.audio_redactor.change_volume(self.volume)
            else:
                self.audio_redactor.refresh_volume()
            self.history_text = history_window.history_update(self.history_text)

        self.check_box_volume.stateChanged.connect(volume_apply)

        self.double_spin_box_volume = QtWidgets.QDoubleSpinBox(parent=self.vertical_layout_widget)
        self.double_spin_box_volume.setMinimum(-60.0)
        self.double_spin_box_volume.setMaximum(20.0)
        self.double_spin_box_volume.setObjectName("double_spin_box_speed")

        self.double_spin_box_volume.valueChanged.connect(self.volume_change_event)

        horizontal_layout.addWidget(self.double_spin_box_volume)

        self.grid_layout.addLayout(horizontal_layout, 3, 0, 1, 1)

    def cut_from_change_event(self, value: float):
        self.cut_from = value

    def cut_to_change_event(self, value: float):
        self.cut_to = value

    def setup_cut_layout(self):
        horizontal_layout = QtWidgets.QHBoxLayout()
        horizontal_layout.setObjectName("horizontal_layout_cut")

        self.button_cut = QPushButton(parent=self.vertical_layout_widget)
        self.button_cut.setText("cut")
        horizontal_layout.addWidget(self.button_cut)

        def cut_apply():
            self.audio_redactor.cut(self.cut_from, self.cut_to)
            self.state_update()
            self.history_text = history_window.history_update(self.history_text)

        self.button_cut.clicked.connect(cut_apply)

        label_from = QtWidgets.QLabel(parent=self.vertical_layout_widget)
        label_from.setObjectName("label_from_cut")
        horizontal_layout.addWidget(label_from)
        label_from.setText("from:")

        self.double_spin_box_from_cut = QtWidgets.QDoubleSpinBox(parent=self.vertical_layout_widget)
        self.double_spin_box_from_cut.setObjectName("double_spin_box_from_cut")
        horizontal_layout.addWidget(self.double_spin_box_from_cut)

        self.double_spin_box_from_cut.valueChanged.connect(self.cut_from_change_event)

        label_to = QtWidgets.QLabel(parent=self.vertical_layout_widget)
        label_to.setObjectName("label_to_cut")
        horizontal_layout.addWidget(label_to)
        label_to.setText("to:")

        self.double_spin_box_to_cut = QtWidgets.QDoubleSpinBox(parent=self.vertical_layout_widget)
        self.double_spin_box_to_cut.setObjectName("double_spin_box_to_cut")
        horizontal_layout.addWidget(self.double_spin_box_to_cut)

        self.double_spin_box_to_cut.valueChanged.connect(self.cut_to_change_event)

        self.grid_layout.addLayout(horizontal_layout, 4, 0, 1, 1)

    def fragment_cut_from_change_event(self, value: float):
        self.fragment_cut_from = value

    def fragment_cut_to_change_event(self, value: float):
        self.fragment_cut_to = value

    def setup_fragment_cut_layout(self):
        horizontal_layout = QtWidgets.QHBoxLayout()
        horizontal_layout.setObjectName("horizontal_layout_fragment")

        self.button_fragment = QPushButton(parent=self.vertical_layout_widget)
        self.button_fragment.setText("fragment cut")
        horizontal_layout.addWidget(self.button_fragment)

        def fragment_cut_apply():
            self.audio_redactor.fragment_cut(self.fragment_cut_from, self.fragment_cut_to)

            self.state_update()
            self.history_text = history_window.history_update(self.history_text)

        self.button_fragment.clicked.connect(fragment_cut_apply)

        label_from = QtWidgets.QLabel(parent=self.vertical_layout_widget)
        label_from.setObjectName("label_from_fragment")
        horizontal_layout.addWidget(label_from)
        label_from.setText("from:")

        self.double_spin_box_from_fragment = QtWidgets.QDoubleSpinBox(parent=self.vertical_layout_widget)
        self.double_spin_box_from_fragment.setObjectName("double_spin_box_from_fragment_cut")
        horizontal_layout.addWidget(self.double_spin_box_from_fragment)

        self.double_spin_box_from_fragment.valueChanged.connect(self.fragment_cut_from_change_event)

        label_to = QtWidgets.QLabel(parent=self.vertical_layout_widget)
        label_to.setObjectName("label_to_fragment")
        horizontal_layout.addWidget(label_to)
        label_to.setText("to:")

        self.double_spin_box_to_fragment = QtWidgets.QDoubleSpinBox(parent=self.vertical_layout_widget)
        self.double_spin_box_to_fragment.setObjectName("double_spin_box_to_fragment_cut")
        horizontal_layout.addWidget(self.double_spin_box_to_fragment)

        self.double_spin_box_to_fragment.valueChanged.connect(self.fragment_cut_to_change_event)

        self.grid_layout.addLayout(horizontal_layout, 5, 0, 1, 1)

    def setup_append_layout(self):
        horizontal_layout = QtWidgets.QHBoxLayout()
        horizontal_layout.setObjectName("horizontal_layout_append")

        label_append = QtWidgets.QLabel(parent=self.vertical_layout_widget)
        label_append.setObjectName("label_append")
        horizontal_layout.addWidget(label_append)
        label_append.setText("append")

        self.line_edit_append = QtWidgets.QLineEdit(parent=self.vertical_layout_widget)
        self.line_edit_append.setObjectName("line_edit_path_append")
        self.line_edit_append.setReadOnly(True)
        horizontal_layout.addWidget(self.line_edit_append)

        self.button_append_file_choose = QtWidgets.QPushButton(parent=self.vertical_layout_widget)
        self.button_append_file_choose.setObjectName("push_button_path_append")
        horizontal_layout.addWidget(self.button_append_file_choose)
        self.button_append_file_choose.setText("выбрать файл")

        def append_file_choose():
            self.append_file_name, _ = QtWidgets.QFileDialog.getOpenFileName(
                None, 'Single File', self.search_path, 'Sound files(*.wav *.mp3)'
            )

            if self.append_file_name != '':
                self.search_path = self.append_file_name

                self.line_edit_append.setText(self.append_file_name)
                self.audio_redactor.set_sound2(
                    self.append_file_name, self.append_file_name.split('/')[-1].split('.')[-1]
                )
                self.history_text = history_window.history_update(self.history_text)

                self.audio_redactor.append()
                self.state_update()
            else:
                history_handler.info_text('Выберите файл для операции append')
            self.history_text = history_window.history_update(self.history_text)

        self.button_append_file_choose.clicked.connect(append_file_choose)

        self.grid_layout.addLayout(horizontal_layout, 6, 0, 1, 1)

    def setup_overlay_layout(self):
        horizontal_layout = QtWidgets.QHBoxLayout()
        horizontal_layout.setObjectName("horizontal_layout_overlay")

        label_overlay = QtWidgets.QLabel(parent=self.vertical_layout_widget)
        label_overlay.setObjectName("label_overlay")
        horizontal_layout.addWidget(label_overlay)
        label_overlay.setText("overlay")

        self.line_edit_overlay = QtWidgets.QLineEdit(parent=self.vertical_layout_widget)
        self.line_edit_overlay.setObjectName("line_edit_path_overlay")
        self.line_edit_overlay.setReadOnly(True)
        horizontal_layout.addWidget(self.line_edit_overlay)

        self.button_overlay_file_choose = QtWidgets.QPushButton(parent=self.vertical_layout_widget)
        self.button_overlay_file_choose.setObjectName("push_button_path_overlay")
        horizontal_layout.addWidget(self.button_overlay_file_choose)
        self.button_overlay_file_choose.setText("выбрать файл")

        def overlay_file_choose():
            self.overlay_file_name, _ = QtWidgets.QFileDialog.getOpenFileName(
                None, 'Single File', self.search_path, 'Sound files(*.wav *.mp3)'
            )

            if self.overlay_file_name != '':
                self.search_path = self.overlay_file_name

                self.line_edit_overlay.setText(self.overlay_file_name)
                self.audio_redactor.set_sound2(
                    self.overlay_file_name, self.overlay_file_name.split('/')[-1].split('.')[-1]
                )
                self.history_text = history_window.history_update(self.history_text)

                self.audio_redactor.overlay()
                self.state_update()
            else:
                history_handler.info_text('Выберите файл для операции overlay')
            self.history_text = history_window.history_update(self.history_text)

        self.button_overlay_file_choose.clicked.connect(overlay_file_choose)

        self.grid_layout.addLayout(horizontal_layout, 7, 0, 1, 1)

    def setup_export_layout(self):
        horizontal_layout = QtWidgets.QHBoxLayout()
        horizontal_layout.setObjectName("horizontal_layout_export")

        self.line_edit_export = QtWidgets.QLineEdit(parent=self.vertical_layout_widget)
        self.line_edit_export.setObjectName("line_edit_path_export")
        self.line_edit_export.setPlaceholderText('выходная папка')
        self.line_edit_export.setReadOnly(True)
        horizontal_layout.addWidget(self.line_edit_export)

        self.button_export_folder_choose = QtWidgets.QPushButton(parent=self.vertical_layout_widget)
        self.button_export_folder_choose.setObjectName("push_button_path_export")
        horizontal_layout.addWidget(self.button_export_folder_choose)
        self.button_export_folder_choose.setText("выбрать папку")

        def export_path_choose():
            self.export_folder_name = QtWidgets.QFileDialog.getExistingDirectory(
                None, 'Single directory', self.search_path
            )

            if self.export_folder_name != '':
                self.search_path = self.export_folder_name

                self.line_edit_export.setText(self.export_folder_name)
            else:
                history_handler.info_text('Выберите выходную папку')
            self.history_text = history_window.history_update(self.history_text)

        self.button_export_folder_choose.clicked.connect(export_path_choose)

        self.grid_layout.addLayout(horizontal_layout, 8, 0, 1, 1)

    def setup_export_settings_layout(self):
        horizontal_layout = QtWidgets.QHBoxLayout()
        horizontal_layout.setObjectName("horizontal_layout_settings")

        radio_button_wav = QRadioButton("wav")
        radio_button_wav.setChecked(True)
        radio_button_wav.setText('wav')

        def wav_choose():
            self.format = 'wav'

        radio_button_wav.toggled.connect(wav_choose)

        horizontal_layout.addWidget(radio_button_wav)

        radio_button_mp3 = QRadioButton("mp3")
        radio_button_mp3.setText('mp3')

        def mp3_choose():
            self.format = 'mp3'

        radio_button_mp3.toggled.connect(mp3_choose)

        horizontal_layout.addWidget(radio_button_mp3)

        self.line_edit_settings = QtWidgets.QLineEdit(parent=self.vertical_layout_widget)
        self.line_edit_settings.setPlaceholderText('имя выходного файла')
        self.line_edit_settings.setObjectName("line_edit_settings")
        horizontal_layout.addWidget(self.line_edit_settings)

        self.button_export = QPushButton(parent=self.vertical_layout_widget)
        self.button_export.setText("export")
        horizontal_layout.addWidget(self.button_export)

        def export_sound():
            if self.export_folder_name != '':
                self.audio_redactor.audio_export(
                    self.export_folder_name + '/' + self.line_edit_settings.text(), self.format
                )
            else:
                history_handler.info_text('Выберите выходной путь')
            self.history_text = history_window.history_update(self.history_text)

        self.button_export.clicked.connect(export_sound)

        self.grid_layout.addLayout(horizontal_layout, 9, 0, 1, 1)

    def state_update(self):
        self.label_state.setText(
            "sound length without speed effect: " + str(len(self.audio_redactor.sound) / 1000) + " seconds"
        )

    def setup_state_layout(self):
        horizontal_layout = QtWidgets.QHBoxLayout()
        horizontal_layout.setObjectName("horizontal_layout_state")

        self.label_state = QtWidgets.QLabel(parent=self.vertical_layout_widget)
        self.label_state.setObjectName("label_state")
        horizontal_layout.addWidget(self.label_state)
        self.state_update()

        self.grid_layout.addLayout(horizontal_layout, 10, 0, 1, 1)

    def setup_play_layout(self):
        self.button_play = QPushButton(parent=self.vertical_layout_widget)
        self.button_play.setText("play")

        def play_audio():
            self.audio_redactor.tmp_save(globals.TMP_EXPORT_PATH)
            playsound(globals.TMP_EXPORT_PATH)

        self.button_play.clicked.connect(play_audio)

        self.grid_layout.addWidget(self.button_play, 11, 0, 1, 1)
