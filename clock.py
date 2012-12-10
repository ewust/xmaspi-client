#!/usr/bin/python

from remote import RemoteDriver
from bulbs import Bulbs
import time
import datetime


# returns a list of leds and their colors 
# given a color (may interleave)
def degree_to_leds(deg, color):
    ret = []
    deg %= 360
    led = ((deg / 360.0) * 37)
    (r,g,b,a)=color

    while led < 100:
        cur_led=int(led)
        next_led=cur_led+1
        ret.append((cur_led, (r, g, b, int((1 - (led - cur_led))*a))))
        ret.append((next_led, (r, g, b, int((1 - (next_led - led))*a))))
        led += 37
    return ret

'''
def show_clock(bulbs, hour, minute, second):
    hour_hand_leds = degree_to_leds(360*hour/12.0, (15, 0, 0, 200))
    minute_hand_leds  = degree_to_leds(6*minute, (0, 15, 0, 200))
    second_hand_leds = degree_to_leds(6*second, (0, 0, 15, 200))
    
    for led,color in hour_hand_leds:
        print led, color
        bulbs.set(led, color)
    for led,color in minute_hand_leds:
        bulbs.set(led, color)
    for led,color in second_hand_leds:
        bulbs.set(led, color)

    bulbs.render()
    bulbs.clear()
'''


# Subpixel Clock
# (gen.py and GenXMas)

from time import sleep
from bulbs import Bulbs
from remote import RemoteDriver
from gen import *
from random import choice
from itertools import chain

print "waiting our turn..."
driver = RemoteDriver("SubpixelClock")
print "it's go time!"
bulbs = Bulbs(driver)

from time import time
def seconds():
    while True: 
        dt = datetime.datetime.now()
        yield dt.second
def minutes():
    while True: 
        dt = datetime.datetime.now()
        yield dt.minute
def hours():
    while True:
        dt = datetime.datetime.now()
        yield dt.hour

gx = GenXMas(bulbs)
gx.add((seconds(), solid(bulbs.RED)))
gx.add((minutes(), solid(bulbs.GREEN)))
gx.add((hours(), solid(bulbs.BLUE)))

while not driver.stop_signal():
    gx.render()
    sleep(0.005)
