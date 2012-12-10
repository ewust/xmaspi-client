#!/usr/bin/python

# OH GOD THE LAGGGGGG

from time import sleep
from bulbs import Bulbs
from remote import RemoteDriver

print "waiting our turn..."
driver = RemoteDriver("ExampleSluice")
print "it's go time!"
bulbs = Bulbs(driver)

class Sluice:
    def __init__(self, position, size, speed, color):
        self.start = position
        self.end = (position+size) % Bulbs.COUNT
        self.speed = speed
        self.color = color

    def move(self):
        self.start = (self.start + self.speed) % Bulbs.COUNT
        self.end = (self.end + self.speed) % Bulbs.COUNT

    def draw(self, bulbs):
        x = self.start
        while x != self.end:
            bulbs.add(x, self.color)
            x = (x + 1) % Bulbs.COUNT

plane = [Sluice(0, 1, 1, Bulbs.WHITE)]
count = 0

while not driver.stop_signal():
    bulbs.clear()
    for sluice in plane:
        sluice.move()
        sluice.draw(bulbs)
    bulbs.render()
    sleep(0.05)
    try:
        new = {30: lambda : plane.append(Sluice(0, 1, 1, Bulbs.CYAN)),
        40: lambda : plane.append(Sluice(0, 1, 1, Bulbs.WHITE)),
        50: lambda : plane.append(Sluice(0, 1, 1, Bulbs.CYAN)),
        55: lambda : plane.append(Sluice(0, 2, 1, Bulbs.BLUE)),
        59: lambda : plane.append(Sluice(0, 1, 1, Bulbs.CYAN)),
        62: lambda : plane.append(Sluice(0, 1, 1, Bulbs.WHITE)),
        65: lambda : plane.append(Sluice(0, 1, 1, Bulbs.CYAN)),
        68: lambda : plane.append(Sluice(0, 2, 1, Bulbs.BLUE)),
        72: lambda : plane.append(Sluice(0, 5, 1, Bulbs.BLUE)),
        79: lambda : plane.append(Sluice(0, 3, 1, Bulbs.BLUE)),
        85: lambda : plane.append(Sluice(0, 70, 1, Bulbs.BLUE)),
        135: lambda : plane.append(Sluice(0, 1, 1, Bulbs.WHITE))
        }[count]()
    except KeyError:
        count = count+0
    count = count+1
