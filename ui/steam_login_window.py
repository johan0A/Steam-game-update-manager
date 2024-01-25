from PyQt5.QtWidgets import QApplication, QWidget, QLabel, QLineEdit, QPushButton, QVBoxLayout, QMessageBox, QComboBox, QHBoxLayout, QGridLayout, QCheckBox
from PyQt5.QtGui import QFont
from PyQt5.QtCore import Qt
from core.utility import App

from core.utility import User_library
from ui.app_state_editor_window import App_state_editor

class Steam_login_window(QWidget):
    def __init__(self, user_library: User_library, parent=None):
        super(Steam_login_window, self).__init__(parent)
        self.user_library = user_library
        self.initUI()

    def initUI(self):
        layout = QVBoxLayout()

        login_status_label = QLabel('Login Status: ' + str(self.user_library.steamclient.is_logged_in))
        login_status_label.setAlignment(Qt.AlignCenter)
        layout.addWidget(login_status_label)

        self.setLayout(layout)

        self.update_display()


    def update_display(self):
        pass
