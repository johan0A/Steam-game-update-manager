from PyQt5.QtWidgets import QApplication, QWidget, QLabel, QLineEdit, QPushButton, QVBoxLayout, QMessageBox, QComboBox, QHBoxLayout

class Main_window(QWidget):
    def __init__(self, parent=None):
        super(SkipUpdateApp, self).__init__(parent)
        
        self.steamapps_directory = find_steamapps()
        self.steamclient = steam.client.SteamClient()
        self.steamclient.anonymous_login()
        self.cdnclient = steam.client.cdn.CDNClient(self.steamclient)
        
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
            skip_button.clicked.connect(self.make_skip_update_handler(game_label.text()))

            game_layout.addWidget(game_label)
            game_layout.addWidget(skip_button)

            layout.addLayout(game_layout)
            self.game_widgets.append((game_label, skip_button))

        self.setLayout(layout)
        self.setWindowTitle('Steam Skip Update')
        self.resize(600, 500)

        self.update_display()

    def make_skip_update_handler(self, game_name):
        def handler():
            try:
                skip_update(self.steamapps_directory, game_name, self.cdnclient)
                QMessageBox.information(self, "Success", f"Update skipped for {game_name}!")
                self.update_display()
            except Exception as e:
                QMessageBox.critical(self, "Error", str(e))

        return handler

    def update_display(self):
        search_query = self.search_bar.text().lower()
        
        games = list_games(self.steamapps_directory)
        
        if search_query:
            games = [game for game in games if search_query in game["name"].lower()]

        for game_label, skip_button in self.game_widgets:
            try:
                game = games.pop(0)
                game_name = game["name"]
                state_flags = game["state"]
                
                color_map = {
                    '4': ('green', 'Has no updates'),
                    '6': ('red', 'Has an update')
                }
                color, state_msg = color_map.get(state_flags, ('yellow', 'Other'))

                game_label.setText(f"{game_name} - {state_msg}")
                game_label.setStyleSheet(f"color: {color}")
                
                skip_button.show()
                skip_button.clicked.disconnect()
                skip_button.clicked.connect(self.make_skip_update_handler(game_name))

            except IndexError:
                game_label.clear()
                skip_button.hide()