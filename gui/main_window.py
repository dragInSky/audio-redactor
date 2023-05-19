from PyQt6 import QtCore, QtWidgets
from PyQt6.QtWidgets import QPushButton

from history import history_handler
from audio import audio_redactor
from audio import base_values
from pydub import AudioSegment


class UiMainWindow:

    def __init__(self):
        self.fragment_cut_to = 0
        self.fragment_cut_from = 0
        self.audio = AudioSegment.from_file('sample_data/s1.wav', format='wav')
        self.cut_to = len(self.audio)
        self.cut_from = 0
        self.volume = base_values.VOLUME
        self.speed = base_values.SPEED

    def setup_ui(self, main_window):
        self.audio_redactor = audio_redactor.AudioRedactor()
        self.audio_redactor.setSound(self.audio)

        main_window.setObjectName("main_window")
        main_window.resize(850, 600)

        self.central_widget = QtWidgets.QWidget(parent=main_window)
        self.central_widget.setObjectName("central_widget")

        self.verticalLayoutWidget = QtWidgets.QWidget(parent=self.central_widget)
        self.verticalLayoutWidget.setGeometry(QtCore.QRect(500, 0, 350, 350))
        self.verticalLayoutWidget.setObjectName("verticalLayoutWidget")

        self.grid_layout = QtWidgets.QGridLayout(self.verticalLayoutWidget)
        self.grid_layout.setContentsMargins(0, 0, 0, 0)
        self.grid_layout.setSpacing(15)
        self.grid_layout.setObjectName("grid_layout")

        self.setup_import_layout()
        self.setup_reverse()
        self.setup_speed_layout()
        self.setup_volume_layout()
        self.setup_cut_layout()
        self.setup_fragment_cut_layout()
        self.setup_append_layout()
        self.setup_overlay_layout()
        self.setup_export_layout()
        self.setup_history()

        main_window.setCentralWidget(self.central_widget)

        main_window.setWindowTitle("audio redactor")
        QtCore.QMetaObject.connectSlotsByName(main_window)

    def reverse_event(self):
        self.audio_redactor.reverse()
        self.history_update()

    def speed_change_event(self, value: float):
        self.speed = value

    def speed_apply(self):
        if self.check_box_speed.isChecked():
            self.audio_redactor.change_speed(self.speed)
        else:
            self.audio_redactor.change_speed(base_values.SPEED)
        self.history_update()

    def volume_change_event(self, value: float):
        self.volume = value

    def volume_apply(self):
        if self.check_box_speed.isChecked():
            self.audio_redactor.change_volume(self.volume)
        else:
            self.audio_redactor.change_volume(base_values.VOLUME)
        self.history_update()

    def cut_from_change_event(self, value: float):
        self.cut_from = value

    def cut_to_change_event(self, value: float):
        self.cut_to = value

    def cut_apply(self):
        if self.check_box_speed.isChecked():
            self.audio_redactor.cut(self.cut_from, self.cut_to)
        else:
            self.audio_redactor.cut(self.cut_from, self.cut_to)
        self.history_update()

    def fragment_cut_from_change_event(self, value: float):
        self.fragment_cut_from = value

    def fragment_cut_to_change_event(self, value: float):
        self.fragment_cut_to = value

    def fragment_cut_apply(self):
        if self.check_box_speed.isChecked():
            self.audio_redactor.fragment_cut(self.fragment_cut_from, self.fragment_cut_to)
        else:
            self.audio_redactor.fragment_cut(self.fragment_cut_from, self.fragment_cut_to)
        self.history_update()

    def append_apply(self):
        # self.audio_redactor.append()
        self.history_update()

    def overlay_apply(self):
        # self.audio_redactor.overlay()
        self.history_update()

    def export(self):
        self.audio_redactor.export('output/output.wav', 'wav')
        self.history_update()

    def setup_import_layout(self):
        horizontal_layout = QtWidgets.QHBoxLayout()
        horizontal_layout.setObjectName("horizontal_layout_import")

        label = QtWidgets.QLabel(parent=self.verticalLayoutWidget)
        label.setObjectName("label_import")
        horizontal_layout.addWidget(label)
        label.setText("import")

        self.line_edit_import = QtWidgets.QLineEdit(parent=self.verticalLayoutWidget)
        self.line_edit_import.setObjectName("line_edit_path_import")
        self.line_edit_import.setReadOnly(True)
        horizontal_layout.addWidget(self.line_edit_import)

        self.push_button_import = QtWidgets.QPushButton(parent=self.verticalLayoutWidget)
        self.push_button_import.setObjectName("push_button_path_import")
        horizontal_layout.addWidget(self.push_button_import)
        self.push_button_import.setText("выбрать файл")

        self.grid_layout.addLayout(horizontal_layout, 0, 0, 1, 1)

    def setup_reverse(self):
        self.check_box_reverse = QtWidgets.QCheckBox(parent=self.verticalLayoutWidget)
        self.check_box_reverse.setObjectName("check_box_reverse")
        self.check_box_reverse.setText("reverse")

        self.check_box_reverse.stateChanged.connect(self.reverse_event)

        self.grid_layout.addWidget(self.check_box_reverse, 1, 0, 1, 1)

    def setup_speed_layout(self):
        horizontal_layout = QtWidgets.QHBoxLayout()
        horizontal_layout.setObjectName("horizontal_layout_speed")

        self.check_box_speed = QtWidgets.QCheckBox(parent=self.verticalLayoutWidget)
        self.check_box_speed.setObjectName("check_box_speed")
        self.check_box_speed.setText("speed")

        horizontal_layout.addWidget(self.check_box_speed)

        self.check_box_speed.stateChanged.connect(self.speed_apply)

        self.double_spin_box_speed = QtWidgets.QDoubleSpinBox(parent=self.verticalLayoutWidget)
        self.double_spin_box_speed.setMinimum(0.1)
        self.double_spin_box_speed.setMaximum(10.0)
        self.double_spin_box_speed.setValue(1)
        self.double_spin_box_speed.setObjectName("double_spin_box_speed")

        self.double_spin_box_speed.valueChanged.connect(self.speed_change_event)

        horizontal_layout.addWidget(self.double_spin_box_speed)

        self.grid_layout.addLayout(horizontal_layout, 2, 0, 1, 1)

    def setup_volume_layout(self):
        horizontal_layout = QtWidgets.QHBoxLayout()
        horizontal_layout.setObjectName("horizontal_layout_volume")

        self.check_box_volume = QtWidgets.QCheckBox(parent=self.verticalLayoutWidget)
        self.check_box_volume.setObjectName("check_box_volume")
        self.check_box_volume.setText("volume")

        horizontal_layout.addWidget(self.check_box_volume)

        self.check_box_volume.stateChanged.connect(self.volume_apply)

        self.double_spin_box_volume = QtWidgets.QDoubleSpinBox(parent=self.verticalLayoutWidget)
        self.double_spin_box_volume.setMinimum(-99.0)
        self.double_spin_box_volume.setMaximum(20.0)
        self.double_spin_box_volume.setObjectName("double_spin_box_speed")

        self.double_spin_box_volume.valueChanged.connect(self.volume_change_event)

        horizontal_layout.addWidget(self.double_spin_box_volume)

        self.grid_layout.addLayout(horizontal_layout, 3, 0, 1, 1)

    def setup_cut_layout(self):
        horizontal_layout = QtWidgets.QHBoxLayout()
        horizontal_layout.setObjectName("horizontal_layout_cut")

        self.check_box_cut = QtWidgets.QCheckBox(parent=self.verticalLayoutWidget)
        self.check_box_cut.setObjectName("check_box_cut")
        self.check_box_cut.setText("cut")

        horizontal_layout.addWidget(self.check_box_cut)

        self.check_box_cut.stateChanged.connect(self.cut_apply)

        label_from = QtWidgets.QLabel(parent=self.verticalLayoutWidget)
        label_from.setObjectName("label_from_cut")
        horizontal_layout.addWidget(label_from)
        label_from.setText("from:")

        self.double_spin_box_from_cut = QtWidgets.QDoubleSpinBox(parent=self.verticalLayoutWidget)
        self.double_spin_box_from_cut.setObjectName("double_spin_box_from_cut")
        horizontal_layout.addWidget(self.double_spin_box_from_cut)

        self.double_spin_box_from_cut.valueChanged.connect(self.cut_from_change_event)

        label_to = QtWidgets.QLabel(parent=self.verticalLayoutWidget)
        label_to.setObjectName("label_to_cut")
        horizontal_layout.addWidget(label_to)
        label_to.setText("to:")

        self.double_spin_box_to_cut = QtWidgets.QDoubleSpinBox(parent=self.verticalLayoutWidget)
        self.double_spin_box_to_cut.setObjectName("double_spin_box_to_cut")
        horizontal_layout.addWidget(self.double_spin_box_to_cut)

        self.double_spin_box_to_cut.valueChanged.connect(self.cut_to_change_event)

        self.grid_layout.addLayout(horizontal_layout, 4, 0, 1, 1)

    def setup_fragment_cut_layout(self):
        horizontal_layout = QtWidgets.QHBoxLayout()
        horizontal_layout.setObjectName("horizontal_layout_fragment")

        self.check_box_fragment = QtWidgets.QCheckBox(parent=self.verticalLayoutWidget)
        self.check_box_fragment.setObjectName("check_box_fragment")
        self.check_box_fragment.setText("fragment cut")

        horizontal_layout.addWidget(self.check_box_fragment)

        self.check_box_fragment.stateChanged.connect(self.fragment_cut_apply)

        label_from = QtWidgets.QLabel(parent=self.verticalLayoutWidget)
        label_from.setObjectName("label_from_fragment")
        horizontal_layout.addWidget(label_from)
        label_from.setText("from:")

        self.double_spin_box_from_fragment = QtWidgets.QDoubleSpinBox(parent=self.verticalLayoutWidget)
        self.double_spin_box_from_fragment.setObjectName("double_spin_box_from_fragment_cut")
        horizontal_layout.addWidget(self.double_spin_box_from_fragment)

        self.double_spin_box_from_fragment.valueChanged.connect(self.fragment_cut_from_change_event)

        label_to = QtWidgets.QLabel(parent=self.verticalLayoutWidget)
        label_to.setObjectName("label_to_fragment")
        horizontal_layout.addWidget(label_to)
        label_to.setText("to:")

        self.double_spin_box_to_fragment = QtWidgets.QDoubleSpinBox(parent=self.verticalLayoutWidget)
        self.double_spin_box_to_fragment.setObjectName("double_spin_box_to_fragment_cut")
        horizontal_layout.addWidget(self.double_spin_box_to_fragment)

        self.double_spin_box_to_fragment.valueChanged.connect(self.fragment_cut_to_change_event)

        self.grid_layout.addLayout(horizontal_layout, 5, 0, 1, 1)

    def setup_append_layout(self):
        horizontal_layout = QtWidgets.QHBoxLayout()
        horizontal_layout.setObjectName("horizontal_layout_append")

        self.check_box_append = QtWidgets.QCheckBox(parent=self.verticalLayoutWidget)
        self.check_box_append.setObjectName("check_box_append")
        self.check_box_append.setText("append")

        horizontal_layout.addWidget(self.check_box_append)

        self.check_box_append.stateChanged.connect(self.append_apply)

        self.line_edit_append = QtWidgets.QLineEdit(parent=self.verticalLayoutWidget)
        self.line_edit_append.setObjectName("line_edit_path_append")
        self.line_edit_append.setReadOnly(True)
        horizontal_layout.addWidget(self.line_edit_append)

        self.push_button_append = QtWidgets.QPushButton(parent=self.verticalLayoutWidget)
        self.push_button_append.setObjectName("push_button_path_append")
        horizontal_layout.addWidget(self.push_button_append)
        self.push_button_append.setText("выбрать файл")

        self.grid_layout.addLayout(horizontal_layout, 6, 0, 1, 1)

    def setup_overlay_layout(self):
        horizontal_layout = QtWidgets.QHBoxLayout()
        horizontal_layout.setObjectName("horizontal_layout_overlay")

        self.check_box_overlay = QtWidgets.QCheckBox(parent=self.verticalLayoutWidget)
        self.check_box_overlay.setObjectName("check_box_overlay")
        self.check_box_overlay.setText("overlay")

        horizontal_layout.addWidget(self.check_box_overlay)

        self.check_box_overlay.stateChanged.connect(self.overlay_apply)

        self.line_edit_overlay = QtWidgets.QLineEdit(parent=self.verticalLayoutWidget)
        self.line_edit_overlay.setObjectName("line_edit_path_overlay")
        self.line_edit_overlay.setReadOnly(True)
        horizontal_layout.addWidget(self.line_edit_overlay)

        self.push_button_overlay = QtWidgets.QPushButton(parent=self.verticalLayoutWidget)
        self.push_button_overlay.setObjectName("push_button_path_overlay")
        horizontal_layout.addWidget(self.push_button_overlay)
        self.push_button_overlay.setText("выбрать файл")

        self.grid_layout.addLayout(horizontal_layout, 7, 0, 1, 1)

    def setup_export_layout(self):
        horizontal_layout = QtWidgets.QHBoxLayout()
        horizontal_layout.setObjectName("horizontal_layout_export")

        button_export = QPushButton(parent=self.verticalLayoutWidget)
        button_export.setText("export")
        horizontal_layout.addWidget(button_export)

        button_export.clicked.connect(self.export)

        self.line_edit_export = QtWidgets.QLineEdit(parent=self.verticalLayoutWidget)
        self.line_edit_export.setObjectName("line_edit_path_export")
        self.line_edit_export.setReadOnly(True)
        horizontal_layout.addWidget(self.line_edit_export)

        self.push_button_export = QtWidgets.QPushButton(parent=self.verticalLayoutWidget)
        self.push_button_export.setObjectName("push_button_path_export")
        horizontal_layout.addWidget(self.push_button_export)
        self.push_button_export.setText("папка для сохранения")

        self.grid_layout.addLayout(horizontal_layout, 8, 0, 1, 1)

    def history_update(self):
        self.history_text.setPlainText(history_handler.get_text())

    def setup_history(self):
        self.history_text = QtWidgets.QPlainTextEdit(parent=self.central_widget)
        self.history_text.setGeometry(QtCore.QRect(0, 0, 500, 600))
        self.history_text.setObjectName("history_text")
        self.history_update()
        self.history_text.setReadOnly(True)
