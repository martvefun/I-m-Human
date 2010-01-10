# -*- coding: iso-8859-1 -*-
from Xlib.display import Display
from Xlib import X
from Xlib.protocol import event
import Xlib.ext.xtest
import time

display = Display(":0")
root = display.screen().root

class PyMouse(object):

    def press(self, x, y, button = 1):
        focus = display.get_input_focus()._data["focus"];
        rel = focus.translate_coords(root, x, y)
        button_list = [None, X.Button1, X.Button3, X.Button2]

        try:
            mousePress = event.ButtonPress(
                time = int(time.time()),
                root=root,
                window=focus,
                same_screen=0,
                child=X.NONE,
                root_x=x,
                root_y=y,
                event_x=rel.x,
                event_y=rel.y,
                state=1,
                detail=button_list[button]
                )
            print "press"
            focus.send_event(mousePress, propagate = True)
        except Exception as e:
            print e
        display.sync()

    def release(self, x, y, button = 1):
        focus = display.get_input_focus().focus
        rel = focus.translate_coords(root, x, y)
        button_list = [None, X.Button1, X.Button3, X.Button2]
        print "release"+str(rel.x)+" "+str(rel.y)
        mouseRealease = event.ButtonRelease(
                time=X.CurrentTime,
                root=root,
                window=focus,
                same_screen=0,
                child=X.NONE,
                root_x=x,
                root_y=y,
                event_x=rel.x,
                event_y=rel.y,
                state=0,
                detail=button_list[button]
                )
        focus.send_event(mouseRealease, propagate = True)

        display.sync()

    def click(self, x, y, button = 1):
        try:
            self.press(x, y, button)
            self.release(x, y, button)
        except:
            # Using xlib-xtest fake input
            self.move(x, y) # I believe you where not setting the position
            Xlib.ext.xtest.fake_input (display, X.ButtonPress, button+1) #Unix-xlib starts from 1

        display.sync()

    def move(self, x, y):
        root.warp_pointer(x, y)
        display.sync()

    def position(self):
        coord = display.screen().root.query_pointer()._data
        return coord["root_x"], coord["root_y"]

    def screen_size(self):
        width = display.screen().width_in_pixels
        height = display.screen().height_in_pixels
        return width, height
        
p=PyMouse()
p.press(200,300,1)
time.sleep(0.1)
p.release(300,300,1)
