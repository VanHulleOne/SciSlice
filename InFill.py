# -*- coding: utf-8 -*-
"""
Created on Thu Oct 29 15:45:02 2015

@author: lvanhulle
"""

import Line as l
import Point as p
import Shape as s

class InFill:
    
    def __init__(self, shape, angle, spacing, design):
        self.shape = shape
        self.angle = angle
        self.spacing = spacing
        if(design == None):
            point1 = p.Point(shape.minX, 0)
            point2 = p.Point(shape.maxX, 0)
            line = l.Line(point1, point2)
            self.design = s.Shape()
            self.design.addLine(line)
        else:
            self.design = design
        
        
