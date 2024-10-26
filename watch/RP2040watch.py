"""
===
= RP2040 LCD 1.28 GC9A01 IMU, QMIC88658 MicroPython library
===

Type:      lib
Author:    Nicholas Schreiner a.k.a. LighthunterWS
Revision:  0.1.0 PA

Hardware: Raspberry Pi RP2040 watch development board with 1.28-inch GC9A01 round watch TFT display IMU on the board as a QMIC88658

""" 

from machine import Pin,I2C,SPI,PWM,ADC
import framebuf
import time

# RP2040 pins toward GC9A01 display
DC = 8
CS = 9
SCK = 10
MOSI = 11
RST = 12

BL = 25


#Keys
S1 = 17
S2 = 18
S3 = 16


I2C_SDA = 6
I2C_SDL = 7

Vbat_Pin = 29

# Orientation
NORTH = 0
EAST = 1
WEST = 2
SOUTH = 3

# RP2040 pins toward GC9A01 buttons
S1 = 17 # set/mode       0 1 0 0 1 1 1
S2 = 18 # up/forward     0 0 1 0 1 0 1
S3 = 16 # down/backward  0 0 0 1 0 1 1


#
#  1.28-inch GC9A01 round watch TFT display driver
#
class GC9A01 (framebuf.FrameBuffer):
    
    """
    Constructor
    """  
    def __init__(self):
        self.width = 240
        self.height = 240
        
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
        
        
    """
    Initialize dispaly
    """  
    def init(self):
        self.rst(1)
        time.sleep(0.01)
        self.rst(0)
        time.sleep(0.01)
        self.rst(1)
        time.sleep(0.05)
        """Inner register enable 2"""
        self.write_cmd(0xEF)
        self.write_cmd(0xEB) # What the hel EBh is?
        self.write_data(0x14)
        """Inner register enable 1"""
        self.write_cmd(0xFE)
        """Inner register enable 2"""
        self.write_cmd(0xEF)
        self.write_cmd(0xEB) # What the hel EBh is?
        self.write_data(0x14) 
        """ TODO: find what is it (commands from 84h to 8Fh)"""
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
        
        """ Display Function Control """
        #self.write_cmd(0xB6)
        #self.write_data(0x00)  # first parameter 00h
        #self.write_data(0x00)  # second parameter 0010 0000
                               #                   ^^
                               #                   ||
                               #                   |+--- SS Select the shift direction of outputs from the source driver:
                               #                   |        R, G, B dots to the source driver pins from S360 to S1, set SS = 1.
                               #                   +---- GS Sets the direction of scan by the gate driver in the range determined by
                               #                         SCN [4:0] and NL [4:0]:
                               #                            scan direction G1→G32
                               # Note: 0x00 left to right, 0x20 right to left
       
        """ Memory access control """
        #self.write_cmd(0x36)   # a.k.a. orientation
        #self.write_data(0x28)  # 00101000
                               # ^^^^^^
                               # ||||||
                               # |||||+--- MH  Horizontal Refresh ORDER
                               # ||||+---- BGR RGB-BGR Order. Color selector switch control (0=RGB color filter panel, 1=BGR color filter panel)
                               # |||+----- ML  Vertical Refresh Order. LCD vertical refresh direction control.
                               # ||+------ MV  Row / Column Exchange
                               # |+------- MX  Column Address Order
                               # +-------- MY  Row Address Order
                               #
                               # MY, MX, MV - These 3 bits control MCU to memory write/read direction.
                               
        """ COLMOD: Pixel Format Set """
        self.write_cmd(0x3A)   # Sets the pixel format for the RGB image data used by the interface. DPI [2:0] is
                               # the pixel format select of RGB interface and DBI [2:0] is the pixel format of MCU interface.
        self.write_data(0x05)  # 00000101
                               #  \ / \ /
                               #   ^   ^
                               #   |   |
                               #   |   +--- DBI [2:0]: 1 0 1 (16 bits / pixel)
                               #   +------- DPI [2:0]: 0 0 0 (reserved)
                            
        """ TODO: find what is it... hell knows what the 90h command is - not documented"""
        self.write_cmd(0x90)
        self.write_data(0x08)
        self.write_data(0x08)
        self.write_data(0x08)
        self.write_data(0x08)
        
        """ TODO: find what is it... hell knows what the BDh command is - not documented"""
        self.write_cmd(0xBD)
        self.write_data(0x06)
        """ TODO: find what is it... hell knows what the BCh command is - not documented"""
        self.write_cmd(0xBC)
        self.write_data(0x00)
        """ TODO: find what is it... hell knows what the FFh command is - not documented"""
        self.write_cmd(0xFF)        
        self.write_data(0x60)
        self.write_data(0x01)
        self.write_data(0x04)

        """ Power Control 2 """
        self.write_cmd(0xC3)  # Set the voltage level value to output the VREG1A and VREG1B OUT level, which is a
                              # reference level for the grayscale voltage level.(Table is valid when vrh=0x28)
                              # VREG1A=(vrh+vbp_d)*0.02+4
                              # VREG1B=vbp_d*0.02+0.3
        self.write_data(0x13) # 00010011
                              # x^^^^^^^ 
                              #  |||||||
                              #  +++++++--- vreg1_vbp_d[6:0]
                              
        """ Power Control 3 """
        self.write_cmd(0xC4)  # Set the voltage level value to output the VREG2A OUT level, which is a reference level for
                              # the grayscale voltage level(Table is valid when vrh=0x28)
        self.write_data(0x13) # 00010011
                              # x^^^^^^^ 
                              #  |||||||
                              #  +++++++--- vreg1_vbn_d[6:0]

        """ Power Control 4 """
        self.write_cmd(0xC9)  # Set the voltage level value to output the VREG1A OUT level, which is a reference level for
                              # the grayscale voltage level. (Table is valid when vbp_d=0x3C and vbn_d=0x3C)
        self.write_data(0x22) # 00100010
                              # xx^^^^^^ 
                              #   ||||||
                              #   ++++++--- vrh[5:0]
                              
        """ TODO: find what is it... hell knows what the BEh command is - not documented"""
        self.write_cmd(0xBE)
        self.write_data(0x11) 

        """ TODO: find what is it... hell knows what the E1h command is - not documented"""
        self.write_cmd(0xE1)
        self.write_data(0x10)
        self.write_data(0x0E)

        """ TODO: find what is it... hell knows what the DFh command is - not documented"""
        self.write_cmd(0xDF)
        self.write_data(0x21)
        self.write_data(0x0c)
        self.write_data(0x02)

        """ SET_GAMMA1 """
        self.write_cmd(0xF0)   
        self.write_data(0x45)
        self.write_data(0x09)
        self.write_data(0x08)
        self.write_data(0x08)
        self.write_data(0x26)
        self.write_data(0x2A)

        """ SET_GAMMA2 """
        self.write_cmd(0xF1)    
        self.write_data(0x43)
        self.write_data(0x70)
        self.write_data(0x72)
        self.write_data(0x36)
        self.write_data(0x37)  
        self.write_data(0x6F)

        """ SET_GAMMA3 """
        self.write_cmd(0xF2)   
        self.write_data(0x45)
        self.write_data(0x09)
        self.write_data(0x08)
        self.write_data(0x08)
        self.write_data(0x26)
        self.write_data(0x2A)

        """ SET_GAMMA4 """
        self.write_cmd(0xF3)   
        self.write_data(0x43)
        self.write_data(0x70)
        self.write_data(0x72)
        self.write_data(0x36)
        self.write_data(0x37) 
        self.write_data(0x6F)

        """ TODO: find what is it... hell knows what the EDh command is - not documented"""
        self.write_cmd(0xED)
        self.write_data(0x1B) 
        self.write_data(0x0B) 

        """ TODO: find what is it... hell knows what the AEh command is - not documented"""
        self.write_cmd(0xAE)
        self.write_data(0x77)
        
        """ TODO: find what is it... hell knows what the CDh command is - not documented"""
        self.write_cmd(0xCD)
        self.write_data(0x63)

        """ TODO: find what is it... hell knows what the 70h command is - not documented"""
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

        """ Frame Rate """
        self.write_cmd(0xE8)  # 
        self.write_data(0x34) # 00110100

        """ TODO: find what is it... hell knows what the 62h command is - not documented"""
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

        """ TODO: find what is it... hell knows what the 63h command is - not documented"""
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

        """ TODO: find what is it... hell knows what the 64h command is - not documented"""
        self.write_cmd(0x64)
        self.write_data(0x28)
        self.write_data(0x29)
        self.write_data(0xF1)
        self.write_data(0x01)
        self.write_data(0xF1)
        self.write_data(0x00)
        self.write_data(0x07)

        """ TODO: find what is it... hell knows what the 66h command is - not documented"""
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

        """ TODO: find what is it... hell knows what the 67h command is - not documented"""
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

        """ TODO: find what is it... hell knows what the 74h command is - not documented"""
        self.write_cmd(0x74)
        self.write_data(0x10)
        self.write_data(0x85)
        self.write_data(0x80)
        self.write_data(0x00) 
        self.write_data(0x00) 
        self.write_data(0x4E)
        self.write_data(0x00)
        
        """ TODO: find what is it... hell knows what the 98h command is - not documented"""
        self.write_cmd(0x98)
        self.write_data(0x3e)
        self.write_data(0x07)

        """ Tearing Effect Line ON """
        self.write_cmd(0x35)  # This command is used to turn ON the Tearing Effect output signal from the TE signal line.
        self.write_cmd(0x21)  # 00100001
                              # xxxxxxx^
                              #        |
                              #        +--- M=0: The Tearing Effect Output line consists of V-Blanking information only
                              #             M=1: The Tearing Effect Output Line consists of both V-Blanking and H-Blanking information
                              # TODO: bit D5 supposed to be 0 but not 1 (why 1 is here?)

        """ Sleep Out Mode """
        self.write_cmd(0x11)  # This command turns off sleep mode. the DC/DC converter is enabled, Internal oscillator is started, and panel scanning is started.
                              # a.k.a. wake up
        time.sleep(0.12)      # ... and wait a bit while waking up
        
        """ Display ON """
        self.write_cmd(0x29)  # This command is used to recover from DISPLAY OFF mode. Output from the Frame
                              # Memory is enabled.
                              # This command makes no change of contents of frame memory.
                              # This command does not change any other status.
        time.sleep(0.02)      # ... and wait a bit
        
        """ Display Inversion ON """
        self.write_cmd(0x21)  # This command is used to enter into display inversion mode.
                              # This command makes no change of the content of frame memory. Every bit is inverted from
                              # the frame memory to the display.
                              # This command doesn’t change any other status.
                              # To exit Display inversion mode, the Display inversion OFF command (20h) should be written.
                              
        """ Sleep Out Mode """
        self.write_cmd(0x11)  # Wake up again (see description above)

        """ Display ON """
        self.write_cmd(0x29)  # ... and display On again (see description above)
    
    """
    Brightness controll PWM
    """
    def set_bl_pwm(self,duty):
        self.pwm.duty_u16(duty)#max 65535

    """
    Write command
    """  
    def write_cmd(self, cmd):
        self.cs(1)
        self.dc(0)
        self.cs(0)
        self.spi.write(bytearray([cmd]))
        self.cs(1)

    """
    Write data
    """  
    def write_data(self, buf):
        self.cs(1)
        self.dc(1)
        self.cs(0)
        self.spi.write(bytearray([buf]))
        self.cs(1)
        
    
    """ TODO: make universal write flexible arguments cmd and data"""
    def _write(self, cmd, data):
        self.cs(1)
        if cmd:
            self.dc(0)
            self.cs(0)
            self.spi.write(bytearray([cmd]))
            self.cs(1)
        if data:
            self.dc(1)
            self.cs(0)
            self.spi.write(bytearray([data])) 
        
    """
    Show content
    """
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
        
    """
    Display Brightness Wright (51H)
    """
    def brightness(self, dimm):
        # dimm from 0x00 to 0xFF
        self.write_cmd(0x51)
        self.write_data(dimm)
       
    """
    Display ON/OFF (29H, 28H)
    """
    def display(self,on):
        if on:
            self.write_cmd(0x29)  # Display ON (recovery after Display OFF, command 28h)
        else:
            self.write_cmd(0x28)  # Display OFF (command 28h) In this mode, the output from
                                  # Frame Memory is disabled and blank page inserted.
                                  # This command makes no change of contents of frame memory.
                                  # This command does not change any other status.
                                  # There will be no abnormal visible effect on the display.
    """
    Display Inversion ON/OFF (21H, 20H)
    """
    def invert(self,on):
        if on:
            self.write_cmd(0x21)  # Display Inversion ON
                                  # This command is used to enter into display inversion mode.
                                  # This command makes no change of the content of frame memory. Every bit is inverted from
                                  # the frame memory to the display.
                                  # This command doesn’t change any other status.
                                  # To exit Display inversion mode, the Display inversion OFF command (20h) should be
                                  # written.
        else:
            self.write_cmd(0x20)  # Display Inversion OFF
                                  # This command is used to recover from display inversion mode.
                                  # This command makes no change of the content of frame memory.
                                  # This command doesn’t change any other status.
        
    """
    Rotate screen
    """  
    def orient(self, direction):
        # NORTH by default
        dfc_param = 0x00
        mac_param = 0b00101000 # 0x28
                    # 01001000
                    # 10001000
                    # 10101000
        
        if direction == EAST:
            dfc_param = 0x00
            mac_param = 0b10001000
        elif direction == SOUTH:
            dfc_param = 0x00
            mac_param = 0b11101000 
        elif direction == WEST:
            dfc_param = 0x00
            mac_param = 0b01001000
            
        """ Display Function Control """
        self.write_cmd(0xB6)
        self.write_data(0x00)  # first parameter 00h
        self.write_data(dfc_param)  # second parameter 0010 0000
                               #                   ^^
                               #                   ||
                               #                   |+--- SS Select the shift direction of outputs from the source driver:
                               #                   |        R, G, B dots to the source driver pins from S360 to S1, set SS = 1.
                               #                   +---- GS Sets the direction of scan by the gate driver in the range determined by
                               #                         SCN [4:0] and NL [4:0]:
                               #                            scan direction G1→G32
                               # Note: 0x00 left to right, 0x20 right to left
       
        """ Memory access control """
        self.write_cmd(0x36)   # a.k.a. orientation
        self.write_data(mac_param)
                               # 00101000
                               # 11000000 0xCO
                               # 10100000 0xAO
                               # 01100000 0x60
                               # ^^^^^^
                               # ||||||
                               # |||||+--- MH  Horizontal Refresh ORDER
                               # ||||+---- BGR RGB-BGR Order. Color selector switch control (0=RGB color filter panel, 1=BGR color filter panel)
                               # |||+----- ML  Vertical Refresh Order. LCD vertical refresh direction control.
                               # ||+------ MV  Row / Column Exchange
                               # |+------- MX  Column Address Order
                               # +-------- MY  Row Address Order
                               #
                               # MY, MX, MV - These 3 bits control MCU to memory write/read direction.

    """
    Load 16bit color image as background to FrameBuffer from binary file
    Note 1: 16bit color JPG or PNG file (convert in GIMP from 8bit to 16bit if necessary)
            must be converted into RGB565 binary file (use PIL or similar)
    Note 2: background size is 240x240 pixels
    Note 3: function loads file as is to FrameBuffer's buffer as is, all bugs are bugs in
            image preparation process (see, Note 1 and Note 2)
    """
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
                
    """
    Set of function for blending colors
    Goal: translucent foregraound graphical elements. Cool staff!!!
    """
    
    # Function to blend two RGB565 colors
    # Note: failed, produces garbage (incorrect colors adjustment)
    #def blend_colors(self, bg_color, fg_color, opacity):
    #    # Extract RGB components from 16-bit colors
    #    bg_r = (bg_color >> 11) & 0x1F
    #    bg_g = (bg_color >> 5) & 0x3F
    #    bg_b = bg_color & 0x1F
    #    fg_r = (fg_color >> 11) & 0x1F
    #    fg_g = (fg_color >> 5) & 0x3F
    #    fg_b = fg_color & 0x1F
    #    # Blend each component
    #   new_r = int(bg_r * (1 - opacity) + fg_r * opacity)
    #    new_g = int(bg_g * (1 - opacity) + fg_g * opacity)
    #    new_b = int(bg_b * (1 - opacity) + fg_b * opacity)
    #    # Return the new RGB565 color
    #    return (new_r << 11) | (new_g << 5) | new_b
    
    """
    convert standard RGB(255,255,255) into RGB565 16bits format
    """
    def color(self, red, green, blue):
        # red, green and blue are 8 bits in range [0..255]
        #goal: scale red 8 bits to 5 bits
        #      scale green 8 bits to 6 bits
        #      scale blue 8 bits to 5 bits
        r_5 = red >> 3      # Scale red to 5 bits
        g_6 = green >> 2      # Scale green to 6 bits
        b_5 = blue >> 3      # Scale blue to 5 bits
        # Combine into a single 16-bit value
        return (r_5 << 11) | (g_6 << 5) | b_5
        #return (b_5 << 11) | (r_5 << 5) | g_6
        #return (r_5 << 11) | (b_5 << 5) | g_6
        #return (b_5 << 11) | (g_6 << 5) | r_5
    
    def rgb565_to_rgb888(self, rgb565):
        # Extract red, green, and blue components
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
        # Extract RGB components from RGB565 (scale to 8 bits)
        bg_r = ((bg_color >> 11) & 0x1F) * 255 // 31
        bg_g = ((bg_color >> 5) & 0x3F) * 255 // 63
        bg_b = (bg_color & 0x1F) * 255 // 31

        fg_r = ((fg_color >> 11) & 0x1F) * 255 // 31
        fg_g = ((fg_color >> 5) & 0x3F) * 255 // 63
        fg_b = (fg_color & 0x1F) * 255 // 31

        # Blend each channel with floating-point precision
        blend_r = round(fg_r * alpha + bg_r * (1 - alpha))
        blend_g = round(fg_g * alpha + bg_g * (1 - alpha))
        blend_b = round(fg_b * alpha + bg_b * (1 - alpha))

        # Convert back to RGB565 with careful rounding
        blend_rgb565 = ((blend_r * 31 // 255) << 11) | ((blend_g * 63 // 255) << 5) | (blend_b * 31 // 255)
        return blend_rgb565

    
    # Draw a translucent rectangle
    def translucent_rect(self, x, y, w, h, color, alpha):
        start_time = time.ticks_ms() 
        for i in range(x, x + w):
            for j in range(y, y + h):
                # Get the background color at (i, j)
                bg_color = self.getPixel(i, j)
                # Blend it with the rectangle color
                blended_color = self.blend_colors(bg_color, color, alpha)
                # Draw the blended color
                self.setPixel(i, j, blended_color)
        end_time = time.ticks_ms()  # End timing
        elapsed_time = time.ticks_diff(end_time, start_time)  # Calculate the elapsed time
        print("Time taken to draw translucent rectangle: {} ms".format(elapsed_time))
        
    @micropython.viper
    def translucent_rect_optimized(self, x:int, y:int, w:int, h:int, color:int, alpha:int):
        start_time = time.ticks_ms()  # Start timing
        width = int(self.width)
        buf = ptr8(self.buffer)
        
        # Color components for blending
        r_color = (color >> 11) & 0x1F
        g_color = (color >> 5) & 0x3F
        b_color = color & 0x1F
        
        # Precompute alpha and inverse alpha for faster blending
        inv_alpha = 255 - alpha
        
        # Calculate the blended colors for the rectangle
        for i in range(w):
            for j in range(h):
                # Calculate the background pixel index
                index = ((y + j) * width + (x + i)) * 2
            
                # Get the current background color
                #bg_color = (self.buffer[index] << 8) | self.buffer[index + 1]
                
                # Extract the background color directly from the buffer
                bg_color = (buf[index] << 8) | buf[index + 1]
                
                # Extract background color components
                r_bg = (bg_color >> 11) & 0x1F
                g_bg = (bg_color >> 5) & 0x3F
                b_bg = bg_color & 0x1F
                
                # Blend color components using fixed-point math
                blended_r = (r_bg * inv_alpha + r_color * alpha) >> 8
                blended_g = (g_bg * inv_alpha + g_color * alpha) >> 8
                blended_b = (b_bg * inv_alpha + b_color * alpha) >> 8
                
                # Manually clamp values within RGB565 limits
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
                    
                # Create the new blended RGB565 color
                blended_color = (int(blended_r) << 11) | (int(blended_g) << 5) | int(blended_b)

                # Write the blended color back into the buffer
                buf[index] = (blended_color >> 8) & 0xFF  # High byte
                buf[index + 1] = blended_color & 0xFF      # Low byte
    
        end_time = time.ticks_ms()  # End timing
        elapsed_time = time.ticks_diff(end_time, start_time)  # Calculate the elapsed time
        print("Time taken to draw translucent rectangle (optimized): {} ms".format(elapsed_time))
        return elapsed_time

        
        
if __name__=='__main__':
    LCD = GC9A01()
    LCD.set_bl_pwm(65535) # to maximum! (TODO: play to change brightness)
    LCD.fill(LCD.black)
    LCD.fill_rect(0,0,240,40,LCD.red)
    LCD.text("RP2040-LCD-1.28",60,25,LCD.green)
    
    LCD.show()