#!/usr/bin/python

# Eiffel Tower Lightshow

from time import sleep
from bulbs import Bulbs
from remote import RemoteDriver
from random import random
from random import choice

print "waiting..."
driver = RemoteDriver("EiffelTower")
print "FLASH!"
bulbs = Bulbs(driver)

base_color = (15,4,0,100)
flash_color = (255,255,255,255)
thresh = 0.1

while not driver.stop_signal():    
    for i in range(Bulbs.COUNT):
        if random() > thresh:
            bulbs.set(i, base_color)
        else:
            bulbs.set(i, flash_color)
    bulbs.render()
    sleep(0.05)
