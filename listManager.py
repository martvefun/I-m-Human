#!/usr/bin/env python
# -*- coding: UTF-8 -*-

from __future__ import with_statement # This isn't required in Python 2.6
from Mouse import Mouse
from Keyboard import Keyboard

try:
  import json
except ImportError:
  try:
    import simplejson as json
  except ImportError:
    raise ImportError

import os, time


def createList():
    
    fileName=raw_input("Enter the name of the new list : ")

    if not os.path.exists("script/"):
        os.makedirs("script")
    if os.path.isfile("script/"+fileName+".json"):
        ok= raw_input("this scripts exist already, do you want to replace ? [y/n] ")
        if (ok=="n") | (ok=="no"):
            return 0
    else:
        print "script/"+fileName+".json doesn't exist"
    
    listAction=[]
    print """
the available commands :
move                # move the mouse
moveHuman           # move the mouse gradually (with errors)
click               # do a click
pressButton         # press a button of the mouse
releaseButton       # release a button of the mouse
write               # write something
writeHuman          # write something gradually
wait                # wait some time
"""

    cmd=raw_input("enter the command ('x' to leave) : ")
    poss_cmd=['move', 'moveHuman', 'click', 'pressButton', 'releaseButton', 'write', 'writeHuman', 'wait']

    while (cmd != 'x'):
        if (cmd not in poss_cmd):
            print "invalid choice, try again"
            cmd=raw_input("enter the command ? ")
            
        else:
            valid=True
            currentAction={}
            if (cmd in [x for x in poss_cmd if x not in ['write', 'writeHuman', 'wait']]):
                x=raw_input("enter the first coordinate (1 is the left border) : ")
                (x, valid) = isValidInt(x, valid)
                
                if valid:
                    y=raw_input("enter the second coordinate (1 is the top border) : ")
                    (y, valid) = isValidInt(y, valid)
                    
                if valid:
                    if (cmd in ['click', 'pressButton', 'releaseButton']):
                        button = raw_input("enter the number of the button (default 1) : ")
                        if button=="":
                            currentAction={"name":cmd, "args":[x, y]}
                        else:
                            (button, valid) = isValidInt(button, valid)
                            currentAction={"name":cmd, "args":[x, y, button]}
                    elif (cmd == 'moveHuman'):
                        speed = raw_input("enter the speed (default 1) : ")
                        if (speed=="") | (speed=="1"):
                            currentAction={"name":cmd, "args":[x, y, 1]}
                        else:
                            (speed, valid) = isValidFloat(speed, valid)
                            currentAction={"name":cmd, "args":[x, y, speed]}
                        freq = raw_input("enter the percentage of error (default 0) : ")
                        if (freq!="") & (freq!="0"):
                            (freq, valid) = isValidFloat(freq, valid)
                            currentAction["args"].append(freq)
                            if valid:
                                amp = raw_input("enter the amplitude (default 200) : ")
                                if (amp!="") & (amp!="200"):
                                    (amp, valid) = isValidInt(amp, valid)
                                    currentAction["args"].append(amp)
                        
                    else:
                        currentAction={"name":cmd, "args":[x, y]}

            elif (cmd in ['write', 'writeHuman']):
                txt=raw_input("What do you want to write : ")
                currentAction={"name":cmd, "args":[txt]}
            elif (cmd=='wait'):
                sec=raw_input("How long do you want to wait (in sec) : ")
                (sec, valid) = isValidFloat(sec, valid)
                currentAction={"name":cmd, "args":[sec]}
            
            if valid:
                listAction.append(currentAction)
            else:
                print "invalid action"
                    
            cmd=raw_input("\nEnter you command ? ")
            
    if listAction!=[]:
        with open("script/"+fileName+".json", 'w') as f:
            f.writelines(json.dumps(listAction, indent=4))
            f.flush()


def loadList():
    fileName=raw_input("Enter the name of your list : ")
    if not os.path.isfile("script/"+fileName+".json"):
        print "list not found"
    else:

        with open("script/"+fileName+".json") as f:
            listAction=json.load(f)
        
        mouse_function = { 
            'move': move_valid,
            'moveHuman': moveHuman_valid,
            'click' : click_valid,
            'pressButton' : pressButton_valid,
            'releaseButton' : releaseButton_valid
        }
        
        keyboard_function = {
            'write' : write_valid,
            'writeHuman' : writeHuman_valid
        }
        
        other_function= {
            'wait' : wait_valid
        }
        
        m = Mouse()
        k = Keyboard()
        for cmd in listAction:
            # cmd contains {'name':'fonction1', 'args':['123', '456', 'abc']} for exemple
            try:
                funcname = cmd['name']
            except:
                print "...error, method list missing..."
            
            try:
                params = cmd['args']
            except:
                params=""

            try:
                func = (mouse_function[ funcname ])
            except:
                try:
                    func = (keyboard_function [ funcname ])
                except:
                    try:
                        func = (other_function [ funcname ])
                    except:
                        print "...error, method unknown "+str(funcname)+"..."

            try:
                func( m, *params )
            except Exception as e:
                print "...error with function "+str(funcname)
                print e
        

def move_valid(m, x=None,y=None):
    print "move"
    m.move(x,y)

def moveHuman_valid(m, x=None,y=None, speed=1, freq=0, amp=200):
    print "moveHuman"
    m.moveHuman(x,y,speed)

def click_valid(m, x=None, y=None, button=1):
    print "click"
    m.click(x,y,button)
    
def pressButton_valid(m, x=None, y=None, button=1):
    print "press"
    m.pressButton(x,y,button)
    
def releaseButton_valid(m, x=None, y=None, button=1):
    print "release"
    m.releaseButton(x,y,button)
    
def write_valid(k,str=""):
    print "write"
    k.write(str)

def writeHuman_valid(k,str="", speed=1):
    print "write human"
    k.writeHuman(str)
        
def wait_valid(u, sec=None):
    print "wait"
    (sec, valid) = isValidFloat(sec,True)

    if valid:
        time.sleep(sec)
    else:
        raise InputError

def isValidInt(n, valid):
    try:
        n=int(n)
        if n<0:
            print "no negative number"
            valid=False
    except:
        print n, "invalid number"
        valid=False
    return (n, valid)

def isValidFloat(n, valid):
    try:
        n=float(n)
        if n<0:
            print "no negative number"
            valid=False
    except:
        print n, "invalid number"
        valid=False
    return (n, valid)

if __name__ == '__main__':
    print """
           *** I am human ***
            
    Thank you for using my program, I hope you'll like it
    If you have any comments, don't hesitate to contact me

        [1] create a new list
        [2] load and execute a list
        [?] about
        [x] quit
        """
    choice = raw_input("what do you want to do ? ")

    
    poss=tuple(('1', '2', '?', 'x'))
    
    while (choice != 'x'):
        while (choice not in poss):
            print "invaliv choice\n", poss
            choice = raw_input("what do you want to do ? ")
        
        if (choice=='1'):
            createList()
        elif (choice=='2'):
            loadList()
        elif (choice=='?'):
            about()
            
        print """
        [1] create a new list
        [2] load and execute a list
        [?] about
        [x] quit
        """
        choice = raw_input("what do you want to do ? ")
        
    print "see you soon"
