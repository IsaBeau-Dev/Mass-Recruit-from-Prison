import os
import json
import winreg

def get_steam_workshop_path():
    try:
        reg_key = winreg.OpenKey(winreg.HKEY_CURRENT_USER, r"SOFTWARE\Valve\Steam")
        steam_path, _ = winreg.QueryValueEx(reg_key, "SteamPath")
        winreg.CloseKey(reg_key)
        return os.path.join(steam_path, "steamapps", "workshop", "content", "1158310")
    except Exception as e:
        print(f"Error accessing Steam registry: {e}")
        return None

def check_window_court_files(mod_list, workshop_path):
    results = {}
    for mod_info in mod_list:
        mod_id = mod_info['id']
        mod_name = mod_info.get('name', '')
        mod_short = mod_info.get('short', '')
        
        gui_path = os.path.join(workshop_path, str(mod_id), "gui")
        
        # Check if the file exists (with any extension)
        exists = False
        if os.path.exists(gui_path):
            # Check for any file named window_court (with or without extension)
            for file in os.listdir(gui_path):
                file_path = os.path.join(gui_path, "window_court.gui")
                exists = os.path.isfile(file_path)
        
        results[mod_id] = {
            'exists': exists,
            'name': mod_name,
            'short': mod_short
        }
        
        display_name = f"{mod_name} ({mod_short})" if mod_name and mod_short else mod_name or mod_short or str(mod_id)
        print(f"Checked {display_name} [{mod_id}]: {'Found' if exists else 'Not found'}")
    
    return results

def save_to_json(data, filename="window_court_check.json"):
    with open(filename, 'w') as f:
        json.dump(data, f, indent=4)
    print(f"Results saved to {filename}")

def main():
    # List of mods to check with their IDs, names, and shorts
    mods_to_check = [
        {
            'id': 2962333032,
            'name': 'A Game of Thrones',
            'short': 'AGOT'
        },
        {
            'id': 2291024373,
            'name': 'LotR: Realms in Exile',
            'short': 'LotR'
        },
        {
            'id': 2887120253,
            'name': 'Elder Kings 2',
            'short': 'Elder Kings 2'
        },
        {
            'id': 2243307127,
            'name': 'The Fallen Eagle - After the Pharaohs Update',
            'short': 'The Fallen Eagle'
        },
        {
            'id': 2216659254,
            'name': 'Princes of Darkness',
            'short': 'POD'
        },
        {
            'id': 2949767945,
            'name': 'Warcraft: Guardians of Azeroth Reforged (Release Alpha)',
            'short': 'Warcraft: Guardians of Azeroth'
        },
        {
            'id': 2882431747,
            'name': 'The Witchers Realms',
            'short': 'The Witchers Realms'
        },
        {
            'id': 2326030123,
            'name': 'Godherja: The Dying World',
            'short': 'Godherja: The Dying World'
        },
        # Add more mods in the same format:
        # {
        #     'id': 123456789,
        #     'name': 'Mod Full Name',
        #     'short': 'MOD'
        # },
    ]
    
    if not mods_to_check:
        print("No mods to check. Please add some mods to the mods_to_check list.")
        return
    
    workshop_path = get_steam_workshop_path()
    if not workshop_path:
        print("Could not determine Steam workshop path.")
        return
    
    if not os.path.exists(workshop_path):
        print(f"Workshop path does not exist: {workshop_path}")
        return
    
    results = check_window_court_files(mods_to_check, workshop_path)
    save_to_json(results)

if __name__ == "__main__":
    main()