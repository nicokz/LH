import argparse
from PIL import Image

def convert_png_to_rgb565_with_transparency(input_png, output_rgb565, key_color=(0xF8, 0x1F, 0x00)):
    # Open the PNG file with RGBA mode (to handle transparency)
    img = Image.open(input_png).convert("RGBA")
    width, height = img.width, img.height
    
    # Create a bytearray for the output file
    rgb565_data = bytearray()
    
    # Add the width and height as a 4-byte header
    rgb565_data.append((width >> 8) & 0xFF)  # Width high byte
    rgb565_data.append(width & 0xFF)         # Width low byte
    rgb565_data.append((height >> 8) & 0xFF) # Height high byte
    rgb565_data.append(height & 0xFF)        # Height low byte

    # Loop through each pixel in the image
    for y in range(height):
        for x in range(width):
            # Get the RGBA values of the pixel
            r, g, b, a = img.getpixel((x, y))
            
            if a < 128:  # Transparency threshold
                # Use key color for transparency
                r, g, b = key_color
            else:
                # Apply RGB565 bit mask
                r = r & 0xF8  # Top 5 bits
                g = g & 0xFC  # Top 6 bits
                b = b & 0xF8  # Top 5 bits

            # Pack into RGB565
            rgb565 = ((r << 8) | (g << 3) | (b >> 3)) & 0xFFFF

            # Append the high and low byte
            rgb565_data.append((rgb565 >> 8) & 0xFF)
            rgb565_data.append(rgb565 & 0xFF)

    # Write the data to a binary file
    with open(output_rgb565, "wb") as f:
        f.write(rgb565_data)

# Set up CLI argument parsing
if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Convert PNG with transparency to RGB565 format with a key color.")
    parser.add_argument("input_png", help="Path to the input PNG file.")
    parser.add_argument("output_rgb565", help="Path to the output RGB565 binary file.")
    parser.add_argument("--key-color", type=str, default="F81F", help="Hex code for the key color (default is magenta F81F).")
    args = parser.parse_args()

    # Parse key color argument from hex string to RGB565
    key_color_hex = int(args.key_color, 16)
    key_color = ((key_color_hex >> 11) & 0x1F) << 3, ((key_color_hex >> 5) & 0x3F) << 2, (key_color_hex & 0x1F) << 3

    # Run the conversion
    convert_png_to_rgb565_with_transparency(args.input_png, args.output_rgb565, key_color)

