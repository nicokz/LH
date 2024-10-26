"""
===
= RP2040 LCD 1.28 screen rotation
===

Type:      code example
Author:    Nicholas Schreiner a.k.a. LighthunterWS
Revision:  0.1.0 PA
"""
import watch.RP2040watch as Watch
import time

LCD = Watch.GC9A01() # init GC9A01
LCD.set_bl_pwm(65535) # to maximum! (TODO: play to change brightness)

def test01_screen_orientation():
    global LCD
    LCD.show()
    time.sleep(2)
    LCD.fill(LCD.black)
    LCD.text("TEST 1: Screen orinetation",10,116,LCD.white)
    LCD.show()
    time.sleep(3)
    LCD.fill(LCD.black)
    LCD.vline(120, 45, 180, 0xffff)
    LCD.line(120, 45, 117, 55, 0xffff)
    LCD.line(120, 45, 123, 55, 0xffff)
    LCD.hline(115, 120, 10, 0xffff)
    LCD.orient(Watch.NORTH) # rotate NORTH (virtually normal handy watch position)
    LCD.fill_rect(0,0,240,40,LCD.red)
    LCD.text("NORTH",60,25,LCD.green)
    LCD.show()
    time.sleep(0.8)
    LCD.orient(Watch.WEST)
    LCD.fill_rect(0,0,240,40,LCD.red)
    LCD.text("WEST",60,25,LCD.green) # rotate 90 degree to left of NORTH
    LCD.show()
    time.sleep(0.8)
    LCD.orient(Watch.SOUTH)
    LCD.fill_rect(0,0,240,40,LCD.red)
    LCD.text("SOUTH",60,25,LCD.green) # rotate 180 degree out of NORTH (opposit position)
    LCD.show()
    time.sleep(0.8)
    LCD.orient(Watch.EAST)
    LCD.fill_rect(0,0,240,40,LCD.red) # rotate 90 degree to right of NORTH
    LCD.text("EAST",60,25,LCD.green)
    LCD.show()
    time.sleep(0.8)
    LCD.orient(Watch.NORTH)
    LCD.fill_rect(0,0,240,40,0x00FF) # rotate back to NORTH
    LCD.text("NORTH",60,25,0xFF00)
                      #0xffff ?
    LCD.show()
    time.sleep(1)

def test2_display_brightness(delay):
    global LCD
    LCD.fill(LCD.black)
    LCD.text("TEST 2: Brightness ",30,116,LCD.white)
    LCD.show()
    time.sleep(2)
    LCD.brightness(0)

    for bright in range(0,0xFF):
        LCD.fill(LCD.white)
        #LCD.set_bl_pwm(bright)
        LCD.text("Bright: "+str(bright),60,116,LCD.black)
        LCD.show()
        LCD.brightness(bright)
        print("Bright: "+str(bright))
        time.sleep(delay)
    LCD.brightness(0xFF)
    
def test3_display_on_off(delay):
    global LCD
    LCD.fill(LCD.black)
    LCD.text("TEST 3: Disp.On/OFF",30,116,LCD.white)
    LCD.show()
    time.sleep(2)
    LCD.display(False)
    time.sleep(delay)
    LCD.display(True)
    time.sleep(delay)
    LCD.display(False)
    time.sleep(delay)
    LCD.display(True)

def test4_display_inversion_on_off(delay):
    global LCD
    LCD.fill(LCD.black)
    LCD.text("TEST 4: Inversion",30,116,LCD.white)
    LCD.show()
    time.sleep(2)
    LCD.fill(LCD.black)
    LCD.text("Inversion OFF",30,70,LCD.white)
    LCD.fill_rect(0, 90, 60, 60, LCD.white)
    LCD.fill_rect(60, 90, 60, 60, LCD.red)
    LCD.fill_rect(120, 90, 60, 60, LCD.green)
    LCD.fill_rect(180, 90, 60, 60, LCD.blue)
    LCD.show()
    time.sleep(delay)
    LCD.fill_rect(0, 70, 12, 240, LCD.black)
    LCD.text("Inversion ON",30,70,LCD.white)
    LCD.show()
    time.sleep(delay)
    LCD.invert(True)
    LCD.fill_rect(0, 70, 12, 240, LCD.black)
    LCD.text("Inversion OFF",30,70,LCD.white)
    LCD.invert(False)
    LCD.show()
    time.sleep(delay)

