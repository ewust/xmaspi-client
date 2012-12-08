#!/usr/bin/python

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
    while True: yield time() % 37
def minutes():
    while True: yield (time()/60) % 37
def hours():
    while True: yield (time()/3600) % 37

gx = GenXMas(bulbs)
gx.add((seconds(), solid(bulbs.RED)))
gx.add((minutes(), solid(bulbs.GREEN)))
gx.add((hours(), solid(bulbs.BLUE)))

while not driver.stop_signal():
    gx.render()
    sleep(0.005)
