# -*- coding: utf-8 -*-
"""
Created on Tue Oct 27 13:13:34 2015

@author: lvanhulle
"""
import numpy
import math
class Point:
    X, Y, Z = 0, 1, 2
    
    def __init__(self, x, y, z=0):
        self.x = x
        self.y = y
        self.z = z
        self.normalVector = numpy.array([x, y, z, 1])
        
    def get2DPoint(self):
        return [self.x, self.y]
        
    def mirror(self, axis):
        transMatrix = numpy.identity(4)
        if(axis == self.X):
            transMatrix[self.Y][1] = -1
        else:
            transMatrix[self.X][0] = -1
        return self.transform(transMatrix)
    
    def rotate(self, angle, point):
        if(point is None): point = Point(0,0)
        toOrigin = numpy.identity(4)
        toOrigin[self.X][3] = -point.x
        toOrigin[self.Y][3] = -point.y
        
        rotateMatrix = numpy.identity(4)
        rotateMatrix[self.X][0] = math.cos(angle)
        rotateMatrix[self.Y][0] = math.sin(angle)
        rotateMatrix[self.X][1] = -rotateMatrix[self.Y][0]
        rotateMatrix[self.Y][1] = rotateMatrix[self.X][0]
        
        transBack = numpy.identity(4)
        transBack[self.X][3] = point.x
        transBack[self.Y][3] = point.y
        
        transMatrix = numpy.dot(transBack, numpy.dot(rotateMatrix, toOrigin))
        return self.transform(transMatrix)
    
    def translate(self, shiftX, shiftY, shiftZ=0):
        transMatrix = numpy.identity(4)
        transMatrix[self.X][3] = shiftX
        transMatrix[self.Y][3] = shiftY
        transMatrix[self.Z][3] = shiftZ
        return self.transform(transMatrix)
        
    def transform(self, transMatrix):
        nv = numpy.dot(transMatrix, self.normalVector)
        return Point(nv[self.X], nv[self.Y], nv[self.Z])
        
    def distance(self, other):
        return numpy.linalg.norm(self.normalVector - other.normalVector)
        
    def squareDistance(self, other):
        return ((self.x - other.x)**2 + (self.y - other.y)**2)
    
#TODO: __cmp__ isn't used in Python 3.0 or later so this should eventually be
    #converted to the 6 rich comparison methods
#TODO: Add comparisons for Z
    def __cmp__(self, other):
        if(self.x > other.x): return 1
        if(self.x < other.x): return -1
        if(self.y > other.y): return 1
        if(self.y < other.y): return -1
        return 0
    
    def __lt__(self, other):
        if(self.x < other.x): return True
        if(self.x > other.x): return False
        if(self.y < other.y): return True
        return False
        
    def __eq__(self, other):
        return (self.x == other.x and self.y == other.y)
    
    def __str__(self):
        return 'X{:.3f} Y{:.3f} Z{:.3f}'.format(self.x, self.y, self.z)
        
    def getX(self):
        return self.normalVector[self.X]
    
    def getY(self):
        return self.normalVector[self.Y]
    
    def getNormalVector(self):
        nv = [n for n in self.normalVector]
        return nv
        
    def __eq__(self, other):
        return (self.getX() == other.getX() and self.getY() == other.getY())
        
    def __ne__(self, other):
        return not (self.getX() == other.getX() and self.getY() == other.getY())