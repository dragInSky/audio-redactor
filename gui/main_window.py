from PyQt6 import QtCore, QtWidgets
from history import history_handler
from audio import audio_redactor


class UiMainWindow:

    def setup_ui(self, main_window):
        self.audio_redactor = audio_redactor.AudioRedactor()

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
        self.audio_redactor.change_speed(value)
        self.history_update()

    def volume_change_event(self, value: float):
        self.audio_redactor.change_volume(value)
        self.history_update()

    def setup_import_layout(self):
        horizontal_layout = self.layout_label_pattern("import")

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
        horizontal_layout = self.layout_label_pattern("speed")

        self.double_spin_box_speed = QtWidgets.QDoubleSpinBox(parent=self.verticalLayoutWidget)
        self.double_spin_box_speed.setMinimum(0.1)
        self.double_spin_box_speed.setMaximum(10.0)
        self.double_spin_box_speed.setObjectName("double_spin_box_speed")

        self.double_spin_box_speed.valueChanged.connect(self.speed_change_event)

        horizontal_layout.addWidget(self.double_spin_box_speed)

        self.grid_layout.addLayout(horizontal_layout, 2, 0, 1, 1)

    def setup_volume_layout(self):
        horizontal_layout = self.layout_label_pattern("volume")

        self.double_spin_box_volume = QtWidgets.QDoubleSpinBox(parent=self.verticalLayoutWidget)
        self.double_spin_box_volume.setMinimum(-99.0)
        self.double_spin_box_volume.setMaximum(20.0)
        self.double_spin_box_volume.setObjectName("double_spin_box_speed")

        self.double_spin_box_volume.valueChanged.connect(self.volume_change_event)

        horizontal_layout.addWidget(self.double_spin_box_volume)

        self.grid_layout.addLayout(horizontal_layout, 3, 0, 1, 1)

    def setup_cut_layout(self):
        horizontal_layout = self.cut_pattern("cut")

        self.double_spin_box_from_cut = QtWidgets.QDoubleSpinBox(parent=self.verticalLayoutWidget)
        self.double_spin_box_from_cut.setObjectName("double_spin_box_from_cut")
        horizontal_layout.addWidget(self.double_spin_box_from_cut)

        self.double_spin_box_to_cut = QtWidgets.QDoubleSpinBox(parent=self.verticalLayoutWidget)
        self.double_spin_box_to_cut.setObjectName("double_spin_box_to_cut")
        horizontal_layout.addWidget(self.double_spin_box_to_cut)

        self.grid_layout.addLayout(horizontal_layout, 4, 0, 1, 1)

    def setup_fragment_cut_layout(self):
        horizontal_layout = self.cut_pattern("fragment_cut")

        self.double_spin_box_from_fragment = QtWidgets.QDoubleSpinBox(parent=self.verticalLayoutWidget)
        self.double_spin_box_from_fragment.setObjectName("double_spin_box_from_fragment_cut")
        horizontal_layout.addWidget(self.double_spin_box_from_fragment)

        self.double_spin_box_to_fragment = QtWidgets.QDoubleSpinBox(parent=self.verticalLayoutWidget)
        self.double_spin_box_to_fragment.setObjectName("double_spin_box_to_fragment_cut")
        horizontal_layout.addWidget(self.double_spin_box_to_fragment)

        self.grid_layout.addLayout(horizontal_layout, 5, 0, 1, 1)

    def setup_append_layout(self):
        horizontal_layout = self.layout_label_pattern("append")

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
        horizontal_layout = self.layout_label_pattern("overlay")

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
        horizontal_layout = self.layout_label_pattern("export")

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

    def cut_pattern(self, name: str) -> QtWidgets.QHBoxLayout:
        horizontal_layout = self.layout_label_pattern(name)

        label_from = QtWidgets.QLabel(parent=self.verticalLayoutWidget)
        label_from.setObjectName("label_from_" + name)
        horizontal_layout.addWidget(label_from)
        label_from.setText("from:")

        label_to = QtWidgets.QLabel(parent=self.verticalLayoutWidget)
        label_to.setObjectName("label_to_" + name)
        horizontal_layout.addWidget(label_to)
        label_to.setText("to:")

        return horizontal_layout

    def layout_label_pattern(self, name: str) -> QtWidgets.QHBoxLayout:
        horizontal_layout = QtWidgets.QHBoxLayout()
        horizontal_layout.setObjectName("horizontal_layout_" + name)

        label = QtWidgets.QLabel(parent=self.verticalLayoutWidget)
        label.setObjectName("label_" + name)
        horizontal_layout.addWidget(label)
        label.setText(name)

        return horizontal_layout
