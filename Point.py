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
        self.normalVector = [x, y, 1]
        
    def getPoint(self):
        return self.normalVector[self.X:self.Y]
        
    def reflect(self, axis):
        transMatrix = numpy.identity(3)
        if(axis == self.X):
            transMatrix[self.Y][1] = -1
        else:
            transMatrix[self.X][0] = -1
        self.transform(transMatrix)
    
    def rotate(self, angle):
        transMatrix = numpy.identity(3)
        transMatrix[self.X][0] = math.cos(angle)
        transMatrix[self.Y][0] = math.sin(angle)
        transMatrix[self.X][1] = -transMatrix[self.Y][0]
        transMatrix[self.Y][1] = transMatrix[self.X][0]
        self.transform(transMatrix)
    
    def translate(self, shiftX, shiftY):
        transMatrix = numpy.identity(3)
        transMatrix[self.X][2] = shiftX
        transMatrix[self.Y][2] = shiftY
        self.transform(transMatrix)
        
    def transform(self, transMatrix):
        self.normalVector = numpy.dot(transMatrix, self.normalVector)
        
    def __str__(self):
        return 'X: {:.3f} Y: {:.3f}'.format(self.normalVector[self.X], self.normalVector[self.Y])