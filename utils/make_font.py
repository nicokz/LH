import math
import struct
#from utils.sans_serif_8x12 import FONT_FILE, FONT_NAME, WIDTH, HEIGHT, ASCII_START, font
from utils.big_32x45 import FONT_FILE, FONT_NAME, WIDTH, HEIGHT, ASCII_START, font

FONTS_BASE = "/fonts/"


# Header data

file_name = FONTS_BASE+FONT_FILE

PREFIX = "BF"

NAME_LENGTH = len(FONT_NAME)

bytes_per_char =  math.ceil(WIDTH / 8) * HEIGHT

font_length = len(font)
print(f"Font length {font_length}")

print(f"     File name : {file_name}")
print(f"   Description : {FONT_NAME}")
print(f"   Symbol size : {WIDTH}x{HEIGHT}")
print(f"Bytes per char : {bytes_per_char}")
print(f"Symbols amount : {font_length}")

# Open file in binary write mode
with open(file_name, 'wb') as f:
    # Write header
    f.write(PREFIX.encode('ascii'))              # 2 bytes for PREFIX
    f.write(struct.pack('B', NAME_LENGTH))       # 1 byte for name length
    f.write(FONT_NAME.encode('ascii'))                # N bytes for NAME
    f.write(struct.pack('B', WIDTH))             # 1 byte for WIDTH
    f.write(struct.pack('B', HEIGHT))            # 1 byte for HEIGHT
    f.write(struct.pack('B', ASCII_START))       # 1 byte for ASCII_START
    f.write(struct.pack('B', font_length))       # 1 byte for amount of described symbols in font
    
    # Write each character's bitmap data
    for char in range(ASCII_START, ASCII_START + font_length):
        char_key = chr(char)
        if char_key in font:
            for row in font[char_key]:
                f.write(struct.pack('B', row))   # Write each row as a single byte
                