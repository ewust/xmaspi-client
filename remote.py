#!/usr/bin/python

import socket
import time
import sys
import traceback


class RemoteDriver(object):
    def __init__(self, addr, port, name):
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
    
    def done(self):
        self.sock.close()


if __name__=="__main__":
    # Unit Test/Example Use:

    # This will block until it is your turn 
    print 'Waiting for our turn...'
    d = RemoteDriver("141.212.110.237", 4908, "UnitTest")
    print 'Our turn!'

    # Turn off all the LEDs 
    for i in range(100):
        d.write_led(i, 0, 0, 0, 0)
        

    # Turn them back on from the top, with some delay
    for i in range(100):
        d.write_led(i, 200, 13, 0, 13)
        time.sleep(.05)
    
    # Send NOP keep-alives until our 30-second time expires
    # Alternatively, you can close the connection with
    # d.done() (or wait for it to time you out)
    i = 0
    while True:
        try:
            d.write_led(0, 0, 0, 0, 0) 
            time.sleep(0.5)
        except:
            break
 
