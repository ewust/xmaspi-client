#!/usr/bin/python

# SNAKES!

from time import sleep
from bulbs import Bulbs
from remote import RemoteDriver

print "waiting our turn..."
driver = RemoteDriver("ExampleBulbs")
print "it's go time!"
bulbs = Bulbs(driver)

class Snake:
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

plane = [Snake(0, 20, 1, Bulbs.RED),
         Snake(79, 20, -1, Bulbs.BLUE),
         Snake(45, 10, 2, Bulbs.GREEN)]

while True:
    bulbs.clear()
    for snake in plane:
        snake.move()
        snake.draw(bulbs)
    bulbs.render()
    sleep(0.05)
