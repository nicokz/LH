"""
Demo: GC9A01 display and RP2040 low-power sleep functions
      RP2040 RTC (real time clock)
      On-board buttons IRQ functionality
      Fonts and text reach functionality
      
Ref.: /watch/RP2040watch.py library
      /watch/Fonts.py library
      
Created: 2024, Nov.9. by Nicholas Schreiner

Note: background image is converted from JPG file to raw RGB565 binary file (.rgb565)
      using /utils/jpg2rgb565.py
      Sans-serif bitmap font binary file generated with help make_font.py
      and 8x12 sans-serif font definition library sans_serif8x12.py
      
Note: power consumption drops down from regular 0.02A-0.05A close to 0.00A during low-power sleep mode
      press S1 key on device after start this example to switch sleep/awake mode
      
Note: edit code in line 33 to set real datetime for testing

TODO: turn off/on backlight fully
"""


import machine
import time
from watch.RP2040watch import GC9A01 as Screen
from watch.RP2040watch import ButtonsIRQ as Buttons
from watch.fonts import Font, Text

# Configure the wake-up pin with the correct pull-up or pull-down resistor
wake_pin = machine.Pin(17, machine.Pin.IN, machine.Pin.PULL_UP)
rtc = machine.RTC()
rtc.datetime((2024, 11, 8, 4, 16, 29, 00, 0)) # initial date and time on power up

buttons = Buttons()

screen = Screen()         # init GC9A01 display
screen.set_bl_pwm(65535)  # backlight of display to maximum
screen.loadRGB565background('/images/rp2040_bg.rgb565') # load background image
font = Font(screen)       # init 8x12 sans-serif font (default)
text = Text(font)         # text object for messages in center and clock
title_S1 = Text(font)     # S1 button's title
text.safe_zone(True)      # draw only in safe zone of the screen (not out to cyrcle's corners)
title_S1.safe_zone(True)  # same for button's title
text.draw("SLEEP MODE TEST", screen.color(255, 255, 255), text.CENTER, text.CENTER, True, 128)
title_S1.draw("< SLEEP", screen.color(255, 255, 0), text.ALIGN_LEFT, text.ALIGN_BOTTOM, True, 255)
screen.show()             # draw all above to screen buffer (show all)             
isSleeping = False

def clocks():
    global isSleeping  # Declare isSleeping as global
    global screen  # Declare screen as global
    global text
    if not isSleeping:
        year, month, day, weekday, hour, minute, second, _ = rtc.datetime()
        text.draw(f"{hour:02}:{minute:02}:{second:02}", screen.color(255, 255, 255), text.CENTER, text.CENTER, True, 128)
        screen.show()
        
action = clocks # define normal action

# Define the backlight dimming function (for both dimming down and up)
def smooth_dimming(screen, start_duty, end_duty, steps, delay):
    # Calculate the step size based on the direction of the transition
    step_size = (end_duty - start_duty) // steps
    
    # Gradually adjust the duty cycle from start_duty to end_duty
    for duty in range(start_duty, end_duty, step_size):
        screen.set_bl_pwm(duty)
        time.sleep(delay)
    # Ensure it ends precisely at the final duty level
    screen.set_bl_pwm(end_duty)

# Define a wake-up function
def wake_up(pin):
    global isSleeping  # Declare isSleeping as global
    global screen  # Declare screen as global
    global text
    global action
    global clocks
    
    if isSleeping:
        text.draw("WOKE UP FROM SLEEP!", screen.color(255, 255, 255), text.CENTER, text.CENTER, True, 128)
        title_S1.draw("< SLEEP", screen.color(255, 255, 0), text.ALIGN_LEFT, text.ALIGN_BOTTOM, True, 255)
        screen.sleep_mode(False)
        screen.set_bl_pwm(65535)
        screen.show()
        screen.display(True)
        isSleeping = False
        action = clocks
    else:
        # Reinitialize the screen for sleep mode
        text.draw("Zzzzzz...", screen.color(255, 255, 255), text.CENTER, text.CENTER, True, 128)
        title_S1.draw("< WAKE UP", screen.color(255, 255, 0), text.ALIGN_LEFT, text.ALIGN_BOTTOM, True, 255)
        screen.show()
        smooth_dimming(screen, 65535, 0, steps=5, delay=0.2)
        screen.display(False)
        screen.sleep_mode(True)
        isSleeping = True
        action = None
        # Enter light sleep (prevents USB disconnection)
        machine.lightsleep(10000)


buttons.enable_s1_interrupt(wake_up) # setting function wake_up() to be called when S1 button pressed

# Add a small delay after displaying the message before entering sleep for testing purposes
time.sleep(2)  # Allow time to see the Zzzzzz message

# Optional: simulate the sleep cycle (without entering deepsleep)
while True:
    if action:
        action() # run clocks if not sleeping
    time.sleep(0.5)  # Sleep and wait for wake-up signal
