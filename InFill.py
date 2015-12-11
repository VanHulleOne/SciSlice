# -*- coding: utf-8 -*-
"""
Created on Thu Oct 29 15:45:02 2015

@author: lvanhulle
"""

import Line as l
import Point as p
import Shape as s
from LineGroup import LineGroup as LG
import LineGroup as lg
import parameters as pr

class InFill(LG):
    
    PARTIAL_ROW = 0
    FULL_ROW = 1
    FULL_FIELD = 2
    TRIMMED_FIELD = 3    
    
    def __init__(self, trimShape, design=None, designType=None):
        LG.__init__(self, None)        
        self.trimShape = s.Shape(trimShape)
        lowerLeft = p.Point(self.trimShape.minX, self.trimShape.minY)
        upperRight = p.Point(self.trimShape.maxX, self.trimShape.maxY)
        
        self.trimDiagonal = lowerLeft.distance(upperRight)*1.1       
        self.operations = {0 : self.extendDesign,
                           1 : self.createField,
                           2 : self.trimField}
        
        if(design is None):
            point1 = p.Point(-self.trimDiagonal-10, 0)
            point2 = p.Point(self.trimDiagonal+10, 0)
            self.design = lg.LineGroup([l.Line(point1, point2)])
            self.designType = self.PARTIAL_ROW
        else:
            self.design = design
        
        for i in range(self.designType, self.TRIMMED_FIELD):
            self.operations[i]();
            
        self.lines.sort()
        
    def extendDesign(self):
        tempDesign = lg.LineGroup(self.design.lines)
        designWidth = self.design.maxX - self.design.minX        
        while(designWidth <= self.trimDiagonal):
            shiftX = self.design[-1].end.x - tempDesign[0].start.x
            shiftY = self.design[-1].end.y - tempDesign[0].start.y
            self.design.addLineGroup(tempDesign.translate(shiftX, shiftY))
            designWidth = self.design.maxX - self.design.minX 
            print "here line 54 Infill"
        
    def createField(self):
        tempDesign = self.design.translate(0, pr.pathWidth)
        designHeight = abs(self.design.maxY - self.design.minY)
        while(designHeight < self.trimDiagonal):
            self.design.addLineGroup(tempDesign)
            tempDesign = tempDesign.translate(0, pr.pathWidth)
            designHeight += pr.pathWidth
        self.centerAndRotateField()
        
    def trimField(self):
        tempLines = []
        for line in self.design.lines:
            pointSet = set([line.getStart()])
            for tLine in self.trimShape.lines:
                result, point = tLine.segmentsIntersect(line)
                if(result == 1):
                    pointSet.add(point)
            pointSet.add(line.getEnd())
            pointList = sorted(list(pointSet))
            for i in range(len(pointList)-1):                
                tempLines.append(l.Line(pointList[i], pointList[i+1]))
        for i in range(len(tempLines)):
            if(self.trimShape.isInside(tempLines[i].getMidPoint())):
                self.lines.append(tempLines[i])
    
    def centerAndRotateField(self):
        designCP = self.design.getMidPoint()
        trimShapeCP = self.trimShape.getMidPoint()
        transX = trimShapeCP.x - designCP.x
        transY = trimShapeCP.y - designCP.y
        self.design = self.design.translate(transX, transY)
        self.design = self.design.rotate(pr.backgroundAngle, trimShapeCP)
        