#!/usr/bin/python

import sys
from time import sleep
from bulbs import Bulbs
from remote import RemoteDriver

import random

NUM_BALLS = 1

print "waiting our turn..."
if len(sys.argv) > 1:
	d = RemoteDriver(name="test", addr="localhost")
else:
	d = RemoteDriver("Physics?")
print "it's go time!"
bulbs = Bulbs(d)


# Start by drawing bumpers at the edge
bumpers = set()
for f in range(5):
	bulbs.frame[f] = Bulbs.BLUE
	bumpers.add(f)
for f in range(95,100):
	bulbs.frame[f] = Bulbs.BLUE
	bumpers.add(f)
field = set(range(100)) - bumpers

# Now add the balls
balls = random.sample(range(10,90,2), NUM_BALLS)
for b in balls:
	if random.randint(0,1):
		bulbs.frame[b] = (15,0,0,random.randint(150,255))
	else:
		bulbs.frame[b] = (0,15,0,random.randint(150,255))

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
		d = 1
	else:
		d = -1

	a = a >> 1
	while (a > 0):
		r,g,b,ign = bulbs.frame[ball]

		ball -= d
		if sum(bulbs.frame[ball][2:]):
			return
		a = a >> 1
		bulbs.add(ball, (r,g,b,a))

for b in balls:
	ghost(b)

bulbs.render()

def advance(ball):
	r,g,b,a = bulbs.frame[ball]
	bulbs.frame[ball] = (0,0,0,0) # 0 for now, will be ghosted later

	if r:
		d = 1
	elif g:
		d = -1
	else:
		print "Something has gone wrong"
		print "Current ball:", ball
		print (r,g,b,a)
		print
		print bulbs.frame

	if ball+d in bumpers:
		d = -d
		ball = ball + d
		bulbs.frame[ball] = (g,r,b,a>>1)
		print "Hit bumper. Ball %d is now (%d %d %d %d)" % (ball, g,r,b,a>>1)
	elif ball+d in balls:
		print "Collided with ", ball+d
		other_idx = ball+d
		other = bulbs.frame[other_idx]

		d = -d
		ball = ball + d
		bulbs.frame[ball] = other

		bulbs.frame[other_idx] = (r,g,b,a)
	else:
		ball = ball + d
		bulbs.frame[ball] = (r,g,b,a)

	return ball

while True:
	for i in range(len(balls)):
		balls[i] = advance(balls[i])
	for b in balls:
		ghost(b)
	bulbs.render()
	for b in field - set(balls):
		bulbs.frame[b] = (0,0,0,0)
	d.busy_wait(.1)

d.busy_wait(5)
