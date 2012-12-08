#!/usr/bin/python

# Fading Random Walk
# (gen.py and GenXMas)

from time import sleep
from bulbs import Bulbs
from remote import RemoteDriver
from gen import *
from random import choice
from itertools import chain

print "waiting our turn..."
driver = RemoteDriver("ExampleSnake")
print "it's go time!"
bulbs = Bulbs(driver)

gx = GenXMas(bulbs)

x=50
while not driver.stop_signal():
    gx.add((fixed(x), 
            chain(
                fader(bulbs.RED, bulbs.WHITE, 10),
                fader(bulbs.WHITE, bulbs.BLACK, 100)
                )
            ))
    gx.render()

    x += choice([1,-1])
    if x == 100:
        x = 0
    elif x < 0:
        x = 99

