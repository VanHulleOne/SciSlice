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
from operator import itemgetter
import matrixTrans as mt
import constants as c
from collections import namedtuple
import copy
import numpy.ma as ma

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
        if(line.upperLeft.x < self.minX or self.minX is None): self.minX = line.upperLeft.x
        if(line.upperLeft.y > self.maxY or self.maxY is None): self.maxY = line.upperLeft.y
        if(line.lowerRight.x > self.maxX or self.maxX is None): self.maxX = line.lowerRight.x
        if(line.lowerRight.y < self.minY or self.minY is None): self.minY = line.lowerRight.y

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
        if self.__vectors is None:
            self.__vectors = np.array([line.vector for line in self])
        return self.__vectors
    
    @property    
    def starts(self):
        if self.__starts is None:
            self.__starts = np.array([line.start.get2DPoint() for line in self])
        return self.__starts
    
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
        for i in xrange(0,len(result),2):
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

    @profile
    def nearestLine_Coro(self, name=None):
        lineList = self.lines[:]#copy.deepcopy(self.lines)
        used, testPoint = yield
        normList = np.array([point.normalVector for point in self.iterPoints()])
        while len(normList[(normList < np.inf)]) > 0:# len(lineList) > 0:
            """
            This got a little complicated but sped up this section by about 10X
            This next line from inside to out does as follows:
            1) take the normList and subtract the normVector from the test point
                This actually subtracts the testPointNormVector from each individual
                element in the normList
            2) Use numpy.linalg.norm to get the length of each element. The first
                object is our subtracted array, None is for something I don't understand
                1 is so that it takes the norm of each element and not of the whole
                array
            3) enumerate over the array of norms so we can later have the index
            4) Find the min of the tuples (index, dist) key-itemgetter(1) is telling min
                to look at dist when comparing the tuples
            5) min returns the lowest tuple, which we split into index and dist
            """
            distances = np.linalg.norm(normList-testPoint.normalVector, None, 1)#, key=itemgetter(1))
            index = np.argmin(dist)            
            if index%2: #If index is odd we are at the end of a line so the line needs to be flipped
                lineList[index/2] = lineList[index/2].fliped()
    
            used, testPoint = yield self.Result(lineList[index/2], name, distances[index])
            if not used and index%2:
                """ If the line was not used and we had flipped it we need to
                flip it back so that it still matches the orientation in normList. """
                lineList[index/2] = lineList[index/2].fliped()
            if used:
                index /= 2
#                lineList.pop(index)
                normList[index*2:index*2+2] = np.inf # = np.delete(normList, [index*2, index*2+1],0)
    
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