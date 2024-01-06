from PyQt5.QtWidgets import QApplication, QWidget, QLabel, QLineEdit, QPushButton, QVBoxLayout, QMessageBox, QComboBox, QHBoxLayout, QGridLayout, QCheckBox
from PyQt5.QtGui import QFont
from PyQt5.QtCore import Qt
from core.utility import App

class App_state_editor(QWidget):
    def __init__(self, app: App, parent=None):
        super(App_state_editor, self).__init__(parent)
        self.app = app
        self.debug_menu = QWidget()
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

        debug_toggle_checkbox = QCheckBox("Debug: Toggle")
        debug_toggle_checkbox.stateChanged.connect(self.toggle_debug)
        layout.addWidget(debug_toggle_checkbox)

        debug_menu_layout = QVBoxLayout()

        new_button = QPushButton("Debug: Save original app manifest as JSON", self)
        new_button.clicked.connect(self.app.debug_save_original_app_manifest_as_json)
        debug_menu_layout.addWidget(new_button)

        new_button = QPushButton("Debug: Save app manifest as JSON", self)
        new_button.clicked.connect(self.app.debug_save_app_manifest_as_json)
        debug_menu_layout.addWidget(new_button)
        
        new_button = QPushButton("Debug: Save depot info as JSON", self)
        new_button.clicked.connect(self.app.debug_save_depot_info_as_json)
        debug_menu_layout.addWidget(new_button)
        
        self.debug_menu.setLayout(debug_menu_layout)
        self.debug_menu.hide()

        layout.addWidget(self.debug_menu)
        
        self.setLayout(layout)
        self.setWindowTitle('app state editor; app: ' + self.app.app_name)

        self.update_display()

    def toggle_debug(self):
        if self.debug_menu.isVisible():
            self.debug_menu.hide()
        else:
            self.debug_menu.show()
        self.update_display()
    
    def update_display(self):
        # make the window the minimum size it can be without cutting off any text
        self.adjustSize()