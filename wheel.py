from time import sleep
from remote import RemoteDriver

d = RemoteDriver("wheel")

idx = 0
count_up = True
colors = [0,0,15]

while True:

	# Set the color
	for i in range(100):
		d.write_led(i, 255, colors[0], colors[1], colors[2])

	# Cycle through the wheel
	if count_up is True:
		colors[idx] += 1
		if colors[idx] == 15:
			count_up = False
			idx = (idx-1)%3
	else:
		colors[idx] -= 1
		if colors[idx] == 0:
			count_up = True
			idx = (idx-1)%3
