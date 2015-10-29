# -*- coding: utf-8 -*-
"""
Created on Wed Oct 28 14:09:55 2015

@author: lvanhulle
"""

class Shape:
    
    def __init__(self):
        self.lines = []
        self.minX = None
        self.minY = None
        self.maxX = None
        self.maxY = None
        
    def addLine(self, line):
        self.lines.append(line)
        if(line.upperLeft.getX() < self.minX): self.minX = line.upperLeft.getX()
        if(line.upperLeft.getY() > self.maxY): self.maxY = line.upperLeft.getY()
        if(line.lowerRight.getX() > self.maxX): self.maxX = line.lowerRight.getX()
        if(line.lowerRight.getY() < self.minY): self.mainY = line.lowerRight.getY()
    
    def testMethod(self):
        return 2*2