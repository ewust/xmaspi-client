#!/usr/bin/python

from bulbs import Bulbs

# bulb control based on Python generators

# color generators

def fader(a,b,n):
    (r1,g1,b1,a1) = a
    (r2,g2,b2,a2) = b
    for i in range(n):
        r0 = r1 + (r2-r1)*(1.*i/n)
        g0 = g1 + (g2-g1)*(1.*i/n)
        b0 = b1 + (b2-b1)*(1.*i/n)
        a0 = a1 + (a2-a1)*(1.*i/n)
        yield (r0,g0,b0,a0)

def solid(color):
    while True:
        yield color

# position generators

def fixed(pos):
    while True:
        yield pos

def inertial(pos,delta):
    while True:
        yield pos
        pos = (pos + delta) % Bulbs.COUNT

def gravity(x,v,g):
    while True:
        print x
        yield x
        x += v
        v += g

def bouncy(x,v,g):
    max = Bulbs.COUNT-1
    while True:
        if x > max:
            x = 2*max-x
            v = -v
        print x,v
        yield x
        x += v
        v += g

# renderer

class GenXMas:
    def __init__(self, bulbs, sprites = []):
        self.bulbs = bulbs
        self.sprites = sprites
    def add(self, (pos_gen, color_gen)):
        self.sprites += [(pos_gen, color_gen)]
    def render(self):
        survivors = []
        frame = [(0,0,0,0)] * Bulbs.COUNT
        for i in range(len(self.sprites)):
            try:
                pos_gen,color_gen = self.sprites[i]
                pos = pos_gen.next()
                color = color_gen.next()
                if pos >= 0 and pos < Bulbs.COUNT:
                    r,g,b,a = color
                    if pos != int(pos):
                        r,g,b,a = color                        
                        y = pos-int(pos)
                        x = 1.-y
                        frame[int(pos)] = (r,g,b,int(x*a))
                        frame[(int(pos)+1) % Bulbs.COUNT] = (r,g,b,int(y*a))
                    else:
                        frame[int(pos)] = color
                survivors += [(pos_gen,color_gen)]
            except StopIteration:
                pass
        self.sprites = survivors
        for i in range(len(frame)):
            self.bulbs.set(i,frame[i])
        self.bulbs.render()
