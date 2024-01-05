from PyQt5.QtWidgets import QApplication, QWidget, QLabel, QLineEdit, QPushButton, QVBoxLayout, QMessageBox, QComboBox, QHBoxLayout, QGridLayout
from PyQt5.QtGui import QFont
from PyQt5.QtCore import Qt
from core.utility import App

class App_state_editor(QWidget):
    def __init__(self, app: App, parent=None):
        super(App_state_editor, self).__init__(parent)
        self.app = app
        self.initUI()

    def initUI(self):
        layout = QVBoxLayout()

        title_label = QLabel('App Title: ' + self.app.app_name)
        id_label = QLabel('App ID: ' + str(self.app.app_id))

        font = QFont()
        font.setFamily('Comic Sans MS')
        font.setBold(True)
        font.setPointSize(14)
        title_label.setFont(font)
        id_label.setFont(font)

        title_label.setAlignment(Qt.AlignCenter)
        id_label.setAlignment(Qt.AlignCenter)

        layout.addWidget(title_label)
        layout.addWidget(id_label)

        debug_save_original_app_manifest_as_json_button = QPushButton("Debug: Save original app manifest as JSON", self)
        debug_save_original_app_manifest_as_json_button.clicked.connect(self.app.debug_save_original_app_manifest_as_json)
        layout.addWidget(debug_save_original_app_manifest_as_json_button)

        debug_save_app_manifest_as_json_button = QPushButton("Debug: Save app manifest as JSON", self)
        debug_save_app_manifest_as_json_button.clicked.connect(self.app.debug_save_app_manifest_as_json)
        layout.addWidget(debug_save_app_manifest_as_json_button)

        self.setLayout(layout)
        self.setWindowTitle('app state editor; app: ' + self.app.app_name)

        self.geometry().center()

        self.update_display()

    def update_display(self):
        pass