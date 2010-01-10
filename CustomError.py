#!/usr/bin/env python
# -*- coding: UTF-8 -*-

class Error(Exception):
    """Base class for exceptions"""
    pass


class InputError(Error):
    """Exception raised for errors in the input.

    Attributes:
        expr -- input expression in which the error occurred
        msg  -- explanation of the error
    """

    def __init__(self, expr, msg):
        self.expr = expr
        self.msg = msg
        
    def __str__(self):
        return self.expr+" : "+self.msg

        
class NotValidInt(Error):
    """Exception raised if a parameter passed is not a valid int

    Attributes:
        i -- the integer
    """

    def __init__(self, i):
        self.i = i
        
    def __str__(self):
        return str(self.i)+" is not a valid integer"
        
       
        
class NotValidButton(Error):
    """Exception raised if a button is incorrect

    Attributes:
        b -- the button
    """

    def __init__(self, b):
        self.b = b
               
    def __str__(self):
        return str(self.b)+" is not a valid button"
        
        
class OutOfScreenError(Error):
    """Exception raised if the position is out of the screen

    Attributes:
        x, y -- the coordinates
    """

    def __init__(self, x, y):
        self.x = x
        self.y = y
        
    def __str__(self):
        return str(self.x)+", "+str(self.y)+" is out of the screen"
