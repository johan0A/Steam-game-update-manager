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
        self.cdnclient = steam.client.cdn.CDNClient(self.steamclient)
        self.is_anonymous_loged_in = False
        self.is_logged_in = False
    
    def anonymous_login(self):
        self.steamclient.anonymous_login()
        if self.steamclient.logged_on:
            self.is_anonymous_loged_in = True
            return True
    
    def get_app_depot_info(self, appID):
        return self.cdnclient.get_app_depot_info(appID)


class User_library():
    def __init__(self):
        self.steamapps_path = None
        self.app_list = []
        self.steamclient = Steam_client()
    
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

class App():
    def __init__(self, appmanifest_path, parent_library=None):
        self.appmanifest_path = appmanifest_path
        self.app_name: str = None
        self.app_id: int = None
        self.app_update_status = None
        self.app_manifestID = None
        self.app_manifest = None
        self.parent_library: User_library = parent_library
        
        self.load_app()
        
    def load_app(self):
        with open(self.appmanifest_path, 'r', encoding='utf-8') as f:
            data = vdf.load(f)
            self.app_name = data.get("AppState", {}).get("name", "Unknown")
            self.app_id = int(data.get("AppState", {}).get("appid", "Unknown"))
            self.app_manifestID = data.get("AppState", {}).get("manifest", "Unknown")
            self.app_manifest = data
            self.app_state = data.get("AppState", {}).get("StateFlags", "Unknown")
            
            possible_states = {
                '4': {'color': 'green', 'text': 'Has no updates'},
                '6': {'color': 'red', 'text': 'Has an update'},
            }
            self.app_update_status = possible_states.get(self.app_state, {'color': 'yellow', 'text': 'Other'})

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
    
    def debug_save_depot_info_as_json(self):
        root = tk.Tk()
        root.withdraw()
        self.create_debug_folder()
        file_path = filedialog.asksaveasfilename(defaultextension=".json", filetypes=[("JSON", "*.json")], initialfile=f"{self.app_name}_depot_info.json", initialdir="debug")
        root.destroy()
        if file_path is None:
            return False
        if file_path:
            with open(file_path, 'w', encoding='utf-8') as f:
                json.dump(self.get_depot_info(), f, indent=4)
        return True
    
    def debug_save_manifest_for_newest_app_version_as_json(self):
        root = tk.Tk()
        root.withdraw()
        self.create_debug_folder()
        file_path = filedialog.asksaveasfilename(defaultextension=".json", filetypes=[("JSON", "*.json")], initialfile=f"{self.app_name}_manifest.json", initialdir="debug")
        root.destroy()
        if file_path is None:
            return False
        if file_path:
            with open(file_path, 'w', encoding='utf-8') as f:
                json.dump(self.get_manifest_for_newest_app_version(), f, indent=4)
        return True

    def get_manifestID_for_newest_app_version(self):
        depot_info = self.get_depot_info()
        return depot_info[self.app_id]["branches"]["public"]["buildid"]
    
    def get_depotID_of_app(self):
        return list(self.app_manifest["AppState"]["InstalledDepots"].keys())[0]
    
    def get_manifest_for_newest_app_version(self):
        depotID = self.get_depotID_of_app()
        manifestID = self.get_manifestID_for_newest_app_version()
        manifest = self.parent_library.steamclient.cdnclient.get_app_manifest(self.app_id, depotID, manifestID)
        return vdf.loads(manifest.data)
    
    def get_depot_info(self):
        return self.parent_library.steamclient.get_app_depot_info(self.app_id)