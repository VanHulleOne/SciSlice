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
#        print 'Start: ' + str(self.start)
#        print 'End: ' + str(self.end)
        self.length = self.distance(start, end)
        if(self.length == 0): print 'SNAFU detected, a line was created with no length.'
        self.upperLeft = None
        self.lowerRight = None
        self.setBoundingBox()
    
    def segmentsIntersect(self, other):
        if(not self.doBoundingBoxesIntersect(other)): return -1, None #return if bounding boxes do not intersect
        if(self.areColinear(other)): return 0, None #return if two lines are colinear
        
        r = numpy.subtract(self.end.getPoint(), self.start.getPoint())
        s = numpy.subtract(other.end.getPoint(), other.start.getPoint())
        Q_Less_P = numpy.subtract(other.start.getPoint(), self.start.getPoint())
        denom = numpy.cross(r, s)
        t = numpy.cross(Q_Less_P, s)/denom
        u = numpy.cross(Q_Less_P, r)/denom
        print 't: ' + str(t) + ' u" ' + str(u)
        if(abs(t) > 1 or abs(u) > 1):
            print 'Should we be here? segmentsIntersect math problem, I think'
        if(t == 1):
            return -3, p.Point(self.start.getX() + r[self.X]*t,
                          self.start.getY()+r[self.Y]*t) #lines meet at end point of self
        return 1, p.Point(self.start.getX() + r[self.X]*t,
                          self.start.getY()+r[self.Y]*t) #lines intersect at given point
        return -2, None #bounding boxes intersected but lines did not    
    
    def getArea(self, p1, p2, p3):
        """
        Uses the determinant of a matrix containing the three to find the area
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
            self.upperLeft.getY() >= other.lowerRight.getY() and
            self.lowerRight.getY() <= other.upperLeft.getY()):
                return True
        return False 
    
    def distance(self, start, end):
        """Returns the distance between two points"""
        return start.distance(end)
        
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
        tempList = [[self.start.x, self.end.x],
                     [self.start.y, self.end.y]]
        for row in tempList:
            row.sort()
        self.upperLeft = p.Point(tempList[0][0], tempList[1][1])
        self.lowerRight = p.Point(tempList[0][1], tempList[1][0])
        return None

#TODO: Remove that +1    
    def getMidPoint(self):
        x = (self.start.getX() - self.end.getX())/2.0 + self.end.getX()#+1
        y = (self.start.getY() - self.end.getY())/2.0 + self.end.getY()
        return p.Point(x, y)
        
    def getStart(self):
        return p.Point(self.start.getX(), self.start.getY())
        
    def getEnd(self):
        return p.Point(self.end.getX(), self.end.getY())
    
    def __str__(self):
        return str(self.start) + '\n' + str(self.end)
        
    def printBoudningBox(self):
        print 'Bounding Box for: ' + str(self)
        print str(self.upperLeft) + ', ' + str(self.lowerRight)