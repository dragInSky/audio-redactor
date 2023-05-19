from PyQt6 import QtCore, QtWidgets
from operations_history import history_handler


class UiMainWindow(object):
    def setup_ui(self, main_window):
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
        self.setup_speed_layout()
        self.setup_fragment_cut_layout()
        self.setup_volume_layout()
        self.setup_cut_layout()
        self.setup_append_layout()
        self.setup_overlay_layout()
        self.setup_export_layout()
        self.setup_reverse()
        self.setup_history()

        main_window.setCentralWidget(self.central_widget)

        main_window.setWindowTitle("audio redactor")
        QtCore.QMetaObject.connectSlotsByName(main_window)

    def setup_import_layout(self):
        self.horizontal_layout_import = QtWidgets.QHBoxLayout()
        self.horizontal_layout_import.setObjectName("horizontal_layout_import")

        self.label_import = QtWidgets.QLabel(parent=self.verticalLayoutWidget)
        self.label_import.setObjectName("label_import")
        self.horizontal_layout_import.addWidget(self.label_import)
        self.label_import.setText("import")

        self.line_edit_choose_import_file = QtWidgets.QLineEdit(parent=self.verticalLayoutWidget)
        self.line_edit_choose_import_file.setObjectName("line_edit_choose_import_file")
        self.line_edit_choose_import_file.setReadOnly(True)
        self.horizontal_layout_import.addWidget(self.line_edit_choose_import_file)

        self.push_button_choose_import_file = QtWidgets.QPushButton(parent=self.verticalLayoutWidget)
        self.push_button_choose_import_file.setObjectName("push_button_choose_import_file")
        self.horizontal_layout_import.addWidget(self.push_button_choose_import_file)
        self.push_button_choose_import_file.setText("выбрать файл")

        self.grid_layout.addLayout(self.horizontal_layout_import, 0, 0, 1, 1)

    def setup_speed_layout(self):
        self.horizontal_layout_speed = QtWidgets.QHBoxLayout()
        self.horizontal_layout_speed.setObjectName("horizontal_layout_speed")

        self.label_speed = QtWidgets.QLabel(parent=self.verticalLayoutWidget)
        self.label_speed.setObjectName("label_speed")
        self.horizontal_layout_speed.addWidget(self.label_speed)
        self.label_speed.setText("speed")

        self.double_spin_box_speed = QtWidgets.QDoubleSpinBox(parent=self.verticalLayoutWidget)
        self.double_spin_box_speed.setMinimum(0.1)
        self.double_spin_box_speed.setMaximum(10.0)
        self.double_spin_box_speed.setObjectName("double_spin_box_speed")
        self.horizontal_layout_speed.addWidget(self.double_spin_box_speed)

        self.grid_layout.addLayout(self.horizontal_layout_speed, 2, 0, 1, 1)

    def setup_fragment_cut_layout(self):
        self.horizontal_layout_fragment_cut = QtWidgets.QHBoxLayout()
        self.horizontal_layout_fragment_cut.setObjectName("horizontal_layout_fragment_cut")

        self.label_fragment_cut = QtWidgets.QLabel(parent=self.verticalLayoutWidget)
        self.label_fragment_cut.setObjectName("label_fragment_cut")
        self.horizontal_layout_fragment_cut.addWidget(self.label_fragment_cut)
        self.label_fragment_cut.setText("fragment cut")

        self.label_fragment_from = QtWidgets.QLabel(parent=self.verticalLayoutWidget)
        self.label_fragment_from.setObjectName("label_fragment_from")
        self.horizontal_layout_fragment_cut.addWidget(self.label_fragment_from)
        self.label_fragment_from.setText("from:")

        self.double_spin_box_fragment_from = QtWidgets.QDoubleSpinBox(parent=self.verticalLayoutWidget)
        self.double_spin_box_fragment_from.setObjectName("double_spin_box_fragment_from")
        self.horizontal_layout_fragment_cut.addWidget(self.double_spin_box_fragment_from)

        self.label_fragment_to = QtWidgets.QLabel(parent=self.verticalLayoutWidget)
        self.label_fragment_to.setObjectName("label_fragment_to")
        self.horizontal_layout_fragment_cut.addWidget(self.label_fragment_to)
        self.label_fragment_to.setText("to:")

        self.double_spin_box_fragment_to = QtWidgets.QDoubleSpinBox(parent=self.verticalLayoutWidget)
        self.double_spin_box_fragment_to.setObjectName("double_spin_box_fragment_to")
        self.horizontal_layout_fragment_cut.addWidget(self.double_spin_box_fragment_to)

        self.grid_layout.addLayout(self.horizontal_layout_fragment_cut, 5, 0, 1, 1)

    def setup_volume_layout(self):
        self.horizontal_layout_volume = QtWidgets.QHBoxLayout()
        self.horizontal_layout_volume.setObjectName("horizontal_layout_volume")

        self.label_volume = QtWidgets.QLabel(parent=self.verticalLayoutWidget)
        self.label_volume.setObjectName("label_volume")
        self.horizontal_layout_volume.addWidget(self.label_volume)
        self.label_volume.setText("volume")

        self.double_spin_box_volume = QtWidgets.QDoubleSpinBox(parent=self.verticalLayoutWidget)
        self.double_spin_box_volume.setMinimum(-99.0)
        self.double_spin_box_volume.setMaximum(20.0)
        self.double_spin_box_volume.setObjectName("double_spin_box_volume")
        self.horizontal_layout_volume.addWidget(self.double_spin_box_volume)

        self.grid_layout.addLayout(self.horizontal_layout_volume, 3, 0, 1, 1)

    def setup_cut_layout(self):
        self.horizontal_layout_cut = QtWidgets.QHBoxLayout()
        self.horizontal_layout_cut.setObjectName("horizontal_layout_cut")

        self.label_cut = QtWidgets.QLabel(parent=self.verticalLayoutWidget)
        self.label_cut.setObjectName("label_cut")
        self.horizontal_layout_cut.addWidget(self.label_cut)
        self.label_cut.setText("cut")

        self.label_from = QtWidgets.QLabel(parent=self.verticalLayoutWidget)
        self.label_from.setObjectName("label_from")
        self.horizontal_layout_cut.addWidget(self.label_from)
        self.label_from.setText("from:")

        self.double_spin_box_from = QtWidgets.QDoubleSpinBox(parent=self.verticalLayoutWidget)
        self.double_spin_box_from.setObjectName("double_spin_box_from")
        self.horizontal_layout_cut.addWidget(self.double_spin_box_from)

        self.label_to = QtWidgets.QLabel(parent=self.verticalLayoutWidget)
        self.label_to.setObjectName("label_to")
        self.horizontal_layout_cut.addWidget(self.label_to)
        self.label_to.setText("to:")

        self.double_spin_box_to = QtWidgets.QDoubleSpinBox(parent=self.verticalLayoutWidget)
        self.double_spin_box_to.setObjectName("double_spin_box_to")
        self.horizontal_layout_cut.addWidget(self.double_spin_box_to)

        self.grid_layout.addLayout(self.horizontal_layout_cut, 4, 0, 1, 1)

    def setup_append_layout(self):
        self.horizontal_layout_append = QtWidgets.QHBoxLayout()
        self.horizontal_layout_append.setObjectName("horizontal_layout_append")

        self.label_append = QtWidgets.QLabel(parent=self.verticalLayoutWidget)
        self.label_append.setObjectName("label_append")
        self.horizontal_layout_append.addWidget(self.label_append)
        self.label_append.setText("append")

        self.line_edit_choose_append_file = QtWidgets.QLineEdit(parent=self.verticalLayoutWidget)
        self.line_edit_choose_append_file.setObjectName("line_edit_choose_append_file")
        self.line_edit_choose_append_file.setReadOnly(True)
        self.horizontal_layout_append.addWidget(self.line_edit_choose_append_file)

        self.push_button_choose_append_file = QtWidgets.QPushButton(parent=self.verticalLayoutWidget)
        self.push_button_choose_append_file.setObjectName("push_button_choose_append_file")
        self.horizontal_layout_append.addWidget(self.push_button_choose_append_file)
        self.push_button_choose_append_file.setText("выбрать файл")

        self.grid_layout.addLayout(self.horizontal_layout_append, 6, 0, 1, 1)

    def setup_overlay_layout(self):
        self.horizontal_layout_overlay = QtWidgets.QHBoxLayout()
        self.horizontal_layout_overlay.setObjectName("horizontal_layout_overlay")

        self.label_overlay = QtWidgets.QLabel(parent=self.verticalLayoutWidget)
        self.label_overlay.setObjectName("label_overlay")
        self.horizontal_layout_overlay.addWidget(self.label_overlay)
        self.label_overlay.setText("overlay")

        self.line_edit_choose_overlay_file = QtWidgets.QLineEdit(parent=self.verticalLayoutWidget)
        self.line_edit_choose_overlay_file.setObjectName("line_edit_choose_overlay_file")
        self.line_edit_choose_overlay_file.setReadOnly(True)
        self.horizontal_layout_overlay.addWidget(self.line_edit_choose_overlay_file)

        self.push_button_choose_overlay_file = QtWidgets.QPushButton(parent=self.verticalLayoutWidget)
        self.push_button_choose_overlay_file.setObjectName("push_button_choose_overlay_file")
        self.horizontal_layout_overlay.addWidget(self.push_button_choose_overlay_file)
        self.push_button_choose_overlay_file.setText("выбрать файл")

        self.grid_layout.addLayout(self.horizontal_layout_overlay, 7, 0, 1, 1)

    def setup_export_layout(self):
        self.horizontal_layout_export = QtWidgets.QHBoxLayout()
        self.horizontal_layout_export.setObjectName("horizontal_layout_export")

        self.label_export = QtWidgets.QLabel(parent=self.verticalLayoutWidget)
        self.label_export.setObjectName("label_export")
        self.horizontal_layout_export.addWidget(self.label_export)
        self.label_export.setText("export")

        self.line_edit_save_path = QtWidgets.QLineEdit(parent=self.verticalLayoutWidget)
        self.line_edit_save_path.setObjectName("line_edit_save_path")
        self.line_edit_save_path.setReadOnly(True)
        self.horizontal_layout_export.addWidget(self.line_edit_save_path)

        self.push_button_save_path = QtWidgets.QPushButton(parent=self.verticalLayoutWidget)
        self.push_button_save_path.setObjectName("push_button_save_path")
        self.horizontal_layout_export.addWidget(self.push_button_save_path)
        self.push_button_save_path.setText("папка для сохранения")

        self.grid_layout.addLayout(self.horizontal_layout_export, 8, 0, 1, 1)

    def setup_reverse(self):
        self.check_box_reverse = QtWidgets.QCheckBox(parent=self.verticalLayoutWidget)
        self.check_box_reverse.setObjectName("check_box_reverse")
        self.check_box_reverse.setText("reverse")

        self.grid_layout.addWidget(self.check_box_reverse, 1, 0, 1, 1)

    def setup_history(self):
        self.history_text = QtWidgets.QPlainTextEdit(parent=self.central_widget)
        self.history_text.setGeometry(QtCore.QRect(0, 0, 500, 600))
        self.history_text.setObjectName("history_text")
        self.history_text.setPlainText(history_handler.get_text())
        self.history_text.setReadOnly(True)
