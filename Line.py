# -*- coding: utf-8 -*-
"""
Created on Tue Oct 27 13:40:56 2015

@author: lvanhulle
"""
import Point as p
import math
import numpy

class Line:
    X, Y = 0, 1
    def __init__(self, start, end):
        self.start = start
        self.end = end
        self.length = self.distance(start, end)
        if(length == 0): print 'SNAFU detected, a line was created with no length.'
        self.upperLeft
        self.lowerRight
        self.setBoundingBox()
    
    def doSegmentsIntersect(self, other):
        if(not self.doBoundingBoxesIntersect(other)): return -1, None #return if bounding boxes do not intersect
        if(self.areColinear(other)): return 0, None #return if two lines are colinear
        
        r = numpy.subtract(self.end.getPoint(), self.start.getPoint())
        s = numpy.subtract(other.end.getPoint(), other.start.getPoint())
        Q_Less_P = numpy.subtract(other.start.getPoint(), self.start.getPoint())
        denom = numpy.cross(r, s)
        t = numpy.cross(Q_Less_P, s)/denom
        u = numpy.cross(Q_Less_P, r)/denom
        if(abs(t) > 1 or abs(u) > 1):
            print 'Should we be here? segmentsIntersect math problem, I think'
        return 1, p.Point(self.start.getX() + r[self.X]*t,
                          self.start.getY()+r[self.Y]*t) #lines intersect at given point
        return -2, None #bounding boxes intersected but lines did not    
    
    def getArea(self, p1, p2, p3):
        """
        Uses the determinant of a matrix conataining the three to find the area
        of the triangle formed by the three points.
        SPECIAL NOTE: the area is actually 1/2 the determinant but I have
        left out that extra, unneeded calculation.
        """
        matrix = [p1.getNormalVector(), p2.getNormalVector(), p3.getNormalVector()]
        matrix = numpy.rot90(matrix)
        return abs(numpy.linalg.det(matrix))
    
    def areColinear(self, other):
        """
        If the area of the two created triangles is less than the tolerance
        than the two lines are assumed to be co-linear.
        """
        tolerance = 0.0001        
        area = self.getArea(self.start, self.end, other.start)
        area += self.getArea(self.start, self.end, other.end)
        if(area < tolerance): return True
        return False        
    
    def doBoundingBoxesIntersect(self, other):
        if(self.upperLeft.getX() <= other.lowerRight.getX() and
            self.lowerRight.getX() >= other.upperLeft.getX() and
            self.upperRight.getY() >= other.lowerRight.getY() and
            self.lowerRight.getY() <= other.upperLeft.getY()):
                return True
    return False 
    
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