LCD.fill(LCD.black)
LCD.fill_rect(0,0,240,40,LCD.red)
LCD.text("RP2040 LCD 1.28",60,25,LCD.green)
LCD.text("GC9A01 COMMANDS TESTS",30,116,LCD.white)
LCD.show()
LCD.fill(LCD.black)
LCD.loadRGB565background('/images/rp2040_bg.rgb565')

#p = LCD.pixel(126,56)
#r,g,b = LCD.rgb565_to_rgb888(p)
#print(f"RGB888: ({r}, {g}, {b})") 
#print(f"pixel original: {p:016b}")

#p = LCD.color(0,0,255)
#LCD.fill_rect(0, 104, 240, 32, LCD.color(0,0,255))
#print(f"pixel in      : {p:016b}")
#p = LCD.pixel(120,120)
#print(f"pixel out     : {p:016b}")

"""
colors = [(0, 0, 255, "B"), (255, 0, 0, "R"), (0, 255, 0, "G"), (255, 255, 0, "Y")]  # Blue, Red, Green, Yellow

rect_width = 20
rect_height = 20

for i, (r, g, b, t) in enumerate(colors):
    p = LCD.color(r, g, b)
    LCD.fill_rectangle(120, 120 + i * (rect_height + 5), rect_width, rect_height, p)
    LCD.text(t,110, 120 + i * (rect_height + 5),LCD.white)
    # Read back and confirm color for the top-left pixel of the rectangle
    #LCD.pixel(120, 120 + i, LCD.color(r,g,b))  # Set different colors to different pixels
    p_out = LCD.getPixel(120, 120+i * (rect_height + 5))
    print(f"Set pixel {i} to RGB({r}, {g}, {b}) - p {p_out:016b}, pixel out: {p_out:016b}")

#LCD.translucent_rect(130, 130, rect_width, (rect_height +5)*4, LCD.color(0,0,0), 0.50)
"""
#LCD.translucent_rect(0, 100, 240, 40, LCD.color(0,0,0), 0.5)
et = LCD.translucent_rect_optimized(0, 100, 240, 40, LCD.color(0,0,0), int(0.5 * 255))
LCD.text(f"OPACITY in {et} ms",30,116,LCD.white)

#with open('output.rgb565', 'rb') as f:
#    pos = 0  # Position in framebuffer's buffer
#    chunk_size = 1024  # Adjust chunk size as needed for memory efficiency
#    while pos < len(LCD.buffer):
#        chunk = f.read(chunk_size)
#        if not chunk:  # End of file
#            break
#        LCD.buffer[pos:pos+len(chunk)] = chunk
#        pos += len(chunk)
        
LCD.show()
 
#test01_screen_orientation()
#time.sleep(5)
#test2_display_brightness(0.1)
#time.sleep(5)
#test3_display_on_off(1)
#time.sleep(5)
#test4_display_inversion_on_off(2)

#LCD.write_cmd(0x53) 
#LCD.write_data(0b00101100)
                #76^4^^10
#LCD.text("GC9A01 BL_PWM",30,126,LCD.white)
#LCD.show()
#for i in range(0,1024):
#    LCD.set_bl_pwm(i)
#    LCD.fill(LCD.black)
#    LCD.text("BL PWN: "+str(i),30,70,LCD.white)
#    LCD.fill_rect(0, 90, 60, 60, LCD.white)
#    LCD.fill_rect(60, 90, 60, 60, LCD.red)
#    LCD.fill_rect(120, 90, 60, 60, LCD.green)
#    LCD.fill_rect(180, 90, 60, 60, LCD.blue)
#    LCD.show()
#   time.sleep(0.5)
#LCD.set_bl_pwm(0)
#time.sleep(1)
#LCD.set_bl_pwm(65535)
#test2_display_brightness(0.1)

#LCD.fill(LCD.black)
#LCD.fill_rect(0,0,240,40,LCD.red)
#LCD.text("RP2040 LCD 1.28",60,25,LCD.green)
#LCD.text("GC9A01 TESTS FINISHED",30,116,LCD.white)
#LCD.show()
#time.sleep(1)
#lLCD.display(False)