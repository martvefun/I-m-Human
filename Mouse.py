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

    """
    creating the mouse depending on the operating system
    """
    def __init__(self):
        self.m = OSMouse()


    """
    press the button
    params:
        x, y : the coordinates where to press
        button : the number of the button. 1=left, 2=middle, 3=right
    except:
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
    release the button
    params:
        x, y : the coordinates where to release
        button : the number of the button. 1=left, 2=middle, 3=right
    except:
        send an InputError if the parameters are not valid    """
    def releaseButton(self, x, y, button = 1):
        try:
            (x, y) = self.isValidPos(x, y)
            button = self.isValidButton(button)
        except Error as e:
            print e
            raise InputError("releaseButton "+str(x)+", "+str(y)+", "+str(button), "invalid parameters")
        OSMouse.releaseButton(self.m, x, y, button)


    """
    make a click
    params:
        x, y : the coordinates where to click
        button : the number of the button. 1=left, 2=middle, 3=right
    except:
        send an InputError if the parameters are not valid
    """
    def click(self, x, y, button = 1):
        try:
            (x, y) = self.isValidPos(x, y)
            button = self.isValidButton(button)
        except Error as e:
            print e
            raise InputError("clic "+str(x)+", "+str(y)+", "+str(button), "invalid parameters")
        OSMouse.click(self.m, x, y, button)


    """
    move the mouse
    params:
        x, y : the coordinates where to go
        checked : boolean is the parameters have already been tested 
                  (should always == False when calling from outside)
    except:
        send an InputError if the parameters are not valid
    """
    def move(self, x, y, checked=False):
        if not checked:
            try:
                (x, y) = self.isValidPos(x, y)
            except Error as e:
                print e
                raise InputError("move "+str(x)+", "+str(y), "invalid parameters")
        OSMouse.move(self.m, x, y)
        

    """
    move the mouse gradually
    params :
        xFin, yFin : the coordinates to go
        speed : how long do you wait between moves
        frq : the frequency of human mistakes (0=never fail, 100=always fail)
        amp : when human mistakes how much do you derivates
        checked : boolean is the parameters have already been tested 
                  (should always == False when calling from outside)
    except:
        send an InputError if the parameters are not valid
    """
    def moveHuman(self, xFin, yFin, speed=1.0, frq=0, amp=200, checked=False):
        if not checked:
            # check the parameters
            try:
                (x, y) = self.isValidPos(xFin, yFin)
                speed = float(speed)
                frq = float(frq)
                amp = int(amp)
            except Error as e:
                print e
                raise InputError("moveEasy "+str(xFin)+", "+str(yFin)+", "+str(speed)+", "+str(frq)+", "+str(amp), "invalid parameters")
        
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

            humanError = random.random()
            if (humanError < (frq/100.0)) & (dist_x>amp/4) & (dist_y>amp/4):
                if x<xFin:
                    dirX=0
                elif x==xFin:
                    dirX=amp/2
                else:
                    dirX=amp
                if y<yFin:
                    dirY=0
                elif y==yFin:
                    dirY=amp/2
                else:
                    dirY=amp
                validPos=False
                while not validPos:
                    newXFin = x + int((random.random()*amp))-dirX
                    newYFin = y + int((random.random()*amp))-dirY
                    try:    
                        self.isValidPos(newXFin,newYFin)
                        validPos=True
                    except:
                        pass
                
                self.moveHuman(newXFin, newYFin, speed, checked=True)
            else:
                
                # if equals, move both x and y
                if (dist_x == dist_y):
                    x=self.nextPos(x,xFin)
                    y=self.nextPos(y,yFin)
                    
                        
                elif (dist_x > dist_y):
                    rapport = dist_y/float(dist_x)
                    # move also y only if has already moved 5 times only x
                    # or if dist_x < 2*dist_y
                    if (rapport < 0.5) &  (cptX < 5):
                        cptX=cptX+1
                        x=self.nextPos(x,xFin)
                        
                    else:
                        cptX=0
                        x=self.nextPos(x,xFin)
                        y=self.nextPos(y,yFin)

                else:
                    rapport = dist_x/float(dist_y)
                    # same as above with y
                    if (rapport < 0.5) &  (cptY < 5):
                        cptY=cptY+1
                        y=self.nextPos(y,yFin)
                    else:
                        cptY=0
                        x=self.nextPos(x,xFin)
                        y=self.nextPos(y,yFin)
                
                # finally move the mouse and wait a random time depending of the speed
                self.move(x,y, checked=True)
                time.sleep(random.random()/(speed*1000.0))

    
    #-------------------------
    #   Interns functions
    #-------------------------


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
    calculate the next position, depending of the current position and the destination
    params:
        fromP : the current position
        toP : the destination
    """
    def nextPos(self, fromP, toP):
        if (fromP>toP):
            return fromP-1
        else:
            return fromP+1

    """
    check if the positions given are valid
    params:
        x, y : the positions to check
    except:
        NotValidIntError(n) if 'n' is not an integer (a float is converted to int)
        OutOfScreenError(x,y) if the position [x,y] is out of the screen
    """
    def isValidPos(self, x, y):
        try:
            x2=int(x)
        except:
            raise NotValidIntError(x)
        try:
            y2=int(y)
        except:
            raise NotValidIntError(y)
        
        maxSc=self.screenSize()
        if (0 < x2) & (0 < y2) & (x2 < maxSc[0]) & (y2 < maxSc[1]):
            return (x2, y2)
        else:
            raise OutOfScreenError(x2, y2)
 
 
    """
    check if the input button is valid
    params:
        b : the button to check
    except:
        NotValidIntError(b) if 'b' is not an integer (a float is converted to int)
        NotValidButtonError(b) if 'b' is not 1, 2 or 3
    """       
    def isValidButton(self, b):
        try:
            b2=int(b)
        except:
            raise NotValidIntError(b)
        if (b2>=1) & (b2<=3):
            return b2
        else:
            raise NotValidButtonError(b2)
