#!/usr/bin/python


from bulbs import Bulbs
from remote import RemoteDriver
import random
import time

import colorsys

# boring rainbow
colors = [(15, 0, 0), \
            (15, 3, 0), \
            (15, 15, 0), \
            (0,   15,   0), \
            (0,   0, 15), \
            (4,  14, 13), \
            (14, 0, 14) ]


def init_colors():
    global colors
    colors = []
    cur_color = [0, 0, 15]
    idx = 0
    count_up = True
    # From Max
    while cur_color != [0, 1, 15]:
        # Cycle through the wheel
        if count_up is True:
            cur_color[idx] += 1
            if cur_color[idx] == 15:
                count_up = False
                idx = (idx-1)%3
        else:
            cur_color[idx] -= 1
            if cur_color[idx] == 0:
                count_up = True
                idx = (idx-1)%3
        (cp_r, cp_g, cp_b) = cur_color
        colors.append([cp_r, cp_g, cp_b])
        

init_colors()


class Sort(object):
    def __init__(self, bulbs):
        self.bulbs = bulbs
        self.lights = [(0,0,0,0)]*100 
        init_colors()
        for i in range(100):
            (r, g, b) = colors[random.randint(0, len(colors)-1)]
            self.lights[i] = (r, g, b, 200)

    # This is NOT a frequency approx
    def freq(self, value):
        (r, g, b, a) = value
        return colorsys.rgb_to_hsv(r/15.0, g/15.0, b/15.0)[0]

    def swap(self, i, j):
        self.lights[i], self.lights[j] = self.lights[j], self.lights[i]

    # Bubble sort!
    def sort(self):
        for i in range(100, 0, -1):
            any_swapped = False
            for j in range(1, i):
                
                if self.freq(self.lights[j-1]) > self.freq(self.lights[j]):
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
    
    
