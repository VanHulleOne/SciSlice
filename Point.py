# -*- coding: utf-8 -*-
"""
Created on Tue Oct 27 13:13:34 2015

@author: lvanhulle
"""
import numpy
import math
class Point:
    X, Y = 0, 1
    
    def __init__(self, x, y):
        self.x = x
        self.y = y        
        self.normalVector = [x, y, 1]
        
    def getPoint(self):
        return self.normalVector[self.X:self.Y+1]
        
    def mirror(self, axis):
        transMatrix = numpy.identity(3)
        if(axis == self.X):
            transMatrix[self.Y][1] = -1
        else:
            transMatrix[self.X][0] = -1
        return self.transform(transMatrix)
    
    def rotate(self, angle):
        transMatrix = numpy.identity(3)
        transMatrix[self.X][0] = math.cos(angle)
        transMatrix[self.Y][0] = math.sin(angle)
        transMatrix[self.X][1] = -transMatrix[self.Y][0]
        transMatrix[self.Y][1] = transMatrix[self.X][0]
        return self.transform(transMatrix)
    
    def translate(self, shiftX, shiftY):
        transMatrix = numpy.identity(3)
        transMatrix[self.X][2] = shiftX
        transMatrix[self.Y][2] = shiftY
        return self.transform(transMatrix)
        
    def transform(self, transMatrix):
        nv = numpy.dot(transMatrix, self.normalVector)
        return Point(nv[self.X], nv[self.Y])
        
    def distance(self, other):
        return math.sqrt((self.x - other.x)**2 + (self.y - other.y)**2)
    
    def __str__(self):
        return 'X: {:.3f} Y: {:.3f}'.format(self.normalVector[self.X], self.normalVector[self.Y])
        
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