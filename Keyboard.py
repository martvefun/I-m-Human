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
        
    """
    write a letter
    params :
        char : the letter to write
    """  
    def writeLetter(self, char):
        # TODO : check input
        OSKeyboard.writeLetter(self.k, char)


    """
    write a sentence
    params :
        string : what to write
    """      
    def write(self, string):
        # TODO : check input
        OSKeyboard.write(self.k, string)


    """
    write a sentence gradually
    params :
        string : what to write
        speed : how long do you wait between letters
        frq : the frequency of human mistakes (0=never fail, 100=always fail) NOT WORKING
    """  
    def writeHuman(self, string, speed=1.0, frq=0):
        # TODO : check input
        for ch in string:
        
            humanError = random.random()
            ascii = ord(ch)
            if (humanError < (frq/100.0)) & ((ascii>=65) & (ascii<=90) | (ascii>=97) & (ascii<=122)) :
                print "errrrrrrooorrrr !!!!"+ch
                if (ch=='a') | (ch=='A'):
                    error=1
                elif (ch=='z') | (ch=='Z'):
                    error=-1
                if int(random.random()*2):
                    error=1
                else:
                    error=-1
                chError=chr(ascii+error)
                OSKeyboard.writeLetter(self.k, chError)
                time.sleep(random.random()/(speed*1.0))
                # TODO : erase the error
                # OSKeyboard.writeKeyCode(self.k, 8)
                time.sleep(random.random()/(speed*10.0))
                
            OSKeyboard.writeLetter(self.k, ch)
            time.sleep(random.random()/(speed*10.0))
            
            
            
