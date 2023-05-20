from PyQt6 import QtWidgets, QtCore

from history import history_handler


def history_update(history_text: QtWidgets.QPlainTextEdit):
    history_text.setPlainText(history_handler.get_text())

    return history_text


def setup_history_layout(central_widget: QtWidgets.QWidget):
    history_text = QtWidgets.QPlainTextEdit(parent=central_widget)
    history_text.setGeometry(QtCore.QRect(0, 0, 400, 600))
    history_text.setObjectName("history_text")
    history_text = history_update(history_text)
    history_text.setReadOnly(True)

    return history_text
