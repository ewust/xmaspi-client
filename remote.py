#!/usr/bin/python

import socket
import time
import sys
import traceback
import getpass

class RemoteDriver(object):
    def __init__(self, name=None, addr="141.212.110.237", port=4908):
        # Default to the username of the person running the script
        if name is None:
            name = getpass.getuser()

        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.sock.connect((addr, port))
        self.name = name
        self.sock.send(name + '\n')

        self.go()

    # blocks until it is our turn
    def go(self):
        self.sock.send("let's go\n")

        buf = self.sock.recv(0x100)
        # recvall
        while 'Go Time!\n' not in buf:
            addin = self.sock.recv(0x100)
            if addin == '':
                raise RuntimeError("socket closed before Go Time")
            buf += addin 
        

    def write_led(self, led_id, brightness, red, green, blue):
        self.sock.send(chr(led_id)+chr(brightness)+ \
                       chr(red)+chr(green)+chr(blue))

    def busy_wait(self, duration=None):
        if duration is None:
            duration = 1000

        while duration > 0:
            try:
                self.write_led(100, 0, 0, 0, 0)
                time.sleep(min(duration, 0.5))
                duration -= 0.5
            except:
                return
    wait = busy_wait

    def stop_signal(self):
        """
        Returns True if client's turn is over
        (use for future compatibility)
        """
        return False

    def done(self):
        self.sock.close()


if __name__=="__main__":
    # Unit Test/Example Use:

    # This will block until it is your turn 
    print 'Waiting for our turn...'
    d = RemoteDriver("UnitTest")
    print 'Our turn!'

    # Turn off all the LEDs 
    for i in range(100):
        d.write_led(i, 0, 0, 0, 0)

    # Turn them back on from the top, with some delay (100*.05 = 5s)
    for i in range(100):
        d.write_led(i, 200, 13, 0, 13)
        time.sleep(.05)

    # Turn them off in chunks of 10 (10*2 = 20s)
    # Note that busy_wait must be used for delays >= 1s
    for i in range(100, 0, -10):
        for j in range(i, i-10, -1):
            d.write_led(j-1, 0, 0, 0, 0)
        d.busy_wait(2)

    # Turn on all the LEDs 
    for i in range(100):
        d.write_led(i, 200, 13, 13, 13)
    
    # Send NOP keep-alives until our 30-second time expires
    # Alternatively, you can close the connection with
    # d.done() (or wait for it to time you out)
    d.busy_wait()
 
