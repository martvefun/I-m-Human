#!/usr/bin/env python
# -*- coding: UTF-8 -*-

from Xlib.display import Display
from Xlib import X, XK
from Xlib.protocol import event
import Xlib.ext.xtest
import time

class MouseUnix(object):

    def __init__(self):
        self.display = Display(":0")
        self.root = self.display.screen().root

    def pressButton(self, x, y, button = 1):
        # TODO : do it with focus.send_event
        self.move(x, y)
        Xlib.ext.xtest.fake_input(self.display, X.ButtonPress, button)
        self.display.sync()


    def releaseButton(self, x, y, button = 1):
        # TODO : do it with focus.send_event
        self.move(x, y)
        Xlib.ext.xtest.fake_input(self.display, X.ButtonRelease, button)
        self.display.sync()
	

    def clic(self, x, y, button = 1):
        # TODO : do it with focus.send_event
        try:
            self.pressButton(x, y, button)
            self.releaseButton(x, y, button)
        except:
            self.move(x, y)
            Xlib.ext.xtest.fake_input (self.display, X.ButtonPress, button)
            Xlib.ext.xtest.fake_input (self.display, X.ButtonRelease, button)
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
