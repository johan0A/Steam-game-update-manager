from PyQt5.QtWidgets import QApplication, QWidget, QLabel, QLineEdit, QPushButton, QVBoxLayout, QMessageBox, QComboBox, QHBoxLayout
from core.utility import User_library
import sys

class Main_window(QWidget):
    def __init__(self, parent=None):
        super(Main_window, self).__init__(parent)
        self.user_library = User_library()
        self.user_library.get_steamapps_path()
        self.user_library.gather_library()

        self.initUI()

    def initUI(self):
        layout = QVBoxLayout()

        self.search_bar = QLineEdit(self)
        self.search_bar.setPlaceholderText("Search for games...")
        self.search_bar.textChanged.connect(self.update_display)

        layout.addWidget(self.search_bar)

        self.game_widgets = []

        for i in range(15):
            game_layout = QHBoxLayout()
            
            game_label = QLabel(self)
            skip_button = QPushButton("Skip Update", self)
            # skip_button.clicked.connect(self.make_skip_update_handler(game_label.text()))

            game_layout.addWidget(game_label)
            game_layout.addWidget(skip_button)

            layout.addLayout(game_layout)
            self.game_widgets.append((game_label, skip_button))

        self.setLayout(layout)
        self.setWindowTitle('Steam Skip Update')
        self.resize(600, 500)

        self.update_display()

    # def make_skip_update_handler(self, game_name):
    #     def handler():
    #         try:
    #             skip_update(self.steamapps_directory, game_name, self.cdnclient)
    #             QMessageBox.information(self, "Success", f"Update skipped for {game_name}!")
    #             self.update_display()
    #         except Exception as e:
    #             QMessageBox.critical(self, "Error", str(e))

    #     return handler

    def update_display(self):
        search_query = self.search_bar.text().lower()
        
        apps = self.user_library.app_list.copy()
    
        if search_query:
            apps = [app for app in apps if search_query in app.app_name.lower()]

        for app_label, skip_button in self.game_widgets:
            try:
                app = apps.pop(0)
                app_name = app.app_name
                # state_flags = game["state"]
                
                # color_map = {
                #     '4': ('green', 'Has no updates'),
                #     '6': ('red', 'Has an update')
                # }
                # color, state_msg = color_map.get(state_flags, ('yellow', 'Other'))

                # game_label.setText(f"{game_name} - {state_msg}")
                app_label.setText(f"{app_name}")
                # game_label.setStyleSheet(f"color: {color}")
                
                skip_button.show()
                # skip_button.clicked.disconnect()
                # skip_button.clicked.connect(self.make_skip_update_handler(app_name))

            except IndexError:
                app_label.clear()
                skip_button.hide()

