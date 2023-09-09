import steam.monkey
steam.monkey.patch_minimal()

import requests
from steam.client import SteamClient, EMsg


import os
import winreg
import vdf
import sys
from PyQt5.QtWidgets import QApplication, QWidget, QLabel, QLineEdit, QPushButton, QVBoxLayout, QMessageBox, QComboBox, QHBoxLayout
import logging
import json

import steam.client
import steam.client.cdn

logging.basicConfig(format='[%(asctime)s] %(levelname)s %(name)s: %(message)s', level=logging.DEBUG)

def find_steamapps():
    paths_to_check = [
        os.path.join("C:", "Program Files (x86)", "Steam", "steamapps"),
        os.path.join("C:", "Program Files", "Steam", "steamapps"),
    ]

    for path in paths_to_check:
        if os.path.exists(path):
            return path

    # Try to retrieve the Steam installation path from the registry
    try:
        registry_key = winreg.OpenKey(winreg.HKEY_LOCAL_MACHINE, r"SOFTWARE\WOW6432Node\Valve\Steam")
        steam_path, _ = winreg.QueryValueEx(registry_key, "InstallPath")
        winreg.CloseKey(registry_key)

        potential_path = os.path.join(steam_path, "steamapps")
        if os.path.exists(potential_path):
            return potential_path

    except (WindowsError, FileNotFoundError):
        pass

    return None

def find_appmanifest_files(directory):
    return [os.path.join(directory, file) for file in os.listdir(directory) if "appmanifest" in file and os.path.isfile(os.path.join(directory, file))]

def load_files_as_vdf(filepaths):
    games_dict = {}

    for filepath in filepaths:
        with open(filepath, 'r', encoding='utf-8') as f:
            data = vdf.load(f)
            game_name = data.get("AppState", {}).get("name", "Unknown") 
            games_dict[game_name] = data

    return games_dict

def get_app_last_manifestID(appID, depotID, cdnclient):
    
    depot_info = cdnclient.get_app_depot_info(appID)
    
    manifestID = depot_info[depotID]['manifests']['public']['gid']
    
    return manifestID

def list_games(steamapps_directory):
    files = find_appmanifest_files(steamapps_directory)
    vdf_contents = load_files_as_vdf(files)
    games = [{"name": i[0], "state": i[1]["AppState"]["StateFlags"]} for i in vdf_contents.items()]
    
    return games

def skip_update(steamapps_directory, game_name, cdnclient):
    files = find_appmanifest_files(steamapps_directory)
    vdf_contents = load_files_as_vdf(files)
    
    game_manifest = vdf_contents[game_name]
    
    appID = int(game_manifest["AppState"]["appid"])
    depotID = list(game_manifest["AppState"]["InstalledDepots"].keys())[0]
    
    print("sending request for newest manifestID")
    last_manifestID = get_app_last_manifestID(appID, depotID, cdnclient)
    print(last_manifestID)

    game_manifest["AppState"]["InstalledDepots"][depotID]["manifest"] = last_manifestID
    game_manifest["AppState"]["StateFlags"] = "4"
    
    # save modified game manifest with indentation
    indented_string = json.dumps(game_manifest, indent=4)
    indented_string = indented_string[1:-1].strip()
    vdf_string = indented_string.replace(': ', ' ').replace('"{', '{').replace('}"', '}').replace('"', '\"').replace(',', '')

    with open(os.path.join(steamapps_directory, f'appmanifest_{appID}.acf'), 'w', encoding='utf-8') as f:
        f.write(vdf_string)

class SkipUpdateApp(QWidget):
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


def main():
    app = QApplication(sys.argv)
    window = SkipUpdateApp()
    
    window.show()
    sys.exit(app.exec_())


if __name__ == '__main__':
    main()

