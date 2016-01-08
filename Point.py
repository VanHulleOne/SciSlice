# -*- coding: utf-8 -*-
"""
Created on Tue Oct 27 13:13:34 2015

@author: lvanhulle
"""
import numpy
import math
from parameters import constants as c
import matrixTrans as mt
class Point(object):
    
    COMPARE_PRECISION = 10000
    
    def __init__(self, x, y=None, z=0):
        try:
            len(x)
        except:            
            self.x = x
            self.y = y
            self.z = z
            if y is None:
                raise Exception('You did not initialize a Point correctly')
        else:
            self.x = x[c.X]
            self.y = x[c.Y]
            self.z = x[c.Z]
        self.normalVector = numpy.array([x, y, z, 1])
        
    @property
    def x(self):
        return self.__x/float(self.COMPARE_PRECISION)
        
    @x.setter
    def x(self, value):
        self.__x = int(round(value*self.COMPARE_PRECISION))
        
    @property
    def y(self):
        return self.__y/float(self.COMPARE_PRECISION)
        
    @y.setter
    def y(self, value):
        self.__y = int(round(value*self.COMPARE_PRECISION))
    
    @property
    def z(self):
        return self.__z/float(self.COMPARE_PRECISION)
        
    @z.setter
    def z(self, value):
        self.__z = int(round(value*self.COMPARE_PRECISION))
    
    def __iter__(self):
        return(i for i in (self.x, self.y, self.z))
    
    def get2DPoint(self):
        return [self.x, self.y]
    
    def mirror(self, axis):
        return self.transform(mt.mirrorMatrix(axis))
    
    def rotate(self, angle, point=None):
        return self.transform(mt.rotateMatrix(angle, point))
    
    def translate(self, shiftX, shiftY, shiftZ=0):
        return self.transform(mt.translateMatrix(shiftX, shiftY, shiftZ))
        
    def transform(self, transMatrix):
        nv = numpy.dot(transMatrix, self.normalVector)
        return Point(nv[c.X], nv[c.Y], nv[c.Z])
        
    def __getitem__(self, index):
        return self.normalVector[index]
    
    def __sub__(self, other):
        return numpy.linalg.norm(self.normalVector - other.normalVector)
        
    def __neg__(self):
        return Point(-self.x, -self.y)
    
    def squareDistance(self, other):
        return ((self.x - other.x)**2 + (self.y - other.y)**2)

    def __key(self):
        return (self.__z, self.__x, self.__y)
    
    def __lt__(self, other):
        return self.__key() < other.__key()
        
    def __gt__(self, other):
        return self.__key() > other.__key()

    def __eq__(self, other):
        return self.__key() == other.__key()
        
    def __ne__(self, other):
        return self.__key() != other.__key()
        
    def __hash__(self):
        return hash(self.__key())
    
    def CSVstr(self):
        return '{:.3f},{:.3f}'.format(self.x, self.y)
    
    def __str__(self):
        return 'X{:.3f} Y{:.3f} Z{:.3f}'.format(self.x, self.y, self.z)
    
    def getNormalVector(self):
        nv = [n for n in self.normalVector]
        return nv
        
    