# -*- coding: utf-8 -*-
"""
Created on Tue Nov 03 09:46:30 2015

@author: lvanhulle
"""
import Point as p
import Line as l
import numpy as np
from operator import itemgetter
import copy

from parameters import constants as c
class LineGroup(object):
    
    def __init__(self, inGroup=None):
        self.minX = None
        self.minY = None
        self.maxX = None
        self.maxY = None
        
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
            
    def addLinesFromCoordinateList(self, coordList):
        pointList = []        
        for coord in coordList:
            pointList.append(p.Point(coord[c.X], coord[c.Y]))
        self.addLinesFromPoints(pointList)
    
    def addLinesFromPoints(self, pointList):
        for i in range(len(pointList)-1):
            self.append(l.Line(pointList[i], pointList[i+1]))
            
    def mirror(self, axis):
        tempLines = [line.mirror(axis) for line in self]
        tempLines.reverse()
        tempLines2 = []
        for line in tempLines:
            tempLines2.append(l.Line(line.end, line.start))
        cls = type(self)
        return cls(tempLines2)
    
    def translate(self, xShift, yShift,zShift=0):
        cls = type(self)
        return cls([line.translate(xShift, yShift, zShift) for line in self])        
        
    def rotate(self, angle, point=p.Point(0,0)):      
        cls = type(self)
        return cls([line.rotate(angle, point) for line in self])
        
    def getMidPoint(self):
        x = (self.maxX - self.minX)/2.0 + self.minX
        y = (self.maxY - self.minY)/2.0 + self.minY
        return p.Point(x, y)
    
    def nearestLine_Coro(self, key=None):
        lineList = copy.deepcopy(self.lines)
        used, testPoint = yield
        normList = []
        for line in lineList:
            normList.append(line.start.normalVector)
            normList.append(line.end.normalVector)
        normList = np.array(normList)
        while len(lineList) > 0:
            """
            This got a little complicated but sped up this section by about 10X
            This next line inside out does as follows:
            1) take the normList and subtract the normVector from the test point
                This actually subtracts the testPointNormVector from each individual
                element in the normList
            2) Use numpy.linalg.norm to get the length of each element. The first
                object is our subtracted array, None is for something I don't understand
                1 is so that it takes the norm of each element and not of the whole
                array
            3) enumerate over the array of norms so we can later have the index
            4) enumerate is a generator, so we are using a for comprehension to
                send the tuple (index, dist) to the min function. The norm stored
                in each element of the array is the distance from the testPoint to
                the point which was at that index
            5) Find the min of the tuples (index, dist) key-itemgetter(1) is telling min
                to look at dist when comparing the tuples
            6) min returns the lowest tuple, which we split into index and dist
            """
            index, dist = min(((index, dist) for index, dist in
                enumerate(np.linalg.norm(normList-testPoint.normalVector, None, 1))),
                key=itemgetter(1))
            if index%2: #If index is odd we are at the end of a line so the line needs to be flipped
                lineList[index/2].flip()
    
            used, testPoint = yield lineList[index/2], key, dist
            if not used and index%2:
                lineList[index/2].flip()
            if used:
                index /= 2
                lineList.pop(index)
                normList = np.delete(normList, [index*2, index*2+1],0)

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
        tempString = ''
        for line in self:
            tempString += line.CSVstr() + '\n'
        return tempString[:-1]