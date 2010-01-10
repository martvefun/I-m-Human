#!/usr/bin/env python
# -*- coding: UTF-8 -*-

import Xlib.display
import Xlib.X
import Xlib.XK
import Xlib.ext.xtest

#import Xlib.protocol.event

class MouseUnix(object):

    def __init__(self):
        self.display = Xlib.display.Display()
        self.root = self.display.screen().root

    def pressButton(self, x, y, button = 1):
        # TODO : do it with Xlib.protocol.event
        self.move(x, y)
        Xlib.ext.xtest.fake_input(self.display, Xlib.X.ButtonPress, button)
        self.display.sync()


    def releaseButton(self, x, y, button = 1):
        # TODO : do it with Xlib.protocol.event
        self.move(x, y)
        Xlib.ext.xtest.fake_input(self.display, Xlib.X.ButtonRelease, button)
        self.display.sync()
	

    def click(self, x, y, button = 1):
        # TODO : do it with Xlib.protocol.event
        self.pressButton(x, y, button)
        self.releaseButton(x, y, button)
        self.display.sync()


    def move(self, x, y):
        self.root.warp_pointer(x, y)
        self.display.sync()

    def getPosition(self):
        coord = self.root.query_pointer()._data
        return (coord["root_x"], coord["root_y"])
        
    def screenSize(self):
        width = self.display.screen().width_in_pixels
        height = self.display.screen().height_in_pixels
        return (width, height)
