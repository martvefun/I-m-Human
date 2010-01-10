#!/usr/bin/env python
# -*- coding: UTF8 -*-

import sys
import random, time
from CustomError import *

if sys.platform.startswith('java'):
    from MouseJava import Mouse as OSMouse

elif sys.platform == 'darwin':
    from MouseMac import Mouse as OSMouse

elif sys.platform == 'win32':
    from MouseWin import Mouse as OSMouse

else:
    from MouseUnix import MouseUnix as OSMouse


class Mouse(object):

    def __init__(self):
        self.m = OSMouse()

    """
    return the current position of the mouse
    """
    def getPosition(self):
        return OSMouse.getPosition(self.m)


    """
    return a tuple with the size of the screen
    """
    def screenSize(self):
        return OSMouse.screenSize(self.m)

    """
    press the specified (default 1) button on x, y
    send an InputError if the parameters are not valid
    """
    def pressButton(self, x, y, button = 1):
        try:
            (x, y) = self.isValidPos(x, y)
            button = self.isValidButton(button)
        except Error as e:
            print e
            raise InputError("pressButton "+str(x)+", "+str(y)+", "+str(button), "invalid parameters")
        OSMouse.pressButton(self.m, x, y, button)


    """
    press the specified (default 1) button on x, y
    send an InputError if the parameters are not valid
    """
    def releaseButton(self, x, y, button = 1):
        try:
            (x, y) = self.isValidPos(x, y)
            button = self.isValidButton(button)
        except Error as e:
            print e
            raise InputError("releaseButton "+str(x)+", "+str(y)+", "+str(button), "invalid parameters")
        OSMouse.releaseButton(self.m, x, y, button)


    """
    clic the specified (default 1) button on x, y
    send an InputError if the parameters are not valid
    """
    def clic(self, x, y, button = 1):
        try:
            (x, y) = self.isValidPos(x, y)
            button = self.isValidButton(button)
        except Error as e:
            print e
            raise InputError("clic "+str(x)+", "+str(y)+", "+str(button), "invalid parameters")
        OSMouse.clic(self.m, x, y, button)


    """
    move the mouse to x, y
    send an InputError if the parameters are not valid
    """
    def move(self, x, y):
        try:
            (x, y) = self.isValidPos(x, y)
        except Error as e:
            print e
            raise InputError("move "+str(x)+", "+str(y), "invalid parameters")
        OSMouse.move(self.m, x, y)
        

    """
    move the mouse gradually to x, y at the specified speed (default 1)
    send an InputError if the parameters are not valid
    """
    def moveEasy(self, xFin, yFin, speed=1.0):
        # check the parameters
        try:
            (x, y) = self.isValidPos(xFin, yFin)
            speed = float(speed)
        except Error as e:
            print e
            raise InputError("moveEasy "+str(xFin)+", "+str(yFin)+" "+str(speed), "invalid parameters")
        
        # init
        (x, y) = self.getPosition()
        cptX=0
        cptY=0
        
        # while not arrived at the final position
        while (x != xFin) | (y != yFin):
            from_pos = self.getPosition()
            x = from_pos[0]
            y = from_pos[1]

            #calculate what's left
            dist_x = abs(x-xFin)
            dist_y = abs(y-yFin)
            
            # if equals, move both x and y
            if (dist_x == dist_y):
                if (x > xFin):
                    x=x-1
                elif (x < xFin):
                    x=x+1
                if (y > yFin):
                    y=y-1
                elif (y < yFin):
                    y=y+1
                    
            elif (dist_x > dist_y):
                rapport = dist_y/float(dist_x)
                # move also y only if has already moved 5 times only x
                # or if dist_x < 2*dist_y
                if (rapport < 0.5) &  (cptX < 5):
                    cptX=cptX+1
                    if (x > xFin):
                        x=x-1
                    elif (x < xFin):
                        x=x+1
                else:
                    cptX=0
                    if (x > xFin):
                        x=x-1
                    elif (x < xFin):
                        x=x+1
                    if (y > yFin):
                        y=y-1
                    elif (y < yFin):
                        y=y+1

            else:
                rapport = dist_x/float(dist_y)
                # same as above with y
                if (rapport < 0.5) &  (cptY < 5):
                    cptY=cptY+1
                    if (y > yFin):
                        y=y-1
                    elif (y < yFin):
                        y=y+1
                else:
                    cptY=0
                    if (x > xFin):
                        x=x-1
                    elif (x < xFin):
                        x=x+1
                    if (y > yFin):
                        y=y-1
                    elif (y < yFin):
                        y=y+1
            
            # finally move the mouse and wait a random time depending of the speed
            OSMouse.move(self.m,x,y)
            time.sleep(random.random()/(speed*1000.0))



    """
    check if the positions given are 
    send an InputError if the parameters are not valid
    """
    def isValidPos(self, x, y):
        try:
            x2=int(x)
        except:
            raise NotValidInt(x)
        try:
            y2=int(y)
        except:
            raise NotValidInt(y)
        
        maxSc=self.screenSize()
        if (0 < x2) & (0 < y2) & (x2 < maxSc[0]) & (y2 < maxSc[1]):
            return (x2, y2)
        else:
            raise OutOfScreenError(x2, y2)
 
    """
    check if the positions given are 
    send an InputError if the parameters are not valid
    """       
    def isValidButton(self, b):
        try:
            b2=int(b)
        except:
            raise NotValidInt(b)
        if (b2>=1) & (b2<=3):
            return b2
        else:
            raise NotValidButton(b2)
