from PyQt5.QtWidgets import QApplication, QWidget, QLabel, QLineEdit, QPushButton, QVBoxLayout, QMessageBox, QComboBox, QHBoxLayout, QGridLayout, QCheckBox
from PyQt5.QtGui import QFont
from PyQt5.QtCore import Qt
from core.utility import App

class Steam_login_window(QWidget):
    def __init__(self, app: App, parent=None):
        super(Steam_login_window, self).__init__(parent)
        self.initUI()

    def initUI(self):
        pass