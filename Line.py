# -*- coding: utf-8 -*-
"""
Created on Tue Oct 27 13:40:56 2015

@author: lvanhulle
"""
import Point as p
import math

class Line:  
    def __init__(self, start, end):
        self.start = start
        self.end = end
        self.length = self.distance(start, end)
        self.upperLeft
        self.lowerRight
        self.setBoundingBox()
    
    def doSegmentsIntersect(self, other):
        if(not self.doBoundingBoxesIntersect(other)): return -1, None #return if bounding boxes do not intersect
    
    def doBoundingBoxesIntersect(self, other):
        if(self.upperLeft.getX() <= other.lowerRight.getX() and
            self.lowerRight.getX() >= other.upperLeft.getX() and
            self.upperRight.getY() >= other.lowerRight.getY() and
            self.lowerRight.getY() <= other.upperLeft.getY()):
                return True
    return False
    
    def getOrientation(self, other):
        """
    getOrientation takes in three points,
    returns 0 if they are colinear
    returns 1 if the turn is clockwise
    returns 2 if the turn is CCW
    """
    val = ((p2[Y] - p1[Y])*(p3[X] - p2[X]) - 
            (p2[X] - p1[X])*(p3[Y] - p2[Y]))
    if(val == 0): return 0 #colinear
    return (1 if val > 0 else 2)
    
    def segmentsIntersect(p1, p2, q1, q2):
        if(not boundingBoxesIntersect(p1, p2, q1, q2)): return -1, None #return if bounding boxes do not intersetc
        o1 = getOrientation(p1, p2, q1)
        o2 = getOrientation(p1, p2, q2)
        o3 = getOrientation(q1, q2, p1)
        o4 = getOrientation(q1, q2, p2)
        
        if((o1+o2+o3+o4) == 0): return 0, None #return if all 4 points are colinear
        
        if(o1 != o2 and o3 != o4):
            r = numpy.subtract(p2, p1)
            s = numpy.subtract(q2, q1)
            Q_Less_P = numpy.subtract(q1, p1)
            denom = numpy.cross(r, s)
            t = numpy.cross(Q_Less_P, s)/denom
            u = numpy.cross(Q_Less_P, r)/denom
            if(abs(t) > 1 or abs(u) > 1):
                print 'Should we be here? segmentsIntersect math problem, I think'
            return 1, [p1[X]+r[X]*t, p1[Y]+r[Y]*t] #lines intersect at given point
            return -2, None #bounding boxes intersected but lines did not    
    
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

    def setBoundingBox(self):
        """
        Set the upper left and lower right coordinates of the smallest box
        which containts the line.
        """
        tempList = [[self.start.getX(), self.end.getX()],
                     [self.start.getY(), self.end.getY()]]
        for row in tempList:
            row.sort()
        upperLeft = p.Point(tempList[0][0], tempList[1][1])
        lowerRight = p.Point(tempList[0][1], tempList[1][0])
    
    def __str__(self):
        return '[' + str(self.start) + '], [' + str(self.end) + ']'
        
    def printBoudningBox(self):
        print 'Bounding Box for: ' + str(self)
        print str(upperLeft) + ', ' + str(lowerRight)