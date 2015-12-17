# -*- coding: utf-8 -*-
"""
Created on Tue Nov 03 09:46:30 2015

@author: lvanhulle
"""
import Point as p
import Line as l

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