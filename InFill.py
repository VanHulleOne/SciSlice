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

class InFill(LG):
    
    PARTIAL_ROW = 0
    FULL_ROW = 1
    FULL_FIELD = 2
    TRIMMED_FIELD = 3    
    
    def __init__(self, trimShape, angle, spacing, design, designType):
        LG.__init__(self, None)        
        self.trimShape = trimShape
        self.angle = angle
        self.spacing = spacing
        
        self.operations = {0 : self.extendDesign,
                           1 : self.createField,
                           2 : self.trimField}
        
        if(design == None):
            point1 = p.Point(trimShape.minX, 0)
            point2 = p.Point(trimShape.maxX, 0)
            lineList = [l.Line(point1, point2)]
            self.design = lg.LineGroup(lineList)
            self.designType = self.FULL_ROW
        else:
            self.design = design
        
        for i in range(self.designType, self.TRIMMED_FIELD):
            self.operations[i]();
        
    def extendDesign(self):
        tempDesign = lg.LineGroup(self.design)
        designWidth = self.design.maxX - self.design.minX
        trimWidth = self.trimShape.maxX - self.trimShape.minX
        
        while(designWidth < trimWidth):
            shiftX = self.design.lines[-1].end.getX() - self.tempDesign.lines[0].start.getX()
            shiftY = self.design.lines[-1].end.getY() - self.tempDesign.lines[0].start.getY()
            self.design.addLineGroup(tempDesign.translate(shiftX, shiftY))
        self.centerDesignBelowTrim() 
        
    def createField(self):
        tempDesign = self.design.translate(0, self.spacing)
        while(tempDesign.minY < self.trimShape.maxY):
            self.design.addLineGroup(tempDesign)
            tempDesign = tempDesign.translate(0, self.spacing)
#            print 'tempDesign: ' + str(tempDesign)
#            print ' minY: ' + tempDesign.minY
#            print ' tS.maxY: ' + self.trimShape.maxY
        
    def trimField(self):
        tempLines = []
        for line in self.design.lines:
            pointList = [line.getStart()]
            for tLine in self.trimShape.lines:
                result, point = line.segmentsIntersect(tLine)
                if(result == 1):
                    pointList.append(point)
            pointList.append(line.getEnd())
            for i in range(len(pointList)-1):
                tempLines.append(l.Line(pointList[i], pointList[i+1]))
        for line in tempLines:
            print str(line)
        for i in range(len(tempLines)):
            if(self.trimShape.isInside(tempLines[i].getMidPoint())):
                print 'Added a temp line.'
                self.lines.append(tempLines[i])
    
    def centerDesignBelowTrim(self):
        designCP = self.design.getMidPoint()
        trimShapeCP = self.trimShape.getMidPoint()
        transX = trimShapeCP.getX() - designCP.getX()
        transY = trimShapeCP.minY - designCP.maxY
        self.design = self.design.translate(transX, transY)
        