import os
import winreg
import vdf
import json
import time

import tkinter as tk
from tkinter import filedialog

import steam.client
import steam.client.cdn


def find_steamapps_path():
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
    """Returns a list of paths to appmanifest files in the given directory."""
    return [os.path.join(directory, file) for file in os.listdir(directory) if "appmanifest" in file and os.path.isfile(os.path.join(directory, file))]

class Steam_client():
    def __init__(self):
        self.steamclient = steam.client.SteamClient()
        self.steamclient.anonymous_login()
        self.cdnclient = steam.client.cdn.CDNClient(self.steamclient)
    
    def aninymous_login(self):
        self.steamclient.anonymous_login()
    
    def get_app_depot_info(self, appID):
        return self.cdnclient.get_app_depot_info(appID)

class App():
    def __init__(self, appmanifest_path, parent_library=None):
        self.appmanifest_path = appmanifest_path
        self.app_name = None
        self.app_id = None
        self.app_state = None
        self.app_depot = None
        self.app_manifestID = None
        self.app_manifest = None
        self.parent_library = None
        
        self.load_app()
        
    def load_app(self):
        with open(self.appmanifest_path, 'r', encoding='utf-8') as f:
            data = vdf.load(f)
            self.app_name = data.get("AppState", {}).get("name", "Unknown")
            self.app_id = data.get("AppState", {}).get("appid", "Unknown")
            self.app_state = data.get("AppState", {}).get("StateFlags", "Unknown")
            self.app_depot = data.get("AppState", {}).get("depots", "Unknown")
            self.app_manifestID = data.get("AppState", {}).get("manifest", "Unknown")
            self.app_manifest = data
    
    def save_app_manifest(self):
        with open(self.appmanifest_path, 'w', encoding='utf-8') as f:
            vdf.dump(self.app_manifest, f, pretty=True)
    
    def create_debug_folder(self):
        if not os.path.exists("debug"):
            os.mkdir("debug")

    def debug_save_original_app_manifest_as_json(self):
        root = tk.Tk()
        root.withdraw()
        self.create_debug_folder()
        file_path = filedialog.asksaveasfilename(defaultextension=".json", filetypes=[("JSON", "*.json")], initialfile=f"{self.app_name}_original.json", initialdir="debug")
        root.destroy()
        if file_path is None:
            return False
        if file_path:
            with open(file_path, 'w', encoding='utf-8') as f:
                json.dump(self.app_manifest, f, indent=4)
        return True
    
    def debug_save_app_manifest_as_json(self):
        root = tk.Tk()
        root.withdraw()
        self.create_debug_folder()
        file_path = filedialog.asksaveasfilename(defaultextension=".json", filetypes=[("JSON", "*.json")], initialfile=f"{self.app_name}_modified.json", initialdir="debug")
        root.destroy()
        if file_path is None:
            return False
        if file_path:
            with open(file_path, 'w', encoding='utf-8') as f:
                json.dump(self.app_manifest, f, indent=4)
        return True
            
    def __repr__(self):
        return f"App({self.app_name}, {self.app_id}, {self.app_state}, {self.app_depot}, {self.app_manifestID})"
    
    def __str__(self):
        return f"App({self.app_name}, {self.app_id}, {self.app_state}, {self.app_depot}, {self.app_manifestID})"
    
    def __eq__(self, other):
        return self.app_name == other.app_name and self.app_id == other.app_id and self.app_state == other.app_state and self.app_depot == other.app_depot and self.app_manifestID == other.app_manifestID
    
    def __hash__(self):
        return hash((self.app_name, self.app_id, self.app_state, self.app_depot, self.app_manifestID))
    
    def __lt__(self, other):
        return

class User_library():
    def __init__(self):
        self.steamapps_path = None
        self.app_list = []
    
    def get_steamapps_path(self):
        steampath = find_steamapps_path()
        if steampath is not None:
            self.steamapps_path = steampath
            return True
        else:
            return False

    def gather_library(self):
        appManifestPaths = find_appmanifest_files(self.steamapps_path)
        for path in appManifestPaths:
            self.app_list.append(App(path, parent_library=self))