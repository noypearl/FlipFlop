import argparse
import subprocess
import os
import sys

class FirmwarePatcher:
    def __init__(self, firmware_dir_path=".", firmware_type="original"):
        # Initialize the path to firmware directory
        self.firmware_dir_path = firmware_dir_path
        self.firmware_type = firmware_type
        self._validate_firmware_exists()
        self._os = self._init_os()

    def _init_os(self):
        if os.name == 'nt':
            return 'windows'
        else:
            return 'linux'

    def get_filename_path(self, filename):
        # Get the relative path from script execution point to filename
        for root, dirs, files in os.walk(self.firmware_dir_path):
            for file in files:
                if file == filename:
                    return root+'/'+str(file)
        raise FileNotFoundError(f"File {filename} in {self.firmware_dir_path} was not found")

    def replace_text_in_firmware_file(self, target_filename, text_to_search, new_text):
        # Patch a specific file by simply replacing other text
        try:
            filepath = self.get_filename_path(target_filename)
        except FileNotFoundError:
            print(f"Couldn't patch {target_filename} file - it was not found in the firmware.\nAre you sure the file exists in the specific firmware?\nTODO - add support/fix for other firmwares")
            return

        # Read the file contents
        with open(filepath, 'r') as file:
            file_contents = file.read()

        # Perform the replacement
        updated_contents = file_contents.replace(text_to_search, new_text)

        # Write the updated contents back to the file
        with open(filepath, 'w') as file:
            print(f"Updating {filepath}, old string: {text_to_search} new string: {new_text}")
            file.write(updated_contents)
            print(f"file {target_filename} was updated!")

    def patch_dolphin_name(self, new_name='Tutin'):
        new_text = f'? NULL : "{new_name}"'
        target_filename = "furi_hal_version.c"
        self.replace_text_in_firmware_file(target_filename, "? NULL : furi_hal_version.name" , new_text)

    def patch_dolphin_image(self):
        # Method to change the dolphin image in the firmware
        # TODO: Implement the image patch
        pass

    # The script should do every patch - we won't try to patch when the user sends us a string instead of int
    def validate_int(self, *integersArgs):
        for integer in integersArgs:
            try:
                int(integer)
            except ValueError as e:
                raise ValueError(f"got invalid int string to patch - {str(e)}.\nAborting.")

    def patch_flappy_bird(self, initial_points=0, counter_points=1):
        target_filename = 'flappy_bird.c'
        # validate points input
        self.validate_int(initial_points, counter_points)
        # Set custom initial score
        print(f"Patching flappy bird initial points to {initial_points}")
        self.replace_text_in_firmware_file(target_filename,"game_state->points = 0",f"game_state->points = {initial_points}")

        # Score will be increased by 10 instead of 1
        print(f"Patching flappy bird counter points to {counter_points}")
        self.replace_text_in_firmware_file(target_filename,"game_state->points++",f"game_state->points+={counter_points}")


    def _validate_firmware_exists(self):
        # Method to check if the firmware exists in the specified path
        try:
            self.get_filename_path('fbt')
        except FileNotFoundError as e :
            print(f"Firmware doesn't exist in {self.firmware_dir_path}, aborting script :( ")
            sys.exit(e)


    def build_firmware(self, build_args):
        # For preserving current dir
        curr_dir = os.getcwd()
        os_type = self._os
        fbt_executable = 'fbt.cmd' if os_type == 'windows' else 'fbt'
        command = f"./{fbt_executable} {build_args}"
        # Otherwise the fbt build won't work and we'll get  No SConstruct file found error
        os.chdir(self.firmware_dir_path)
        process = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)

        # Print output as it becomes available
        for line in iter(process.stdout.readline, ''):
            print(line.decode(), end='')
        
        # Wait for the process to finish and get the return code
        process.stdout.close()
        return_code = process.wait()

        if return_code != 0:
            print(f"{return_code} Failed to build firmware when running {command}")
            print(f"Error message: {process.stderr.read().decode()}")
        else:
            print(f"Built firmware successfully: \n Now go to dist and update to qFlipper")

        # Return back to preserve script context
        os.chdir(curr_dir)




def parse_args():
    # Parse command-line arguments
    parser = argparse.ArgumentParser(description="Patching custom stuff in new firmwares")
    parser.add_argument("-p", "--path", default=".", help="path to directory of the custom firmware sources")
    parser.add_argument("-f", "--firmware", default="original", help="Firmware type of the flipper")
    parser.add_argument("-b", "--build", help="Build the firmware as well with fbt. can have arguments",action='store_true', required=False)
    parser.add_argument("-a", "--build_args", help="Custom arguments for the build",default="COMPACT=1 DEBUG=1 updater_package")

    args = parser.parse_args()
    return args

def main():
    args = parse_args()
    patcher = FirmwarePatcher(args.path, args.firmware)
    patcher.patch_dolphin_name()
    patcher.patch_flappy_bird(1337, 10)
    if args.build:
        patcher.build_firmware(args.build_args)


if __name__ == "__main__":
    main()