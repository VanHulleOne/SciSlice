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
        newStart = self.start.translate(shiftX, shiftY)
        newEnd = self.end.translate(shiftX, shiftY)
        return Line(newStart, newEnd)
        
    def mirror(self, axis):
        newStart = self.start.mirror(axis)
        newEnd = self.end.mirror(axis)
        return Line(newStart, newEnd)
    
    def rotate(self, angle):
        newStart = self.start.rotate(angle)
        newEnd = self.end.rotate(angle)
        return Line(newStart, newEnd)
    
    def __str__(self):
        return '[' + str(self.start) + '], [' + str(self.end) + ']'