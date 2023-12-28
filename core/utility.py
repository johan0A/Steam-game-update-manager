import os
import winreg
import vdf

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
    return [os.path.join(directory, file) for file in os.listdir(directory) if "appmanifest" in file and os.path.isfile(os.path.join(directory, file))]

class App():
    def __init__(self, appmanifest_path):
        self.appmanifest_path = appmanifest_path
        self.app_name = None
        self.app_id = None
        self.app_state = None
        self.app_depot = None
        self.app_manifestID = None
        self.app_manifest = None
        
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
            self.app_list.append(App(path))