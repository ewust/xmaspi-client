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


if __name__=="__main__":
    d = RemoteDriver()  
    b = Bulbs(d)

    hour = 3
    minute = 45
    second = 10

    for led in range(100):
        d.write_led(led, 0, 0, 0, 0)

    while True:
        dt = datetime.datetime.now()
        show_clock(b, dt.hour, dt.minute, dt.second)
        time.sleep(.5)
        d.write_led(100, 0, 0, 0, 0)


