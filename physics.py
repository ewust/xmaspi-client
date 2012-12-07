#!/usr/bin/python

import sys
from time import sleep
from bulbs import Bulbs
from remote import RemoteDriver

import random

NUM_BALLS = random.randint(2,5)

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

# Draw blank slate
blank_slate = list(bulbs.frame)
bulbs.render(force=True)
sleep(.1)

# Now add the balls
balls = zip(*[random.sample(range(10,90,2), NUM_BALLS),random.sample(Bulbs.COLORS, NUM_BALLS),[x*[-1,1][random.randint(0,1)] for x in [1]*NUM_BALLS]])


def ghost(ball, color, direction, initial=False):
	r,g,b,a = color

	a = a >> 1
	while (a > 0):
		ball -= direction
		if ball in bumpers or ball in zip(*balls)[0]:
			return

		a = a >> 1
		bulbs.mix(ball, (r,g,b,a))
		if initial:
			bulbs.render()
			sleep(.1)

print "Starting with %d balls at positions:" % (NUM_BALLS)
for ball,color,direction in balls:
	print "\t%d: %s going %d" % (ball, str(color), direction)
	bulbs.frame[ball] = color
	bulbs.render()
	sleep(.1)
	ghost(ball, color, direction, True)

# Blink balls before starting motion
cache = bulbs.frame
for blinks in range(3):
	bulbs.frame = blank_slate
	bulbs.render(force=True)
	d.busy_wait(.5)
	bulbs.frame = cache
	bulbs.render(force=True)
	d.busy_wait(.5)


def advance(ball_tuple):
	ball, color, direction = ball_tuple
	r,g,b,a = color
	bulbs.frame[ball] = (0,0,0,0) # 0 for now, will be ghosted later

	if ball+direction in bumpers:
		print "%d Hit bumper." % (ball)
		direction = -direction
		ball = ball + direction
		a = a >> 1
	elif ball+direction in zip(*balls)[0]:
		print "%d Collided with %d" % (ball, ball+direction)
		other = ball+direction
		ro,go,bo,ao = bulbs.frame[other]

		if random.randint(0,255) in range(abs(a-ao)):
			# Pass through instead of collide
			# Should be impossilbe if both lights same brightess
			# Greater the delta `a', greater the prob. of passthru
			ball += direction
		else:
			direction = -direction
			ball = ball + direction

			# Reverse direction of collided ball
			temp = list(balls[zip(*balls)[0].index(other)])
			temp[2] *= -1
			balls[zip(*balls)[0].index(other)] = tuple(temp)
	else:
		ball += direction

	bulbs.frame[ball] = (r,g,b,a)
	return ball, (r,b,g,a), direction

while True:
	for i in range(len(balls)):
		balls[i] = advance(balls[i])
	for ball,color,direction in balls:
		ghost(ball,color,direction)
	bulbs.render()
	for b in field - set(zip(*balls)[0]):
		bulbs.frame[b] = (0,0,0,0)
	d.busy_wait(.1)

d.busy_wait(5)
