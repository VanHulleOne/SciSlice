# -*- coding: utf-8 -*-
"""
Created on Tue Oct 27 13:40:56 2015

@author: lvanhulle
"""
#import Point as p
import math

class Line:       
    def __init__(self, start, end):
        self.start = start
        self.end = end
        self.length = self.distance(start, end)
    
    def distance(self, start, end):
        """Returns the distance between two points"""
        return math.sqrt((start.X - end.X)**2 + (start.Y - end.Y)**2)
        
    def translate(self, shiftX, shiftY):
        self.start.translate(shiftX, shiftY)
        self.end.translate(shiftX, shiftY)
        
    def mirror(self, axis):
        self.start.mirror(axis)
        self.end.mirror(axis)
    
    def rotate(self, angle):
        self.start.rotate(angle)
        self.end.rotate(angle)
    
    def __str__(self):
        return '[' + str(self.start) + '], [' + str(self.end) + ']'