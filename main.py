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
time.sleep(5)
#test01_screen_orientation()
#time.sleep(5)
#test2_display_brightness(0.1)
#time.sleep(5)
#test3_display_on_off(1)
#time.sleep(5)
#test4_display_inversion_on_off(2)

LCD.write_cmd(0x53) 
LCD.write_data(0b00101100)
                #76^4^^10
LCD.text("GC9A01 BL_PWM",30,126,LCD.white)
LCD.show()
for i in range(0,1024):
    LCD.set_bl_pwm(i)
    LCD.fill(LCD.black)
    LCD.text("BL PWN: "+str(i),30,70,LCD.white)
    LCD.fill_rect(0, 90, 60, 60, LCD.white)
    LCD.fill_rect(60, 90, 60, 60, LCD.red)
    LCD.fill_rect(120, 90, 60, 60, LCD.green)
    LCD.fill_rect(180, 90, 60, 60, LCD.blue)
    LCD.show()
    time.sleep(0.5)
#LCD.set_bl_pwm(0)
#time.sleep(1)
#LCD.set_bl_pwm(65535)
#test2_display_brightness(0.1)

LCD.fill(LCD.black)
LCD.fill_rect(0,0,240,40,LCD.red)
LCD.text("RP2040 LCD 1.28",60,25,LCD.green)
LCD.text("GC9A01 TESTS FINISHED",30,116,LCD.white)
LCD.show()
time.sleep(1)
LCD.display(False)