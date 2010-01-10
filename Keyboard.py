#!/usr/bin/env python
# -*- coding: UTF-8 -*-

import sys
import random, time

if sys.platform.startswith('java'):
    from KeyboardJava import Keyboard as OSKeyboard
elif sys.platform == 'darwin':
    from KeyboardMac import Keyboard as OSKeyboard
elif sys.platform == 'win32':
    from KeyboardWin import Keyboard as OSKeyboard
else:
    from KeyboardUnix import Keyboard as OSKeyboard
            
            
class Keyboard(object):

    def __init__(self):

        self.k = OSKeyboard()
        
        
    def writeLetter(self, char):
        # TODO : check input
        OSKeyboard.writeLetter(self.k, char)
    
    def write(self, string):
        # TODO : check input
        OSKeyboard.write(self.k, string)

    def writeEasy(self, string, speed=1.0):
        # TODO : check input
        for ch in string:
            OSKeyboard.writeLetter(self.k, ch)
            time.sleep(random.random()/(speed*10.0))
