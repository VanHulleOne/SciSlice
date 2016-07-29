# -*- coding: utf-8 -*-
"""
Created on Tue Nov 03 17:08:13 2015

A small module for easily creating arcs and circles.

@author: lvanhulle
"""

from linegroup import LineGroup as LG
import math
from point import Point
from line import Line
import constants as c

class Arc(LG):
    
    def __init__(self, start, end, direction, center, numPoints=c.ARC_NUMPOINTS):
        LG.__init__(self, None)        
        self.start = start
        self.end = end
        self.direction = direction
        self.center = center
        self.numPoints = numPoints        
        self.arcToLines()
        
    def arcToLines(self):
        """Converts an arc to a set of line segments"""
        radius = self.start - self.center
        startAngle = math.atan2(self.start.y- self.center.y,
                            self.start.x - self.center.x)
        startAngle = startAngle if startAngle >= 0 else 2*math.pi+startAngle
        endAngle = math.atan2(self.end.y- self.center.y,
                            self.end.x- self.center.x)
        endAngle = endAngle if endAngle >= 0 else 2*math.pi+endAngle
        
        includedAngle = self.calcIncludedAngle(startAngle, endAngle)
        currentAngle = startAngle
        startPoint = Point(self.start.x, self.start.y)
        for i in range(self.numPoints-2):
            currentAngle += includedAngle/(self.numPoints-1)
            x = self.center.x+radius*math.cos(currentAngle)
            y = self.center.y+radius*math.sin(currentAngle)
            endPoint = Point(x, y)
            self.append(Line(startPoint, endPoint))
            startPoint = endPoint
        endPoint = Point(self.end.x, self.end.y)
        self.append(Line(startPoint, endPoint))
        
    def calcIncludedAngle(self, start, end):
        """
        Given an input of two angles, calculated in unit circle fashion, and the
        direction around the circle you want to travel, this method will return
        the total included angle.
        """    
        t = end - start
        if(self.direction == c.CW and t > 0):
            return t - 2*math.pi
        elif(self.direction == c.CCW and t < 0):
            return 2*math.pi+t
        elif(t == 0):
            return 2*math.pi
        else:
            return t
            
            