import os
from datetime import datetime
import winreg

# Function to insert mod lines into the existing file 
def insert_into_existing_file():
    with open(vanilla_file_path, 'r') as vanilla_file:
        vanilla_content = vanilla_file.readlines()

    # with open(not_my_modded_file_path, 'r') as modded_file:
    #     modded_content = modded_file.readlines()

    # Remove mod lines from the modded content for comparison
    # modded_content_without_mod_lines = [line for line in modded_content if line not in mod_lines]

    # if vanilla_content == modded_content_without_mod_lines:
    #     print("No changes detected in the vanilla file.")
    # else:
        # print("Changes detected in the vanilla file. Updating the modded file...")
        # Find the insertion point for the mod lines in the vanilla content
        # insertion_point = modded_content.index(mod_lines[0])
    stripped_vanilla_content = []
    for line in vanilla_content:
        stripped_vanilla_content.append(line.strip())
    i = 0
    while i < len(vanilla_content):
        if all(line in stripped_vanilla_content[i:i+len(insert_after_lines)] for line in insert_after_lines):
            insertion_point = i+len(insert_after_lines)+1
            print(insertion_point)
            with open(modded_file_path, 'w') as modded_file:
                modded_file.writelines(vanilla_content[:insertion_point])
                modded_file.writelines(mod_lines)
                modded_file.writelines(vanilla_content[insertion_point:])
        i+=1
    print("Modded file updated.")


# Function to compare files and update the modded file if necessary
def update_modded_file(vanilla_file_path, modded_file_path, mod_lines):
    with open(vanilla_file_path, 'r') as vanilla_file:
        vanilla_content = vanilla_file.readlines()

    with open(modded_file_path, 'r') as modded_file:
        modded_content = modded_file.readlines()

    # Remove mod lines from the modded content for comparison
    modded_content_without_mod_lines = [line for line in modded_content if line not in mod_lines]

    if vanilla_content == modded_content_without_mod_lines:
        print("No changes detected in the vanilla file.")
    else:
        print("Changes detected in the vanilla file. Updating the modded file...")
        # Find the insertion point for the mod lines in the vanilla content
        insertion_point = modded_content.index(mod_lines[0])
        with open(modded_file_path, 'w') as modded_file:
            modded_file.writelines(vanilla_content[:insertion_point])
            modded_file.writelines(mod_lines)
            modded_file.writelines(vanilla_content[insertion_point:])
        print("Modded file updated.")

# Function to find the Steam installation path via the Windows Registry 
def find_steam_installation_path(): 
    try: 
        reg_key = winreg.OpenKey(winreg.HKEY_LOCAL_MACHINE, r"SOFTWARE\WOW6432Node\Valve\Steam") 
        steam_path, _ = winreg.QueryValueEx(reg_key, "InstallPath") 
        winreg.CloseKey(reg_key)
        # steam_path = os.path.join(steam_path, 'steamapps', 'common', 'Crusader Kings III', 'game')
        # print(steam_path) 
        return steam_path 
    except FileNotFoundError: 
        raise FileNotFoundError("Steam installation not found in the registry.") 

#global
steam_path = find_steam_installation_path()


# Paths to the vanilla and modded files 
ck3_installation_path = os.path.join(steam_path, 'steamapps', 'common', 'Crusader Kings III', 'game')
ck3_workshop_mods_folder = os.path.join(steam_path, 'steamapps', 'workshop', 'content', '1158310')
vanilla_file_path = os.path.join(ck3_installation_path, 'gui', 'window_court.gui') 
modded_file_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'gui', 'window_court.gui')

mod_lines = [
    "\t\t\t\t\t\t\t\t#MRFP\n",
    "\t\t\t\t\t\t\t\tmrfp_button = {}\n",
    "\t\t\t\t\t\t\t\tmrfp_button_ransom = {}\n",
    "\t\t\t\t\t\t\t\t#MRFP\n"
]
# insert_after_lines = [
#     "\t\t\t\t\t\t\tbutton_round  = {\n",
#     "\t\t\t\t\t\t\t\tname = \"execute\"\n",
#     "\t\t\t\t\t\t\t\tenabled = \"[CourtWindow.CanDoMassPrisonerAction('execute')]\"\n",
#     "\t\t\t\t\t\t\t\tbutton_prison_execute = {\n",
#     "\t\t\t\t\t\t\t\t\tparentanchor = center\n",
#     "\t\t\t\t\t\t\t\t\tonclick = \"[CourtWindow.MassPrisonerAction('execute')]\"\n",
#     "\t\t\t\t\t\t\t\t\ttooltip = \"[CourtWindow.GetMassPrisonerActionTooltip('execute')]\"\n",
#     "\t\t\t\t\t\t\t\t\tusing = tooltip_se\n",
#     "\t\t\t\t\t\t\t\t}\n",
#     "\t\t\t\t\t\t\t}\n"
# ]
insert_after_lines = [
    '''button_round  = {''''',
    '''name = "execute"''',
    '''enabled = "[CourtWindow.CanDoMassPrisonerAction('execute')]"''',
    '''button_prison_execute = {''',
    '''parentanchor = center''',
    '''onclick = "[CourtWindow.MassPrisonerAction(\'execute\')]"''',
    '''tooltip = "[CourtWindow.GetMassPrisonerActionTooltip(\'execute\')]"''',
    '''using = tooltip_se''',
    '''}''',
    '''}'''
]
print(insert_after_lines)

# Check if the vanilla file needs to be updated
vanilla_file_mod_time = datetime.fromtimestamp(os.path.getmtime(vanilla_file_path))
modded_file_mod_time = datetime.fromtimestamp(os.path.getmtime(modded_file_path))

# print(f"Vanilla file was updated at: {vanilla_file_mod_time}")
# print(f"Modded file was updated at: {modded_file_mod_time}")

if vanilla_file_mod_time > modded_file_mod_time:
    print("Vanilla file has been updated. Checking for changes...")
    update_modded_file(vanilla_file_path, modded_file_path, mod_lines)
else:
    print("No updates detected for the vanilla file.")

insert_into_existing_file()