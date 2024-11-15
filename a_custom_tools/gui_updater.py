import os
from datetime import datetime

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

# Check if the vanilla file needs to be updated
vanilla_file_mod_time = datetime.fromtimestamp(os.path.getmtime(vanilla_file_path))
modded_file_mod_time = datetime.fromtimestamp(os.path.getmtime(modded_file_path))

if vanilla_file_mod_time > modded_file_mod_time:
    print("Vanilla file has been updated. Checking for changes...")
    update_modded_file(vanilla_file_path, modded_file_path, mod_lines)
else:
    print("No updates detected for the vanilla file.")
