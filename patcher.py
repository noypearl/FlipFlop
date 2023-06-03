import argparse
import os
import sys

# Parse command-line arguments
def parse_args():
    parser = argparse.ArgumentParser(description="Patching custom stuff in new firmwares")
    parser.add_argument("-p", "--path", default=".", help="path to directory of the custom firmware sources")
    args = parser.parse_args()
    return args

# Get the relative path from script execution point to filename
# TODO - convert script to class so I won't have to pass firmware-dir_path everywhere lol
# TODO - add reboot fast button to one of the main menus
def get_filename_path(filename, directory):
    for root, dirs, files in os.walk(directory):
        for file in files:
            if file == filename:
                return root+'/'+str(file)
    raise FileNotFoundError(f"File {filename} in {directory} was not found")

# Change dolphin name to my Dog's
def patch_dolphin_name(firmware_dir_path):
    target_filename = "furi_hal_version.c"
    try:
        filepath = get_filename_path(target_filename, firmware_dir_path)
    except FileNotFoundError:
        print(f"Couldn't patch dolphin name -  file {filepath} not found in firmware")
        return

    # Replacement text
    new_name = 'Tutin'
    replacement_text = f'? NULL : "{new_name}"'

    # Read the file contents
    with open(filepath, 'r') as file:
        file_contents = file.read()
        # print(file_contents)

    # Perform the replacement
    updated_contents = file_contents.replace("? NULL : furi_hal_version.name", replacement_text)

    # Write the updated contents back to the file
    with open(filepath, 'w') as file:
        print(f"Updating Dolpin name with {new_name}")
        file.write(updated_contents)
        print(f"Dolphin name was updated to {new_name}!")


# TODO - change the bitmap to my dog's one <3
def patch_dolpihn_image(firmware_dir):
    return

def validate_firmware_exists(firmware_dir_path):
    try:
        get_filename_path('fbt',firmware_dir_path)
    except FileNotFoundError as e :
        print(f"Firmware doesn't exist in {firmware_dir_path}, aborting script :( ")
        sys.exit(e)

def main():
    # Get the firmware path 
    firmware_dir_path = args.path or '.'

    # Validate firmware directory exists
    validate_firmware_exists(firmware_dir_path)

    patch_dolphin_name(firmware_dir_path)
    patch_dolpihn_image(firmware_dir_path)

if __name__ == "__main__":
    args = parse_args()

    main()
    
