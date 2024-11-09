from PIL import Image

def convert_to_rgb565(input_file, output_file):
    img = Image.open(input_file)
    img = img.convert('RGB').resize((240, 240))  # Resize to your display dimensions
    with open(output_file, 'wb') as f:
        for pixel in img.getdata():
            r, g, b = pixel
            # Convert RGB888 to RGB565
            rgb565 = ((r & 0xF8) << 8) | ((g & 0xFC) << 3) | (b >> 3)
            f.write(rgb565.to_bytes(2, 'big'))

convert_to_rgb565('test_bg.jpg', 'test_bg.rgb565')

