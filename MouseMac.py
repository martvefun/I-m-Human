#!/usr/bin/env python
# -*- coding: iso-8859-1 -*-

from Quartz import CGPostMouseEvent, CGWarpMouseCursorPosition, CGDisplayPixelsHigh, CGDisplayPixelsWide
from AppKit import NSEvent
from UserEmulation import UserEmulationMeta

class UserEmulation(UserEmulationMeta):

    def pressButton(self, x, y, button = 1):
        button_list = [0, 0, 0]
        button_list[button - 1] = 1
        CGPostMouseEvent((x, y), 1, 3, *button_list)

    def releaseButton(self, x, y, button = 1):
        CGPostMouseEvent((x, y), 1, 3, 0, 0, 0)
    
    def clic(self, x, y, button = 1):
        self.pressButton(x, y, button)
        self.releaseButton(x, y, button)
    
    def move(self, x, y):
        CGWarpMouseCursorPosition((float(x), float(y)))

    def getPosition(self):
        loc = NSEvent.mouseLocation()
        return (loc.x, CGDisplayPixelsHigh(0) - loc.y)

    def screenSize(self):
        return (CGDisplayPixelsWide(0), CGDisplayPixelsHigh(0))

#
#CGPostMouseEvent deprecated in SnowLeopard
#
#use instead
#
#CGEventRef mouseDownEv = CGEventCreateMouseEvent (NULL,kCGEventLeftMouseDown,pt,kCGMouseButtonLeft);
#CGEventPost (kCGHIDEventTap, mouseDownEv);
#
#CGEventRef mouseUpEv = CGEventCreateMouseEvent (NULL,kCGEventLeftMouseUp,pt,kCGMouseButtonLeft);
#CGEventPost (kCGHIDEventTap, mouseUpEv );
#
#http://developer.apple.com/Mac/library/documentation/Carbon/Reference/QuartzEventServicesRef/DeprecationAppendix/AppendixADeprecatedAPI.html#jumpTo_5
#http://developer.apple.com/Mac/library/documentation/Carbon/Reference/QuartzEventServicesRef/Reference/reference.html#jumpTo_7
