import os
from datetime import datetime
import winreg

# Function to compare files and update the modded file if necessary
def update_modded_file(vanilla_file_path, modded_file_path, mod_lines):
    with open(vanilla_file_path, 'r') as vanilla_file:
        vanilla_content = vanilla_file.readlines()

    with open(modded_file_path, 'r') as modded_file:
        modded_content = modded_file.readlines()

    # Check if the modded file contains only the mod lines
    modded_content_without_mod_lines = [line for line in modded_content if line not in mod_lines]

    if vanilla_content == modded_content_without_mod_lines:
        print("No changes detected in the vanilla file.")
    else:
        print("Changes detected in the vanilla file. Updating the modded file...")
        with open(modded_file_path, 'w') as modded_file:
            modded_file.writelines(vanilla_content)
            modded_file.writelines(mod_lines)
        print("Modded file updated.")

# Paths to the vanilla and modded files
# vanilla_file_path = "path/to/vanilla/file"
# modded_file_path = "path/to/modded/file"
# Function to find the CK3 installation path via Steam 
def find_ck3_installation_path(): 
    steam_path = os.path.join(os.getenv('ProgramFiles(x86)'), 'Steam', 'steamapps', 'common', 'Crusader Kings III') 
    if os.path.exists(steam_path):
        print(steam_path) 
        return steam_path 
    else: 
        raise FileNotFoundError("Crusader Kings III installation not found.")
    
# Function to find the Steam installation path via the Windows Registry 
def find_steam_installation_path(): 
    try: 
        reg_key = winreg.OpenKey(winreg.HKEY_LOCAL_MACHINE, r"SOFTWARE\WOW6432Node\Valve\Steam") 
        steam_path, _ = winreg.QueryValueEx(reg_key, "InstallPath") 
        winreg.CloseKey(reg_key)
        print(steam_path) 
        return steam_path 
    except FileNotFoundError: 
        raise FileNotFoundError("Steam installation not found in the registry.") 
# Paths to the vanilla and modded files 
# ck3_installation_path = find_ck3_installation_path()
ck3_installation_path = find_steam_installation_path()  
# vanilla_file_path = os.path.join(ck3_installation_path, 'gui', 'your_vanilla_file.gui') 
# modded_file_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'gui', 'your_modded_file.gui')


mod_lines = [
    "\t\t\t\t\t\t\t\t#MRFP\n",
    "\t\t\t\t\t\t\t\tmrfp_button = {}\n",
    "\t\t\t\t\t\t\t\tmrfp_button_ransom = {}\n",
    "\t\t\t\t\t\t\t\t#MRFP\n"
]

# Check if the vanilla file needs to be updated
vanilla_file_mod_time = datetime.fromtimestamp(os.path.getmtime(vanilla_file_path))
modded_file_mod_time = datetime.fromtimestamp(os.path.getmtime(modded_file_path))

if vanilla_file_mod_time > modded_file_mod_time:
    print("Vanilla file has been updated. Checking for changes...")
    # update_modded_file(vanilla_file_path, modded_file_path, mod_lines)
else:
    print("No updates detected for the vanilla file.")
