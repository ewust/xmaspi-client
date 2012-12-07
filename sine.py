#!/usr/bin/python

# sine rainbow

from time import sleep
from math import sin
from remote import RemoteDriver

print "waiting our turn..."
driver = RemoteDriver("ExampleBulbs")
print "it's go time!"

offr = 0
offg = 0
offb = 0
offa = 0

while not driver.stop_signal():
    for i in range(100):
        xr = (i+offr) % 100
        xg = (i+offg) % 100
        xb = (i+offb) % 100
        xa = (i+offb) % 100
        yr = sin(xr/5.) * 8+7
        yg = sin(xg/5.) * 8+7
        yb = sin(xb/5.) * 8+7
        ya = sin(xa/10.) * 128+127
        driver.write_led(i,int(ya),int(yr),int(yg),int(yb))
    offr = (offr + 1) % 100
    offg = (offg + 2) % 100
    offb = (offb + 3) % 100
    offa = (offa + 1) % 100
