#!/usr/bin/env python

from Mouse import Mouse
from Keyboard import Keyboard
import time

m = Mouse()
k = Keyboard()

try:
    m.clic(111, 222, 1)
    time.sleep(2)
    k.write("azerty")
except Exception as e:
    print e
