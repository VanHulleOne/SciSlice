# -*- coding: utf-8 -*-
"""
Created on Tue Oct 27 13:13:34 2015

@author: lvanhulle
"""

class Point:
    
    def __init__(self, x, y):
        self.X = x
        self.Y = y
        
    def getNormalVector(self):
        return [self.X, self.Y, 1]
    
    def __str__(self):
        return 'X: {:.3f} Y: {:.3f}'.format(self.X, self.Y)