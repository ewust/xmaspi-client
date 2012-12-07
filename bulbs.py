#!/usr/bin/python

def clamp(x, min, max):
    if x < min: return min
    if x > max: return max
    return x

class Bulbs:
    COUNT = 100

    WHITE   = (15,15,15,255)
    RED     = (15, 0, 0,255)
    GREEN   = ( 0,15, 0,255)
    BLUE    = ( 0, 0,15,255)
    CYAN    = ( 0,15,15,255)
    PURPLE  = (15, 0,15,255)
    YELLOW  = (15,15, 0,255)

    COLORS = (BLACK, WHITE, RED, GREEN, BLUE, CYAN, PURPLE, YELLOW)

    def __init__(self, driver):
        self.state =  [(0,0,0,0)] * self.COUNT
        self.frame = [(0,0,0,0)] * self.COUNT
        self.driver = driver
    def clear(self):
        self.frame = [(0,0,0,0)] * self.COUNT
    def set(self, i, (r,g,b,a)):
        r = clamp(r,0,15)
        g = clamp(g,0,15)
        b = clamp(b,0,15)
        a = clamp(a,0,255)
        self.frame[i] = (r,g,b,a)
    def add(self, i, (r,g,b,a)):
        (cr,cg,cb,ca) = self.frame[i]
        self.set(i,(cr+r,cg+g,cb+b,ca+a))
    def mix(self, i, (r,g,b,a)):
        # XXX: Work like add(), but scale relative amounts based on alpha channel
        #      (e.g. bright red + dim blue is mostly red stil, not bright purple)
        return self.add(i, (r,g,b,a))
    def render(self, force=False):
        wrote_bulb = False
        for i in range(self.COUNT):
            if force or self.frame[i] != self.state[i]:
                wrote_bulb = True
                (r,g,b,a) = self.frame[i]
                self.driver.write_led(i, a, r, g, b)
                self.state[i] = self.frame[i] # deep copy
        # Write something so we don't time out
        if not wrote_bulb:
            self.driver.write_led(self.COUNT, 0, 0, 0, 0)
