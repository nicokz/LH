import struct
import os
from watch.RP2040watch import GC9A01 as Screen

FONTS_BASE = "/fonts/"

class Font:
    def __init__(self, screen:Screen, font_name = FONTS_BASE + "sans_serif_8x12.bin"):
        # screen - screen driver with buffer where symbols will be drawn to
        # font_name - file name of bitmap font with literal font name, header width, height, chars encoded, bitsarray
        self.screen = screen
        self.name = font_name
        self.load()
        
    def load(self):
        self.desc = "Dummy Font"
        self.width = 0
        self.height = 0
        self.amount = 0
        self.bitmap = bytearray()
        
        with open(self.name, 'rb') as f:
            prefix = f.read(2).decode('ascii')
            if prefix != "BF":
                raise ValueError("Invalid font file prefix.")
            name_length = struct.unpack('B', f.read(1))[0]
            self.desc = f.read(name_length).decode('ascii')
            self.width = struct.unpack('B', f.read(1))[0]
            self.height = struct.unpack('B', f.read(1))[0]
            self.ascii_start = struct.unpack('B', f.read(1))[0]
            self.amount = struct.unpack('B', f.read(1))[0]
            self.bytes_per_char = (self.width + 7) // 8 * self.height
            total_bytes = self.bytes_per_char * self.amount
            self.bitmap = bytearray(f.read(total_bytes))
            if len(self.bitmap) != total_bytes:
                print(f"*** Warning: Expected {total_bytes} bytes but read only {len(self.bitmap)} in {self.name}.")

    def draw(self, x, y, char, color):
        ascii_code = ord(char)
        
        if ascii_code < self.ascii_start or ascii_code >= self.ascii_start + self.amount:
            return  # Skip drawing if the character is out of range
        
        if (x+self.width) > self.screen.width:
            return # Skip out of range by x
        
        if (y+self.height) > self.screen.height:
            return # Skip out of range by y
        
        start = (ascii_code - self.ascii_start) * self.bytes_per_char
        color_high = color >> 8  # High byte of RGB565
        color_low = color & 0xFF  # Low byte of RGB565
        for row in range(self.height):
            byte_index = start + row * ((self.width + 7) // 8)
            for bit in range(self.width):
                if self.bitmap[byte_index + (bit // 8)] & (0b10000000 >> (bit % 8)):
                    # Calculate the index in the buffer for the pixel
                    buffer_index = ((y + row) * self.screen.width + (x + bit)) * 2
                    # Set the color in the buffer
                    self.screen.buffer[buffer_index] = color_high
                    self.screen.buffer[buffer_index + 1] = color_low
                    
    def draw_blended(self, x: int, y: int, char: str, color: int, alpha: int):
        ascii_code = ord(char)
    
        if ascii_code < self.ascii_start or ascii_code >= self.ascii_start + self.amount:
            return  # Skip drawing if the character is out of range
    
        if (x + self.width) > self.screen.width or (y + self.height) > self.screen.height:
            return  # Skip if character will be out of bounds
    
        # Extract the font color channels
        r_color, g_color, b_color = (color >> 11) & 0x1F, (color >> 5) & 0x3F, color & 0x1F
        inv_alpha = 255 - alpha
        start = (ascii_code - self.ascii_start) * self.bytes_per_char

        for row in range(self.height):
            byte_index = start + row * ((self.width + 7) // 8)
            for bit in range(self.width):
                # Check if the font pixel is set (i.e., part of the character)
                if self.bitmap[byte_index + (bit // 8)] & (0b10000000 >> (bit % 8)):
                    # Calculate the index in the buffer for the pixel
                    buffer_index = ((y + row) * self.screen.width + (x + bit)) * 2

                    # Read background color from buffer at the pixel position
                    bg_color = (self.screen.buffer[buffer_index] << 8) | self.screen.buffer[buffer_index + 1]
                    r_bg = (bg_color >> 11) & 0x1F
                    g_bg = (bg_color >> 5) & 0x3F
                    b_bg = bg_color & 0x1F

                    # Blend each channel using alpha
                    blended_r = ((r_bg * inv_alpha) + (r_color * alpha)) >> 8
                    blended_g = ((g_bg * inv_alpha) + (g_color * alpha)) >> 8
                    blended_b = ((b_bg * inv_alpha) + (b_color * alpha)) >> 8

                    # Ensure the blended channels are within valid RGB565 limits
                    blended_r = min(31, max(0, blended_r))
                    blended_g = min(63, max(0, blended_g))
                    blended_b = min(31, max(0, blended_b))

                    # Compose the blended color in RGB565
                    blended_color = (blended_r << 11) | (blended_g << 5) | blended_b
                
                    # Set the blended color in the buffer
                    self.screen.buffer[buffer_index] = (blended_color >> 8) & 0xFF  # High byte
                    self.screen.buffer[buffer_index + 1] = blended_color & 0xFF      # Low byte
        
class Text:
    CENTER = -1
    ALIGN_LEFT = -2
    ALIGN_RIGHT = -3
    ALIGN_TOP = -4
    ALIGN_BOTTOM = -5
    SAFE_ZONE = 36
    
    def __init__(self, font:Font, safe = False):
        self.posX = 0
        self.posY = 0
        self.font = font
        self.marging_min = 0
        self.marging_max = self.font.screen.width
        self.safe_zone(safe)
        self.isClipped = False
        
    def change_font(self, font:Font):
        self.font = font
        
    def safe_zone(self, safe):
        self.safe = safe
        if safe:
            self.marging_min = self.SAFE_ZONE
            self.marging_max = self.font.screen.width - self.SAFE_ZONE
        else:
            self.marging_min = 0
            self.marging_max = self.font.screen.width
            
    @micropython.viper
    def wipe(self):
        if self.isClipped:
            back_buf = ptr8(self.clip_buf)  # Pointer to the backup buffer
            screen_buf = ptr8(self.font.screen.buffer)  # Pointer to the screen buffer
            width = int(self.clip_width)
            height = int(self.clip_height)
            screen_width = int(self.font.screen.width)
            screen_height = int(self.font.screen.height)
            pos_x_prev = int(self.clip_x)
            pos_y_prev = int(self.clip_y)
        
            for y in range(height):
                for x in range(width):
                    # Calculate previous screen coordinates
                    screen_x_prev = pos_x_prev + x
                    screen_y_prev = pos_y_prev + y

                    # Ensure the sprite fits within the screen boundaries
                    if 0 <= screen_x_prev < screen_width and 0 <= screen_y_prev < screen_height:
                        # Compute buffer indices for restoration
                        prev_screen_index = (screen_y_prev * screen_width + screen_x_prev) * 2
                        sprite_index = (y * width + x) * 2

                        # Restore the background pixel from the backup buffer
                        screen_buf[prev_screen_index] = back_buf[sprite_index]  # High byte
                        screen_buf[prev_screen_index + 1] = back_buf[sprite_index + 1]  # Low byte
            
    @micropython.viper
    def backup(self, x:int, y:int, width:int, height:int):
        self.clip_x = x
        self.clip_y = y
        self.clip_width = width
        self.clip_height = height
        buffer_size = width * height * 2 
        self.clip_buf = bytearray(buffer_size)
        # speed up
        clip_buf = ptr8(self.clip_buf)  # Pointer to the backup buffer
        screen_buf = ptr8(self.font.screen.buffer)  # Pointer to the screen buffer
        
        #width = int(self.width)
        #height = int(self.height)
        screen_width = int(self.font.screen.width)
        screen_height = int(self.font.screen.height)        
        pos_x = x
        pos_y = y
        
        for y in range(height):
            for x in range(width):
                screen_x = pos_x + x
                screen_y = pos_y + y
                # Ensure the sprite fits within the screen boundaries
                if 0 <= screen_x < screen_width and 0 <= screen_y < screen_height:
                    screen_index = (screen_y * screen_width + screen_x) * 2
                    sprite_index = (y * width + x) * 2
                    # Backup the current screen pixel data
                    clip_buf[sprite_index] = screen_buf[screen_index]  # High byte
                    clip_buf[sprite_index + 1] = screen_buf[screen_index + 1]  # Low byte
                    
        self.isClipped = True  # Set backup flag to true
        
        
            
    def draw(self, string, color, x=None, y=None, clip_on = False, shadow = 0xFF):
        posX = x if x is not None else self.posX
        posY = y if y is not None else self.posY
        if posX == self.CENTER:
            posX = int((self.font.screen.width - len(string) * self.font.width) / 2)
        elif posX == self.ALIGN_RIGHT:
            posX = self.marging_max - len(string) * self.font.width
        elif posX < 0:
            posX = self.marging_min
        if posY == self.CENTER:
            posY = int((self.font.screen.height - self.font.height) / 2)
        elif posY == self.ALIGN_BOTTOM:
            posY = self.marging_max - self.font.height
        elif posY < 0:
            posY = self.marging_min
            
        
        if clip_on:
            if self.isClipped:
                self.wipe()
            self.backup(posX, posY, len(string) * self.font.width, self.font.height)
            
        stepX = self.font.width
        stepY = self.font.height
        shadow_color = self.font.screen.color(0,0,0)
        for s in string:
            if (posX + stepX > self.font.screen.width):
                posX = self.marging_min
                posY += stepY
            if shadow < 0xFF:
                self.font.draw_blended(posX+1,posY+1, s, shadow_color, shadow)
            self.font.draw(posX,posY, s, color)
            posX += stepX
            
    def draw_blended(self, string, color, alpha, x=None, y=None):
        posX = x if x is not None else self.posX
        posY = y if y is not None else self.posY
        if posX == self.CENTER:
            posX = int((self.font.screen.width - len(string) * self.font.width) / 2)
        elif posX == self.ALIGN_RIGHT:
            posX = self.marging_max - len(string) * self.font.width
        elif posX < 0:
            posX = self.marging_min
        if posY == self.CENTER:
            posY = int((self.font.screen.height - self.font.width) / 2)
        elif posY == self.ALIGN_BOTTOM:
            posY = self.marging_max - self.font.height
        elif posY < 0:
            posY = self.marging_min
            
        stepX = self.font.width
        stepY = self.font.height
        shadow_color = screen.color(0,0,0)
        for s in string:
            if (posX + stepX > self.font.screen.width):
                posX = self.marging_min
                posY += stepY
            self.font.draw_blended(posX,posY, s, color, alpha)
            posX += stepX
        
if __name__=='__main__':
    screen = Screen() # init GC9A01
    screen.loadRGB565background('/images/rp2040_bg.rgb565')
    font = Font(screen)
    text = Text(font)
    text.safe_zone(True)
    text.draw("+", screen.color(255,241,0), text.CENTER, text.CENTER)
    #text.draw("LEFT", screen.color(110,200,110), text.ALIGN_LEFT, text.ALIGN_TOP, 128)
    text.draw_blended("LEFT", screen.color(110,200,110), 200, text.ALIGN_LEFT, text.ALIGN_TOP)
    text.draw("RIGHT", screen.color(110,200,110), text.ALIGN_RIGHT, text.ALIGN_TOP)
    text.draw("LEFT", screen.color(180,180,255), text.ALIGN_LEFT, text.CENTER)
    #text.draw("RIGHT", screen.color(180,180,255), text.ALIGN_RIGHT, text.CENTER, 10)
    text.draw_blended("RIGHT", screen.color(180,180,255), 100, text.ALIGN_RIGHT, text.CENTER)
    text.draw("TOP", screen.color(150,250,255), text.CENTER, text.ALIGN_TOP, 128)
    text.draw("BOTTOM", screen.color(150,250,255), text.CENTER, text.ALIGN_BOTTOM)
    text.draw("LEFT", screen.color(110,200,110), text.ALIGN_LEFT, text.ALIGN_BOTTOM)
    text.draw("RIGHT", screen.color(110,200,110), text.ALIGN_RIGHT, text.ALIGN_BOTTOM)
    screen.show()