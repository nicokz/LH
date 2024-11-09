from machine import Pin,I2C,SPI,PWM,ADC
import framebuf
import math
import time
import random
import gc

DC = 8
CS = 9
SCK = 10
MOSI = 11
RST = 12
BL = 25

S1 = 17
S2 = 18
S3 = 16

I2C_SDA = 6
I2C_SDL = 7

Vbat_Pin = 29

NORTH = 0
EAST = 1
WEST = 2
SOUTH = 3

class GC9A01 (framebuf.FrameBuffer):
    def __init__(self):
        self.width = 240
        self.height = 240
        self._cmd_buffer = bytearray(1)
        self.black =   0x0000
        self.red   =   0x07E0
        self.green =   0x001f
        self.blue  =   0xf800
        self.white =   0xffff
        self.cs = Pin(CS,Pin.OUT)
        self.rst = Pin(RST,Pin.OUT)
        self.cs(1)
        self.spi = SPI(1,100_000_000,polarity=0, phase=0,sck=Pin(SCK),mosi=Pin(MOSI),miso=None)
        self.dc = Pin(DC,Pin.OUT)
        self.dc(1)
        self.buffer = bytearray(self.height * self.width * 2)
        super().__init__(self.buffer, self.width, self.height, framebuf.RGB565)
        self.init()
        self.fill(0x0000)
        self.show()
        self.pwm = PWM(Pin(BL))
        self.pwm.freq(5000)
        
    def init(self):
        self.rst(1)
        time.sleep(0.01)
        self.rst(0)
        time.sleep(0.01)
        self.rst(1)
        time.sleep(0.05)
        self.write_cmd(0xEF)
        self.write_cmd(0xEB)
        self.write_data(0x14)
        self.write_cmd(0xFE)
        self.write_cmd(0xEF)
        self.write_cmd(0xEB)
        self.write_data(0x14) 
        self.write_cmd(0x84)
        self.write_data(0x40)
        self.write_cmd(0x85)
        self.write_data(0xFF) 
        self.write_cmd(0x86)
        self.write_data(0xFF) 
        self.write_cmd(0x87)
        self.write_data(0xFF)
        self.write_cmd(0x88)
        self.write_data(0x0A)
        self.write_cmd(0x89)
        self.write_data(0x21) 
        self.write_cmd(0x8A)
        self.write_data(0x00) 
        self.write_cmd(0x8B)
        self.write_data(0x80) 
        self.write_cmd(0x8C)
        self.write_data(0x01) 
        self.write_cmd(0x8D)
        self.write_data(0x01) 
        self.write_cmd(0x8E)
        self.write_data(0xFF) 
        self.write_cmd(0x8F)
        self.write_data(0xFF)
        self.orient(NORTH)
        self.write_cmd(0x3A)
        self.write_data(0x05)
        self.write_cmd(0x90)
        self.write_data(0x08)
        self.write_data(0x08)
        self.write_data(0x08)
        self.write_data(0x08)
        self.write_cmd(0xBD)
        self.write_data(0x06)
        self.write_cmd(0xBC)
        self.write_data(0x00)
        self.write_cmd(0xFF)        
        self.write_data(0x60)
        self.write_data(0x01)
        self.write_data(0x04)
        self.write_cmd(0xC3)
        self.write_data(0x13)
        self.write_cmd(0xC4)
        self.write_data(0x13)
        self.write_cmd(0xC9)
        self.write_data(0x22)
        self.write_cmd(0xBE)
        self.write_data(0x11) 
        self.write_cmd(0xE1)
        self.write_data(0x10)
        self.write_data(0x0E)
        self.write_cmd(0xDF)
        self.write_data(0x21)
        self.write_data(0x0c)
        self.write_data(0x02)
        self.write_cmd(0xF0)   
        self.write_data(0x45)
        self.write_data(0x09)
        self.write_data(0x08)
        self.write_data(0x08)
        self.write_data(0x26)
        self.write_data(0x2A)
        self.write_cmd(0xF1)    
        self.write_data(0x43)
        self.write_data(0x70)
        self.write_data(0x72)
        self.write_data(0x36)
        self.write_data(0x37)  
        self.write_data(0x6F)
        self.write_cmd(0xF2)   
        self.write_data(0x45)
        self.write_data(0x09)
        self.write_data(0x08)
        self.write_data(0x08)
        self.write_data(0x26)
        self.write_data(0x2A)
        self.write_cmd(0xF3)   
        self.write_data(0x43)
        self.write_data(0x70)
        self.write_data(0x72)
        self.write_data(0x36)
        self.write_data(0x37) 
        self.write_data(0x6F)
        self.write_cmd(0xED)
        self.write_data(0x1B) 
        self.write_data(0x0B) 
        self.write_cmd(0xAE)
        self.write_data(0x77)
        self.write_cmd(0xCD)
        self.write_data(0x63)
        self.write_cmd(0x70)
        self.write_data(0x07)
        self.write_data(0x07)
        self.write_data(0x04)
        self.write_data(0x0E) 
        self.write_data(0x0F) 
        self.write_data(0x09)
        self.write_data(0x07)
        self.write_data(0x08)
        self.write_data(0x03)
        self.write_cmd(0xE8)
        self.write_data(0x34)
        self.write_cmd(0x62)
        self.write_data(0x18)
        self.write_data(0x0D)
        self.write_data(0x71)
        self.write_data(0xED)
        self.write_data(0x70) 
        self.write_data(0x70)
        self.write_data(0x18)
        self.write_data(0x0F)
        self.write_data(0x71)
        self.write_data(0xEF)
        self.write_data(0x70) 
        self.write_data(0x70)
        self.write_cmd(0x63)
        self.write_data(0x18)
        self.write_data(0x11)
        self.write_data(0x71)
        self.write_data(0xF1)
        self.write_data(0x70) 
        self.write_data(0x70)
        self.write_data(0x18)
        self.write_data(0x13)
        self.write_data(0x71)
        self.write_data(0xF3)
        self.write_data(0x70) 
        self.write_data(0x70)
        self.write_cmd(0x64)
        self.write_data(0x28)
        self.write_data(0x29)
        self.write_data(0xF1)
        self.write_data(0x01)
        self.write_data(0xF1)
        self.write_data(0x00)
        self.write_data(0x07)
        self.write_cmd(0x66)
        self.write_data(0x3C)
        self.write_data(0x00)
        self.write_data(0xCD)
        self.write_data(0x67)
        self.write_data(0x45)
        self.write_data(0x45)
        self.write_data(0x10)
        self.write_data(0x00)
        self.write_data(0x00)
        self.write_data(0x00)
        self.write_cmd(0x67)
        self.write_data(0x00)
        self.write_data(0x3C)
        self.write_data(0x00)
        self.write_data(0x00)
        self.write_data(0x00)
        self.write_data(0x01)
        self.write_data(0x54)
        self.write_data(0x10)
        self.write_data(0x32)
        self.write_data(0x98)
        self.write_cmd(0x74)
        self.write_data(0x10)
        self.write_data(0x85)
        self.write_data(0x80)
        self.write_data(0x00) 
        self.write_data(0x00) 
        self.write_data(0x4E)
        self.write_data(0x00)
        self.write_cmd(0x98)
        self.write_data(0x3e)
        self.write_data(0x07)
        self.write_cmd(0x35)
        self.write_cmd(0x21)
        self.write_cmd(0x11)
        time.sleep(0.12)
        self.write_cmd(0x29)
        time.sleep(0.02)
        self.write_cmd(0x21)
        self.write_cmd(0x11)
        self.write_cmd(0x29)
    
    def set_bl_pwm(self,duty):
        self.pwm.duty_u16(duty)#max 65535

    @micropython.viper
    def write_cmd(self, cmd:int):
        self.cs(1)
        self.dc(0)
        self.cs(0)
        self.spi.write(bytearray([cmd]))
        self.cs(1)
        
    @micropython.viper
    def write_data(self, data:int):
        self.cs(1)
        self.dc(1)
        self.cs(0)
        self.spi.write(bytearray([data]))
        self.cs(1)
        
    def show(self):        
        self.write_cmd(0x2A)
        self.write_data(0x00)
        self.write_data(0x00)
        self.write_data(0x00)
        self.write_data(0xef)        
        self.write_cmd(0x2B)
        self.write_data(0x00)
        self.write_data(0x00)
        self.write_data(0x00)
        self.write_data(0xEF)
        self.write_cmd(0x2C)
        self.cs(1)
        self.dc(1)
        self.cs(0)
        self.spi.write(self.buffer)
        self.cs(1)
        
    def brightness(self, dimm):
        self.write_cmd(0x51)
        self.write_data(dimm)
       
    def display(self,on):
        if on:
            self.write_cmd(0x29)
        else:
            self.write_cmd(0x28)
            
    def sleep_mode(self,on):
        if on:
            self.write_cmd(0x10)
        else:
            self.write_cmd(0x11)
            
    def invert(self,on):
        if on:
            self.write_cmd(0x21)
        else:
            self.write_cmd(0x20)

    def orient(self, direction):
        dfc_param = 0x00
        mac_param = 0b00101000
        if direction == EAST:
            dfc_param = 0x00
            mac_param = 0b10001000
        elif direction == SOUTH:
            dfc_param = 0x00
            mac_param = 0b11101000 
        elif direction == WEST:
            dfc_param = 0x00
            mac_param = 0b01001000
        self.write_cmd(0xB6)
        self.write_data(0x00)
        self.write_data(dfc_param)
        self.write_cmd(0x36)
        self.write_data(mac_param)

    def loadRGB565background(self,file_name):
        with open(file_name, 'rb') as f:
            pos = 0  # Position in framebuffer's buffer
            chunk_size = 1024  # Adjust chunk size as needed for memory efficiency
            while pos < len(self.buffer):
                chunk = f.read(chunk_size)
                if not chunk:  # End of file
                    break
                self.buffer[pos:pos+len(chunk)] = chunk
                pos += len(chunk)

    def color(self, red, green, blue):
        r_5 = red >> 3      # Scale red to 5 bits
        g_6 = green >> 2      # Scale green to 6 bits
        b_5 = blue >> 3      # Scale blue to 5 bits
        
        return (r_5 << 11) | (g_6 << 5) | b_5
        
    
    def rgb565_to_rgb888(self, rgb565):
        r = (rgb565 >> 11) & 0x1F  # Red component (5 bits)
        g = (rgb565 >> 5) & 0x3F   # Green component (6 bits)
        b = rgb565 & 0x1F          # Blue component (5 bits)
    
        # Scale to 8 bits
        r_8 = (r * 255) // 31  # Scale red
        g_8 = (g * 255) // 63  # Scale green
        b_8 = (b * 255) // 31  # Scale blue
    
        return r_8, g_8, b_8
    
    def setPixel(self,x,y, color):
        index = (y * self.width + x) * 2  # Calculate the byte index in the buffer
        self.buffer[index] = color >> 8  # High byte of RGB565
        self.buffer[index + 1] = color & 0xFF  # Low byte of RGB565
        
    def getPixel(self,x,y):
        index = (y * self.width + x) * 2  # Calculate the index in the framebuffer
        return (self.buffer[index] << 8) | self.buffer[index + 1]
    
    def fill_rectangle(self, x, y, width, height, color):
        for row in range(y, y + height):
            for col in range(x, x + width):
                self.setPixel(col, row, color)
    
    def blend_colors(self, bg_color, fg_color, alpha):
        bg_r = ((bg_color >> 11) & 0x1F) * 255 // 31
        bg_g = ((bg_color >> 5) & 0x3F) * 255 // 63
        bg_b = (bg_color & 0x1F) * 255 // 31

        fg_r = ((fg_color >> 11) & 0x1F) * 255 // 31
        fg_g = ((fg_color >> 5) & 0x3F) * 255 // 63
        fg_b = (fg_color & 0x1F) * 255 // 31

        blend_r = round(fg_r * alpha + bg_r * (1 - alpha))
        blend_g = round(fg_g * alpha + bg_g * (1 - alpha))
        blend_b = round(fg_b * alpha + bg_b * (1 - alpha))

        blend_rgb565 = ((blend_r * 31 // 255) << 11) | ((blend_g * 63 // 255) << 5) | (blend_b * 31 // 255)
        return blend_rgb565
    
    @micropython.viper
    def translucent_rect(self, x:int, y:int, w:int, h:int, color:int, alpha:int):
        width = int(self.width)
        buf = ptr8(self.buffer)
        r_color = (color >> 11) & 0x1F
        g_color = (color >> 5) & 0x3F
        b_color = color & 0x1F
        inv_alpha = 255 - alpha
        for i in range(w):
            for j in range(h):
                index = ((y + j) * width + (x + i)) * 2
                bg_color = (buf[index] << 8) | buf[index + 1]
                r_bg = (bg_color >> 11) & 0x1F
                g_bg = (bg_color >> 5) & 0x3F
                b_bg = bg_color & 0x1F
                blended_r = (r_bg * inv_alpha + r_color * alpha) >> 8
                blended_g = (g_bg * inv_alpha + g_color * alpha) >> 8
                blended_b = (b_bg * inv_alpha + b_color * alpha) >> 8
                if blended_r < 0:
                    blended_r = 0
                elif blended_r > 31:
                    blended_r = 31
                if blended_g < 0:
                    blended_g = 0
                elif blended_g > 63:
                    blended_g = 63
                if blended_b < 0:
                    blended_b = 0
                elif blended_b > 31:
                    blended_b = 31
                blended_color = (int(blended_r) << 11) | (int(blended_g) << 5) | int(blended_b)
                buf[index] = (blended_color >> 8) & 0xFF  # High byte
                buf[index + 1] = blended_color & 0xFF      # Low byte

class QMI8658():
    def __init__(self, address=0X6B):
        self._address = address
        self._bus = I2C(id=1, scl=Pin(I2C_SDL), sda=Pin(I2C_SDA), freq=100_000)
        bRet = self.WhoAmI()
        if bRet:
            self.Read_Revision()
        else:
            return None  # Return None if the sensor is not recognized
        self.Config_apply()  # Apply the default configuration settings

    def _read_byte(self, cmd):
        rec = self._bus.readfrom_mem(int(self._address), int(cmd), 1)
        return rec[0]

    def _read_block(self, reg, length=1):
        rec = self._bus.readfrom_mem(int(self._address), int(reg), length)
        return rec

    def _read_u16(self, cmd):
        LSB = self._bus.readfrom_mem(int(self._address), int(cmd), 1)
        MSB = self._bus.readfrom_mem(int(self._address), int(cmd) + 1, 1)
        return (MSB[0] << 8) + LSB[0]

    def _write_byte(self, cmd, val):
        self._bus.writeto_mem(int(self._address), int(cmd), bytes([int(val)]))

    def WhoAmI(self):
        bRet = False
        if (0x05) == self._read_byte(0x00):  # Compare with expected value
            bRet = True
        return bRet

    def Read_Revision(self):
        return self._read_byte(0x01)

    def Config_apply(self):
        # Set control registers with predefined values
        self._write_byte(0x02, 0x60)  # REG CTRL1
        self._write_byte(0x03, 0x23)  # REG CTRL2: Accelerometer settings
        self._write_byte(0x04, 0x53)  # REG CTRL3: Gyroscope settings
        self._write_byte(0x05, 0x00)  # REG CTRL4: No specific configuration
        self._write_byte(0x06, 0x11)  # REG CTRL5: Enable low-pass filter
        self._write_byte(0x07, 0x00)  # REG CTRL6: Disable motion on demand
        self._write_byte(0x08, 0x03)  # REG CTRL7: Enable gyro and accelerometer

    def Read_Raw_XYZ(self):
        xyz = [0, 0, 0, 0, 0, 0]
        raw_timestamp = self._read_block(0x30, 3)  # Read timestamp
        raw_acc_xyz = self._read_block(0x35, 6)   # Read accelerometer data
        raw_gyro_xyz = self._read_block(0x3b, 6)   # Read gyroscope data
        raw_xyz = self._read_block(0x35, 12)  # Read combined data
        
        # Combine raw timestamp into a single value
        timestamp = (raw_timestamp[2] << 16) | (raw_timestamp[1] << 8) | (raw_timestamp[0])
        
        for i in range(6):
            xyz[i] = (raw_xyz[(i * 2) + 1] << 8) | raw_xyz[i * 2]
            if xyz[i] >= 32767:
                xyz[i] = xyz[i] - 65535  # Adjust for signed values
        return xyz

    def Read_XYZ(self):
        xyz = [0, 0, 0, 0, 0, 0]
        raw_xyz = self.Read_Raw_XYZ()  # Get raw data
        
        # Constants for calibration based on sensor specifications
        acc_lsb_div = (1 << 12)  # For accelerometer
        gyro_lsb_div = 64  # For gyroscope
        
        for i in range(3):
            xyz[i] = raw_xyz[i] / acc_lsb_div  # Calibrate accelerometer data
            xyz[i + 3] = raw_xyz[i + 3] * 1.0 / gyro_lsb_div  # Calibrate gyroscope data
        return xyz

    def Read_Mag_XYZ(self):
        mag_xyz = [0, 0, 0]  # Initialize magnetometer values
        raw_mag_xyz = self._read_block(0x3C, 6)  # Read raw magnetometer data
        
        for i in range(3):
            mag_xyz[i] = (raw_mag_xyz[(i * 2) + 1] << 8) | raw_mag_xyz[i * 2]
            if mag_xyz[i] >= 32767:
                mag_xyz[i] -= 65536  # Adjust for signed values
        return mag_xyz

    def Calculate_Heading(self):
        mag_xyz = self.Read_Mag_XYZ()  # Get magnetometer data
        mag_x, mag_y = mag_xyz[0], mag_xyz[1]

        heading = math.atan2(mag_y, mag_x) * (180 / math.pi)  # Convert radians to degrees
        if heading < 0:
            heading += 360  # Normalize to 0-360 degrees
        return heading

    def Read_Temperature(self):
        raw_temp = self._read_u16(0x3F)  # Replace with the actual temperature register address
        # Convert the raw temperature value to degrees Celsius
        temperature = raw_temp * 0.1  # Example conversion; check the datasheet for the exact formula
        return temperature
    
class Sprite:

    def __init__(self, name, screen):
        self.width = 0
        self.height = 0
        self.posX = 0  # Initialize X position
        self.posY = 0  # Initialize Y position
        self.buffer = bytearray()  # Buffer to store pixel data
        self.isBackup = False  # Flag to indicate if background is backed up
        self.posXprev = 0  # Previous X position
        self.posYprev = 0  # Previous Y position
        self.back = bytearray()  # Buffer to hold background pixel data
        self.screen = screen  # Screen object for drawing the sprite
        self.load(name)  # Load the sprite data from the file

    def load(self, file_name: str):
        with open(file_name, 'rb') as f:
            # Read the 4-byte header in one go and calculate width and height
            header = f.read(4)
            self.width = (header[0] << 8) | header[1]
            self.height = (header[2] << 8) | header[3]

            # Initialize the buffer for the sprite and background with expected size
            buffer_size = self.height * self.width * 2  # 2 bytes per pixel
            self.buffer = bytearray(buffer_size)
            self.back = bytearray(buffer_size)

            # Read the pixel data directly into the buffer
            data = f.read(buffer_size)

            # Check if loaded data size matches the expected size
            if len(data) != buffer_size:
                print(f"Warning: Loaded data size {len(data)} does not match expected size {buffer_size}.")

            # Copy the data into the sprite buffer
            self.buffer[:len(data)] = data
   
    def move(self, deltaX, deltaY):
        self.posXprev = self.posX  # Save current position for restoration
        self.posYprev = self.posY
        self.posX += deltaX  # Update X position
        self.posY += deltaY  # Update Y position
        
    def move_to(self, toX, toY):
        self.posXprev = self.posX  # Save current position for restoration
        self.posYprev = self.posY
        self.posX = toX  # Update to the new X position
        self.posY = toY  # Update to the new Y position
    
    @micropython.viper
    def restore(self):
        if self.isBackup:
            back_buf = ptr8(self.back)  # Pointer to the backup buffer
            screen_buf = ptr8(self.screen.buffer)  # Pointer to the screen buffer
            width = int(self.width)
            height = int(self.height)
            screen_width = int(self.screen.width)
            screen_height = int(self.screen.height)
            pos_x_prev = int(self.posXprev)
            pos_y_prev = int(self.posYprev)
        
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
    def backup(self):
        back_buf = ptr8(self.back)  # Pointer to the backup buffer
        screen_buf = ptr8(self.screen.buffer)  # Pointer to the screen buffer
        width = int(self.width)
        height = int(self.height)
        screen_width = int(self.screen.width)
        screen_height = int(self.screen.height)        
        pos_x = int(self.posX)
        pos_y = int(self.posY)
        
        for y in range(height):
            for x in range(width):
                screen_x = pos_x + x
                screen_y = pos_y + y
                # Ensure the sprite fits within the screen boundaries
                if 0 <= screen_x < screen_width and 0 <= screen_y < screen_height:
                    screen_index = (screen_y * screen_width + screen_x) * 2
                    sprite_index = (y * width + x) * 2
                    # Backup the current screen pixel data
                    back_buf[sprite_index] = screen_buf[screen_index]  # High byte
                    back_buf[sprite_index + 1] = screen_buf[screen_index + 1]  # Low byte
        self.isBackup = True  # Set backup flag to true
    
    @micropython.viper
    def draw(self):
        buffer = ptr8(self.buffer)  # Pointer to the sprite's pixel data
        screen_buf = ptr8(self.screen.buffer)  # Pointer to the screen buffer
        width = int(self.width)
        height = int(self.height)
        screen_width = int(self.screen.width)
        screen_height = int(self.screen.height)
        pos_x = int(self.posX)
        pos_y = int(self.posY)
        
        for y in range(height):
            for x in range(width):
                screen_x = pos_x + x
                screen_y = int(pos_y + y)
                # Ensure the sprite fits within the screen boundaries
                if 0 <= screen_x < screen_width and 0 <= screen_y < screen_height:
                    # Read color from the sprite buffer
                    sprite_index = (y * width + x) * 2
                    sprite_color = (buffer[sprite_index] << 8) | buffer[sprite_index + 1]
                    # Check for transparency using the key color (assuming key color is the same for all transparent pixels)
                    if sprite_color != 0xF81F:  # Key color for transparency
                        # Draw the sprite pixel
                        screen_index = (screen_y * screen_width + screen_x) * 2
                        screen_buf[screen_index] = buffer[sprite_index]  # High byte
                        screen_buf[screen_index + 1] = buffer[sprite_index + 1]  # Low byte

class Battery:
    # Define voltage thresholds as class constants
    _FULLY_CHARGED_VOLTAGE = const(4.2)
    _HALF_CHARGED_VOLTAGE = const(3.7)
    _EMPTY_VOLTAGE = const(3.0)
    
    def __init__(self):
        self.Vbat= ADC(Pin(Vbat_Pin))
    
    def volts(self):
        return self.Vbat.read_u16()*3.3/65535*2
    
    def level(self):
        volts = self.volts()
        if volts >= _FULLY_CHARGED_VOLTAGE:
            return 100  # Fully charged
        elif volts >= _HALF_CHARGED_VOLTAGE:
            # Calculate percentage between 50% and 100%
            return int((volts - 3.7) / (4.2 - 3.7) * 50 + 50)
        elif volts >= _EMPTY_VOLTAGE:
            # Calculate percentage between 0% and 50%
            return int((volts - 3.0) / (3.7 - 3.0) * 50)
        else:
            return 0  # Fully discharged or below 3.0V
        
class Buttons:
    
    def __init__(self):
        self.s1 = Pin(S1, Pin.IN, Pin.PULL_DOWN)
        self.s2 = Pin(S2, Pin.IN, Pin.PULL_DOWN)
        self.s3 = Pin(S3, Pin.IN, Pin.PULL_DOWN)
        
    def isPressed(self):
        s1 = self.s1.value()
        s2 = self.s2.value()
        s3 = self.s3.value()
        return (s3 << 2) | (s2 << 1) | s1

class ButtonsIRQ:
    def __init__(self):
        # Initialize the buttons with pins
        self.s1 = Pin(17, Pin.IN, Pin.PULL_DOWN)  # S1
        self.s2 = Pin(18, Pin.IN, Pin.PULL_DOWN)  # S2
        self.s3 = Pin(16, Pin.IN, Pin.PULL_DOWN)  # S3 (for sleep/wakeup)

    # Method to enable interrupt for S1 with dynamic handler assignment
    def enable_s1_interrupt(self, action):
        self.s1.irq(trigger=Pin.IRQ_RISING, handler=action)

    # Method to enable interrupt for S2 with dynamic handler assignment
    def enable_s2_interrupt(self, action):
        self.s2.irq(trigger=Pin.IRQ_RISING, handler=action)

    # Method to enable interrupt for S3 with dynamic handler assignment
    def enable_s3_interrupt(self, action):
        self.s3.irq(trigger=Pin.IRQ_RISING, handler=action)

    # Method to disable interrupt for S1
    def disable_s1_interrupt(self):
        self.s1.irq(handler=None)

    # Method to disable interrupt for S2
    def disable_s2_interrupt(self):
        self.s2.irq(handler=None)

    # Method to disable interrupt for S3
    def disable_s3_interrupt(self):
        self.s3.irq(handler=None)

if __name__=='__main__':
    LCD = GC9A01()
    LCD.set_bl_pwm(65535) # to maximum! (TODO: play to change brightness)
    buttons = Buttons()
    battery = Battery()
    volts = battery.volts()
    level = battery.level()
    LCD.fill(LCD.black)
    LCD.fill_rect(0,0,240,40,LCD.red)
    LCD.text("RP2040-LCD-1.28",60,25,LCD.green)
    LCD.text(f"Bat.: {level:.0f}% ({volts:.2f}V)",40,55,LCD.white)
    LCD.text("MicroPython GC9A01",30,90,LCD.green)
    LCD.text("MicroPython QMI8658",30,100,LCD.green)
    LCD.text("MicroPython Sprite",30,110,LCD.green)
    LCD.text("MicroPython Battery",30,120,LCD.green)
    LCD.text("(C) 2024, Nicholas Schreiner",10,145,LCD.green)
    gc.collect()
    sprite = Sprite("/images/python_100x60.rgba565", LCD)
    sprite.move(int((LCD.width - sprite.width)/2),165)
    gc.collect()
    while True:
        volts = battery.volts()
        level = battery.level()
        
        # Update battery display
        LCD.fill_rect(0, 51,240,16,LCD.blue)
        LCD.text(f"Bat.: {level:3.0f}% ({volts:4.2f}V)",40,55,LCD.white)
        
        b_state = buttons.isPressed()
        if b_state < 7: # one or combinations of keys are pressed
            if (b_state & 0b00000110) == 0: # S3 + S2
                step_x = 3
                step_y = 0
            elif (b_state & 0b00000001) == 0: # S1
                step_x = -3
                step_y = 0
            elif (b_state & 0b00000010) == 0: # S2
                step_x = 0
                step_y = 3
            elif (b_state & 0b00000100) == 0: # S3
                step_x = 0
                step_y = -3
        else:
            # Apply random offset to sprite position
            step_x = random.randint(-1, 1)
            step_y = random.randint(-1, 1)
        
        # Check screen boundaries for the sprite's next position
        next_x = sprite.posX + step_x
        next_y = sprite.posY + step_y
    
        # Apply boundary checks
        if next_x < 0:
            step_x = 0
        elif next_x > LCD.width - sprite.width:
            #step_x = LCD.width - sprite.width - sprite.posX
            step_x = 0
    
        if next_y < 67:
            step_y = 0
        elif next_y > LCD.height - sprite.height:
            #step_y = LCD.height - sprite.height - sprite.posY
            step_y = 0
        
        # Draw and move the sprite
        sprite.restore()
        sprite.backup()    
        sprite.draw()
        sprite.move(step_x, step_y) 
        LCD.show()
        #time.sleep(0.5)

    