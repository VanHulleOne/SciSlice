# -*- coding: utf-8 -*-
"""
Created on Wed Oct 28 14:09:55 2015

@author: lvanhulle
"""
import Line as l
import Point as p
class Shape:
    
    def __init__(self):
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
    
    def closeShape(self):
        if(self.lines[0].start != self.lines[-1].end):
            self.lines.append(l.Line(self.lines[-1].getEnd(),
                                     self.lines[0].getStart()))
                                     
    def isInside(self, point):
        """
        This method determines if the point is inside
        or outside the shape. Returns 1 if inside and 0 if outside.
        
        If a line is drawn from the point down to the outside of the part, the number
        of times that line intersects with the shape determines if the point was inside
        or outside. If the number of intersections is even then the point was outside
        of the shape. If the number of intersections is odd then the point is inside.
        """
        testLine = l.Line(point, p.Point(point.getX(), self.minY - 10))
        intersections = 0
        for line in self.lines:
            if(line.segmentsIntersect(testLine)): intersections += 1
        return (intersections % 2)
        
    