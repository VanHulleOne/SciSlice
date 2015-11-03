# -*- coding: utf-8 -*-
"""
Created on Tue Nov 03 09:46:30 2015

@author: lvanhulle
"""

class LineGroup(object):
    
    X, Y = 0, 1
    
    def __init__(self, inGroup):
        if(inGroup != None):
            self.lines = inGroup
            for line in self.lines:
                self.updateMinMax(line)
        else:
            self.lines = []
            self.minX = None
            self.minY = None
            self.maxX = None
            self.maxY = None
            
    def addLine(self, line):
        self.lines.append(line)
        self.updateMinMax(line)
        
    def updateMinMax(self, line):
        if(line.upperLeft.getX() < self.minX): self.minX = line.upperLeft.getX()
        if(line.upperLeft.getY() > self.maxY): self.maxY = line.upperLeft.getY()
        if(line.lowerRight.getX() > self.maxX): self.maxX = line.lowerRight.getX()
        if(line.lowerRight.getY() < self.minY): self.mainY = line.lowerRight.getY()

    def addLineGroup(self, inGroup):
        for line in inGroup:
            self.addLine(line)
            
    def mirror(self, axis):
        return LineGroup([line.mirror(axis) for line in self.lines])
    
    def translate(self, xShift, yShift):
        return LineGroup([line.translate(xShift, yShift) for line in self.lines])        
        
    def rotate(self, angle):
        return LineGroup([line.rotate(angle) for line in self.lines])
        
    def __str__(self):
        tempString = ''     
        for line in self.lines:
            tempString = tempString + str(line) + '\n'
        return tempString