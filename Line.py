# -*- coding: utf-8 -*-
"""
Created on Tue Oct 27 13:40:56 2015

@author: lvanhulle
"""
#import Point as p
import math

class Line:
    X, Y = 0, 1      
    def __init__(self, start, end):
        self.start = start
        self.end = end
        self.length = self.distance(start, end)
        self.boundingBox = []
    
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
#TODO: Keep working on boundingBox
        #I think I should sort the points and that would make it easier
    def getBoundingBox(self):
        """
        Given two points marking the ends of a line, return the upper left
        and lower right coordinates of the smallest box which containts the line.
        """
        if(self.start.normalVector[Y] == self.end.normalVector[Y]):
            self.boudingBox = ([self.start, self.end] if self.start.normalVector[X] <
                self.end.normalVector[X] else [self.end, self.start])
        if(self.start.normalVector[X] == self.end.normalVector[X]):
            self.boundingBox = ([self.start, self.end] if self.start.normalVector[Y] >
                self.end.normalVector[Y] else [self.end, self.start])
        upperLeft = [None]*2
        lowerRight = [None]*2
        upperLeft[X], lowerRight[X] = orderTwoNumbers(p1[X], p2[X])
        lowerRight[Y], upperLeft[Y] = orderTwoNumbers(p1[Y], p2[Y])
        return (upperLeft, lowerRight)
    
    def __str__(self):
        return '[' + str(self.start) + '], [' + str(self.end) + ']'