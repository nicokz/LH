"""
Demo: GC9A01 display 16bit RGB565 color image load
      Sprite anymation driven by
      QMI8658 IMU (gyroscope)
Ref.: /watch/RP2040watch.py library

Created: 2024, Nov.9. by Nicholas Schreiner

Note: background image is converted from JPG file to raw RGB565 binary file (.rgb565)
      using /utils/jpg2rgb565.py
      sprite image is converted from PNG file to raw RGB565 with alpha binary file (.rgba565)
      using /utils/jpg2rgb565.py
"""

import framebuf
from watch.RP2040watch import GC9A01 as Screen, QMI8658, Sprite
import time


qmi8658=QMI8658()

screen = Screen() # init GC9A01
screen.set_bl_pwm(65535) # to maximum! (TODO: play to change brightness)

screen.loadRGB565background('/images/rp2040_bg.rgb565') # loading background image
sprite = Sprite("/images/lenorko.rgba565", screen) # loading sprite

sprite.move(int((screen.width - sprite.width)/2),int((screen.height - sprite.height)/2)) # set sprite to center of screen

while True:
    xyz=qmi8658.Read_XYZ() # read gyro
    stepX = -int(xyz[3]) # for NORTH orientation x axis is reversive
    stepY = int(xyz[4])
    if 0 <= (stepX + sprite.posX) < (screen.width - sprite.width) and 0 <= (stepY + sprite.posY) < (screen.height - sprite.height):
        sprite.restore() # restore background under sprite in old position if any
        sprite.backup()  # backup background under sprite in new position  
        sprite.draw()    # draw sprite
        screen.show()    # send screen buffer to LCD display (show all)
        sprite.move(stepX, stepY) # change sprite position relativly
    #time.sleep(0.1)
    





