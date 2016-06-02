# -*- coding: utf-8 -*-
"""
Created on Tue Nov 03 09:46:30 2015

LineGroup at its core is simply a list of lines and the operations we can perform
on them. It keeps track of various characteristics of the lines as they are entered
so they do not need to be calculated when called.

@author: lvanhulle
"""
import Point as p
import Line as l
import numpy as np
import matrixTrans as mt
import constants as c
from collections import namedtuple

class LineGroup(object):
    
    Result = namedtuple('Result', 'line name distance')
    
    def __init__(self, inGroup=None):
        self.minX = None
        self.minY = None
        self.maxX = None
        self.maxY = None
        self.__starts = None
        self.__vectors = None
        
        try:
            self.lines = list(inGroup)
        except Exception:
            self.lines = []
        else:
            for line in self:
                self.updateMinMax(line)
    
    def updateMinMax(self, line):
        if(self.minX is None or line.upperLeft.x < self.minX): self.minX = line.upperLeft.x
        if(self.maxY is None or line.upperLeft.y > self.maxY): self.maxY = line.upperLeft.y
        if(self.maxX is None or line.lowerRight.x > self.maxX): self.maxX = line.lowerRight.x
        if(self.minY is None or line.lowerRight.y < self.minY): self.minY = line.lowerRight.y

    def addLineGroup(self, inGroup):
        for line in inGroup:
            self.append(line)
            
    def fourCorners(self):
        corners = []
        corners.append(p.Point(self.minX, self.minY))
        corners.append(p.Point(self.maxX, self.minY))
        corners.append(p.Point(self.maxX, self.maxY))
        corners.append(p.Point(self.minX, self.maxY))
        return corners
    
    @property       
    def vectors(self):
        return np.array([line.vector for line in self])
#        if self.__vectors is None:
#            self.__vectors = np.array([line.vector for line in self])
#        return self.__vectors
    
    @property    
    def starts(self):
        return np.array([line.start.get2DPoint() for line in self])
#        if self.__starts is None:
#            self.__starts = np.array([line.start.get2DPoint() for line in self])
#        return self.__starts
    
    def addLinesFromCoordinateList(self, coordList):
        pointList = []        
        for coord in coordList:
            pointList.append(p.Point(coord[c.X], coord[c.Y]))
        self.addLinesFromPoints(pointList)
    
    def addLinesFromPoints(self, pointList):
        for i in range(len(pointList)-1):
            self.append(l.Line(pointList[i], pointList[i+1]))
            
    def mirror(self, axis):
        return self.transform(mt.mirrorMatrix(axis))
    
    def translate(self, xShift, yShift,zShift=0):
        return self.transform(mt.translateMatrix(xShift, yShift, zShift))      
        
    def rotate(self, angle, point=p.Point(0,0)):
        return self.transform(mt.rotateMatrix(angle, point))
  
    def transform(self, transMatrix):
        cls = type(self)
        numpyArray = np.array([point.normalVector for point in self.iterPoints()])        
        result = np.inner(numpyArray, transMatrix)
        lines = []        
        for i in range(0,len(result),2):
            start = p.Point(result[i])
            end = p.Point(result[i+1])
            lines.append(l.Line(start, end, self[i%2]))
        transShape = cls()
        transShape.lines = lines
        transShape.minX, transShape.minY = np.amin(result[:,:2], axis=0)
        transShape.maxX, transShape.maxY = np.amax(result[:,:2], axis=0)
        return transShape
    
    def getMidPoint(self):
        x = (self.maxX - self.minX)/2.0 + self.minX
        y = (self.maxY - self.minY)/2.0 + self.minY
        return p.Point(x, y)
    
    def lineOutsideBoundingBox(self, line):
        startX = line.start.x
        startY = line.start.y
        endX = line.end.x
        endY = line.end.y
        if(startX < self.minX > endX): return True # Both ends are less than minX
        if(startX > self.maxX < endX): return True # Both ends are greater than maxX
        if(startY < self.minY > endY): return True # Both ends are less than minY
        if(startY > self.maxY < endY): return True # Both ends are greater than maxY
        return False

    def nearestLine_Coro(self, name=None):
        used, testPoint = yield
        normList = np.array([point.normalVector for point in self.iterPoints()])
        while len(normList[(normList < np.inf)]) > 0:
            """ Continue working until all items have been used/are set to infinity. """

            distances = np.linalg.norm(normList-testPoint.normalVector, None, 1)
            index = np.argmin(distances)
            nearestLine = self[index//2]
            if index%2:
                """ If index is odd we are at the end of a line so the line needs to be flipped. """
                nearestLine = nearestLine.fliped()
    
            used, testPoint = yield self.Result(nearestLine, name, distances[index])
            if used:
                index //= 2
                """ Instead of deleting the points from the NumPy array, which
                causes a new array to be made, we instead set the used points to
                infinity which means they will never be a minimum distance. """
                normList[[index*2,index*2+1]] = np.inf
    
    def append(self, line):
        self.lines.append(line)
        self.updateMinMax(line)
    
    def remove(self, line):
        self.lines.remove(line)
    
    def sort(self):
        self.lines.sort()
    
    def pop(self, index=-1):
        return self.lines.pop(index)
    
    def __add__(self, other):
        cls = type(self)
        return cls(list(self)+list(other))
    
    def iterPoints(self):
        for line in self:
            yield line.start
            yield line.end
    
    def __getitem__(self, index):
        return self.lines[index]
    
    def __len__(self):
        return len(self.lines)
        
    def __iter__(self):
        return iter(self.lines)
    
    def __str__(self):
        tempString = ''     
        for line in self.lines:
            tempString = tempString + str(line) + '\n'
        return tempString
        
    def CSVstr(self):
        """ Creates a comma seperated value string. """
        tempString = ''
        for line in self:
            tempString += line.CSVstr() + '\n'
        return tempString[:-1]