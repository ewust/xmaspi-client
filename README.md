xmaspi-client
=============

Remote control examples and framework for the xmaspi light show

Using the API
-------------

Writing to the lights with this API is simple:

    from remote import 
    d = RemoteDriver("UnitTest")
    d.write_led(led_id, brightness, red, green, blue)

For led_id = [0..99], brightness = [0..255], red,green,blue = [0..15]

We have provided a few examples, including Snake (snake.py), 
Bubble sort (sort.py) and Quicksort (quicksort.py).

We encourage you to add your own!

