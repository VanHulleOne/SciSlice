# -*- coding: utf-8 -*-
"""
Created on Tue Oct 27 13:40:56 2015

@author: lvanhulle
"""
import Point as p
import numpy
from parameters import constants as c

class Line:
    def __init__(self, start, end):
        self.start = start
        self.end = end
        self.length = start.distance(end)
        if(self.length == 0):
            print ('SNAFU detected, a line was created with no length at: ' + 
                    str(self.start))
        self.upperLeft = None
        self.lowerRight = None
        self.setBoundingBox()
    
    def segmentsIntersect(self, other, allowProjInt = False):
        if(not(allowProjInt) and not(self.doBoundingBoxesIntersect(other))): return -1, None #return if bounding boxes do not intersect
        if(self.areColinear(other)):
            pointList = sorted([self.start, self.end, other.start, other.end])
            if(self.doBoundingBoxesIntersect(other)):                
                return 2, pointList[1:3] #If lines are colinear and they overlap then there are two intersections
            else:
                tempLine = Line(pointList[1], pointList[2])
                return -2, tempLine.getMidPoint() #If they are colinear and do not overlap return half way inbetween lines
        
        r = numpy.subtract(self.end.get2DPoint(), self.start.get2DPoint())
        s = numpy.subtract(other.end.get2DPoint(), other.start.get2DPoint())
        Q_Less_P = numpy.subtract(other.start.get2DPoint(), self.start.get2DPoint())
        denom = numpy.cross(r, s)*1.0
        t = numpy.cross(Q_Less_P, s)/denom
        u = numpy.cross(Q_Less_P, r)/denom
        #If t or u are not in the range 0-1 then the intersection is projected
        if(t > 1 or u > 1 or t < 0 or u < 0):
            return -1, p.Point(self.start.x + r[c.X]*t,
                          self.start.y+r[c.Y]*t) #return for projected intersection of non-colinear lines

        return 1, p.Point(self.start.x + r[c.X]*t,
                          self.start.y+r[c.Y]*t) #lines intersect at given point
           
    
    def isOnLine(self, point):
        if((point < self.start and point < self.end) or (
            point > self.start and point > self.end)):
            return False #point is not between the start and end of self
        
        if(self.getArea(self.start, self.end, point) > 0.0001):
            return False #points are not co-linear
        
        return True
    
    def getArea(self, p1, p2, p3):
        """
        Uses the determinant of a matrix containing the three to find the area
        of the triangle formed by the three points.
        """
        matrix = [p1.getNormalVector(), p2.getNormalVector(), p3.getNormalVector(), [1,1,1,1]]
        matrix = numpy.rot90(matrix)
        return abs(numpy.linalg.det(matrix))/2.0
    
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
        if(self.upperLeft.x <= other.lowerRight.x and
            self.lowerRight.x >= other.upperLeft.x and
            self.upperLeft.y >= other.lowerRight.y and
            self.lowerRight.y <= other.upperLeft.y):
                return True
        return False 
        
    def translate(self, shiftX, shiftY, shiftZ=0):
        newStart = self.start.translate(shiftX, shiftY, shiftZ)
        newEnd = self.end.translate(shiftX, shiftY, shiftZ)
        return Line(newStart, newEnd)
        
    def mirror(self, axis):
        newStart = self.start.mirror(axis)
        newEnd = self.end.mirror(axis)
        return Line(newStart, newEnd)
    
    def rotate(self, angle, point):
        if(point is None): point = p.Point(0,0)
        newStart = self.start.rotate(angle, point)
        newEnd = self.end.rotate(angle, point)
        return Line(newStart, newEnd)

    def flip(self):
        self.start, self.end = self.end, self.start
        
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
    
    def getMidPoint(self):
        x = (self.start.x - self.end.x)/2.0 + self.end.x
        y = (self.start.y - self.end.y)/2.0 + self.end.y
        return p.Point(x, y)
        
    def getStart(self):
        return p.Point(self.start.x, self.start.y, self.start.z)
        
    def getEnd(self):
        return p.Point(self.end.x, self.end.y, self.end.z)
    
    def __lt__(self, other):
        selfLower = self.start if self.start < self.end else self.end
        otherLower = other.start if other.start < other.end else other.end
        return (selfLower < otherLower)
        
    def __eq__(self, other):
        return (self.start == other.start and self.end == other.end)
        
    
    def __str__(self):
        return str(self.start) + '    \t' + str(self.end)
        
    def printBoudningBox(self):
        print 'Bounding Box for: ' + str(self)
        print str(self.upperLeft) + ', ' + str(self.lowerRight)