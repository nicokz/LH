import framebuf
from watch.RP2040watch import GC9A01 as Screen, QMI8658, Sprite
import time


qmi8658=QMI8658()

screen = Screen() # init GC9A01
screen.set_bl_pwm(65535) # to maximum! (TODO: play to change brightness)
#screen.loadRGB565background('/images/test_bg.rgb565')
screen.loadRGB565background('/images/rp2040_bg.rgb565')
sprite = Sprite("/images/lenorko.rgba565", screen)

#time.sleep(2)
sprite.move(120,120)

#for x in range(200):
while True:
    xyz=qmi8658.Read_XYZ()
    stepX = -int(xyz[3]) # for NORTH orientation x axis is reversive
    stepY = int(xyz[4])
    if 0 <= (stepX + sprite.posX) < (screen.width - sprite.width) and 0 <= (stepY + sprite.posY) < (screen.height - sprite.height):
        sprite.restore()
        sprite.backup()    
        sprite.draw()
        screen.show()
        sprite.move(stepX, stepY) 
    #time.sleep(0.1)
    





