#!/usr/bin/python


from bulbs import Bulbs
from remote import RemoteDriver
import random
import time

import colorsys

colors = [(15, 0, 0), \
            (15, 3, 0), \
            (15, 15, 0), \
            (0,   15,   0), \
            (0,   0, 15), \
            (4,  14, 13), \
            (14, 0, 14) ]


class Sort(object):
    def __init__(self, bulbs):
        self.bulbs = bulbs
        self.lights = [(0,0,0,0)]*100 
        for i in range(100):
            r = random.randint(0, 15)
            g = random.randint(0, 15)
            b = random.randint(0, 15)
            (r, g, b) = colors[random.randint(0, len(colors)-1)]
            self.lights[i] = (r, g, b, 200)

    # This is NOT a frequency approx
    def freq(self, idx):
        (r, g, b, a) = self.lights[idx]
        return colorsys.rgb_to_hsv(r/15.0, g/15.0, b/15.0)[0]

    def swap(self, i, j):
        self.lights[i], self.lights[j] = self.lights[j], self.lights[i]

    # Bubble sort!
    def sort(self):
        for i in range(100, 0, -1):
            any_swapped = False
            for j in range(1, i):
                
                if self.freq(j-1) > self.freq(j):
                    self.swap(j-1, j)
                    any_swapped = True
                
                self.render()
                time.sleep(0.003)
            if not any_swapped:
                print 'i finished'
                return
            


    def render(self):
        for i in range(100):
            self.bulbs.set(i, self.lights[i])
        self.bulbs.render()




if __name__=="__main__":
    print 'waiting...'
    d = RemoteDriver("BubbleSort")
    print 'our turn'
    b = Bulbs(d)
    
    sorter = Sort(b)
    sorter.sort()
    
    # Leave the sorted list up
    d.busy_wait()
    
    
