#!/usr/bin/env python

from Mouse import Mouse
from Keyboard import Keyboard
import time

m = Mouse()
k = Keyboard()

try:
    print "click left"
    m.click(300,400,1)
    time.sleep(1)
    print "write"
    k.writeHuman("azertyuioqsddfghj\n")
    time.sleep(1)
    print "move human"    
    m.moveHuman(1000,780, speed=0.5, frq=10, amp=500)
except Exception as e:
    print e
