# -*- coding: utf-8 -*-
"""
Created on Thu Oct 29 15:45:02 2015

@author: lvanhulle
"""

import Line as l
import Point as p
import Shape as s
from LineGroup import LineGroup as LG

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
            line = l.Line(point1, point2)
            self.design = LG.LineGroup(line)
            self.designType = self.FULL_ROW
        else:
            self.design = design
        
        for i in range(self.designType, self.TRIMMED_FIELD):
            self.operations[i]();
        
    def extendDesign(self):
        return 1
        
    def createField(self):
        return 1
        
    def trimField(self):
        return 1
    