#!/usr/bin/python

import sys
from time import sleep
from bulbs import Bulbs
from remote import RemoteDriver

import random

print "waiting our turn..."
if len(sys.argv) > 1:
	d = RemoteDriver(name="test", addr="localhost")
else:
	d = RemoteDriver("Physics?")
print "it's go time!"
bulbs = Bulbs(d)


# Start by drawing bumpers at the edge
for f in range(5):
	bulbs.frame[f] = Bulbs.BLUE
for f in range(95,100):
	bulbs.frame[f] = Bulbs.BLUE

# Now add the balls
balls = random.sample(range(10,90), 4)
for b in balls:
	if random.randint(0,1):
		bulbs.frame[b] = (15,0,0,random.randint(0,255))
	else:
		bulbs.frame[b] = (0,15,0,random.randint(0,255))

# Draw everything
bulbs.render(force=True)

# Blink balls before starting motion
for blinks in range(3):
	d.busy_wait(.5)
	a = [0] * len(balls)
	for i in range(len(balls)):
		a[i] = bulbs.frame[balls[i]][3]
		r,g,b,ign = bulbs.frame[balls[i]]
		bulbs.frame[balls[i]] = (r,g,b,0)
	bulbs.render()
	d.busy_wait(.5)
	for i in range(len(balls)):
		r,g,b,ign = bulbs.frame[balls[i]]
		bulbs.frame[balls[i]] = (r,g,b,a[i])
	bulbs.render()


def ghost(ball):
	a = bulbs.frame[ball][3]
	if bulbs.frame[ball][0]:
		# Red is down
		d = -1
	else:
		d = 1

	a = a >> 1
	while (a > 0):
		r,g,b,ign = bulbs.frame[ball]

		ball += d
		if sum(bulbs.frame[ball]):
			return
		a = a >> 1
		bulbs.frame[ball] = (r,g,b,a)

for b in balls:
	ghost(b)

bulbs.render()

d.busy_wait(5)
