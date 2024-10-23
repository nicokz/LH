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
LCD.fill(LCD.black)
LCD.fill_rect(0,0,240,40,LCD.red)
LCD.text("RP2040 LCD 1.28",60,25,LCD.green)
LCD.vline(120, 45, 180, 0xffff)
LCD.line(120, 45, 117, 55, 0xffff)
LCD.line(120, 45, 123, 55, 0xffff)
LCD.hline(115, 120, 10, 0xffff)
LCD.show()
time.sleep(2)
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
