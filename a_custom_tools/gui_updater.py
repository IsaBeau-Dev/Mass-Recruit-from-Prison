import os
import requests

# Function to get the current version of Crusader Kings 3 from Steam
def get_ck3_version():
    steam_api_url = "https://api.steampowered.com/ISteamApps/GetAppList/v2/"
    response = requests.get(steam_api_url)
    app_list = response.json()["applist"]["apps"]
    ck3_app = next(app for app in app_list if app["name"] == "Crusader Kings III")
    ck3_app_id = ck3_app["appid"]

    steam_app_details_url = f"https://store.steampowered.com/api/appdetails?appids={ck3_app_id}"
    response = requests.get(steam_app_details_url)
    ck3_details = response.json()[str(ck3_app_id)]["data"]
    ck3_version = ck3_details["version"]
    return ck3_version

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
vanilla_file_path = "path/to/vanilla/file"
modded_file_path = "path/to/modded/file"
mod_lines = [
    "mod_line_1\n",
    "mod_line_2\n",
    "mod_line_3\n",
    "mod_line_4\n"
]

# Get the current version of Crusader Kings 3
ck3_version = get_ck3_version()
print(f"Current version of Crusader Kings 3: {ck3_version}")

# Update the modded file if necessary
# update_modded_file(vanilla_file_path, modded_file_path, mod_lines)
