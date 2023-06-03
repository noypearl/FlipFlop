import argparse
import struct
import os
import sys
import math
from datetime import datetime

parser = argparse.ArgumentParser(description="Patch the icounter(xp) of a flipper-zero's .dolphin.state")
parser.add_argument("file", type=str, help="Path of the .dolphin.state file")
parser.add_argument("xp", type=int, help="new value of XP (icounter). lv1: 0-300, lv2 : 301-1800, lv3: 1801+")
args = parser.parse_args()

state_filepath = args.file
# Check that file exists
if not os.path.exists(state_filepath):
    print(f'File {state_filepath} does not exist. Aborting...')
    sys.exit(1)

# replace bytes of icount and checksum
with open(state_filepath, 'r+b') as reader:
    # buffer = reader.read()
    xp = int(args.xp)
    # print("[+] Read", len(buffer), "bytes from", args.file)
    reader.seek(2)
    checksum = int.from_bytes(reader.read(1), byteorder='little')
    reader.seek(20)
    icount = int.from_bytes(reader.read(4), byteorder='little')
    print(f"Current icount: {hex(icount)}, Current checksum: {hex(checksum)}")
    new_icount = xp
    # Add to checksum, since xp is larger than icount
    if xp > icount:
        diff = xp - icount
        # No need to re-calculate checksum - just add the diff, modulo & add remainder :)
        temp_checksum = checksum + diff
        remainder = math.floor(temp_checksum / 256)
        new_checksum = temp_checksum % 256 + remainder
        print(f"Changing icount to : {new_icount}, hex: {hex(new_icount)}")
        print(f"Changing checksum to : {new_checksum}, hex: {hex(new_checksum)} ")
    # Subtract from checksum, since xp is lower than icount
    elif xp < icount:
        print(f"Noo! Don't decrease your xp, we are cheaters, remember!? \nAborting! Are you crazy!?")
        sys.exit(1)
    else:
        print("xp is the same as current xp (icount) in state file.\nAre you trolling? \nAborting.")
        sys.exit(1)

    # Replace byte of checksum
    print(f"Writing values to {state_filepath} file")
    reader.seek(2)
    reader.write(new_checksum.to_bytes(1, byteorder='little'))
    # Replace bytes of icount
    reader.seek(20)
    reader.write(new_icount.to_bytes(4, byteorder='little'))
    reader.close()
    print("Done!")





# unpack_header(buffer)
# unpack_state(buffer)
