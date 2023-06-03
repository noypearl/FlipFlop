import argparse
import struct
import os

parser = argparse.ArgumentParser(description="Packer for bytes, enter byte and get the little endian representation for binary relace")
parser.add_argument("byte", type=str, help="unter byte value, such as 300, 0x50")
args = parser.parse_args()
byte = int(args.byte)
print(f"Packing {byte}")
packed = struct.pack("I", byte)
print(f"here's your binary stuff: \n{packed}")
