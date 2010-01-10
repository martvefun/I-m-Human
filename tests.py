#!/usr/bin/env python

from Mouse import Mouse
from Keyboard import Keyboard
import time

m = Mouse()
k = Keyboard()
m.click(200,300,3)

try:
    print "move"
    m.move(600,300)
    time.sleep(1)
    print "click right"
    m.click(200,300,3)
    time.sleep(1)
    print "click left"
    m.click(180,280,1)
    time.sleep(1)
    print "write"
    k.write("Something\n")
    time.sleep(1)
    print "move human"    
    m.moveHuman(1000,780, speed=0.5, frq=10, amp=500)
except Exception as e:
    print e
