#!/usr/bin/python

from time import sleep
from bulbs import Bulbs
from remote import RemoteDriver

print "waiting our turn..."
d = RemoteDriver("ExampleBulbs")
print "it's go time!"
bulbs = Bulbs(d)

class Snake:
    def __init__(self, position, size, speed, color):
        self.start = position
        self.end = (position+size) % 100
        self.speed = speed
        self.color = color

    def move(self):
        self.start = (self.start + self.speed) % 100
        self.end = (self.end + self.speed) % 100

    def draw(self, bulbs):
        x = self.start
        while x != self.end:
            bulbs.add(x, self.color)
            x = (x + 1) % 100

red = (15,0,0,255) # red 0-15, green 0-15, blue 0-15, brightness 0-255
blue = (0,0,15,255)

plane = [Snake(0,10,1,red), Snake(50,15,-1,blue)]

while True:
    for snake in plane:
        snake.move()
        snake.draw(bulbs)
    bulbs.render()
    sleep(0.01)
