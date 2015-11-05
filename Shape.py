# -*- coding: utf-8 -*-
"""
Created on Wed Oct 28 14:09:55 2015

@author: lvanhulle
"""
import Line as l
import Point as p
from LineGroup import LineGroup as LG

class Shape(LG):    
    def __init__(self, shape):
        LG.__init__(self, shape)
        self.shapeIsClosed = self.isShapeClosed() #False
        
    def addInternalShape(self, inShape):
        if(not inShape.shapeIsClosed):
            print '********** Your internal shape was not closed. **********'
        if(not self.isInside(inShape.lines[0].start)):
            print '********** The internal shape is not inside the main shape. **********'
        if(self.doShapesIntersect(inShape)):
            print '********** Internal shape is not completely inside main shape. **********'
        
        for line in inShape.lines:
            self.lines.append(line)
    
    def doShapesIntersect(self, inShape):
        for line in self.lines:
            for line2 in inShape.lines:
                result, point = line.segmentsIntersect(line2)
                if(result > 0):
                    return True
        return False
    
    def closeShape(self):
        if(self.lines[0].start != self.lines[-1].end):
            self.lines.append(l.Line(self.lines[-1].getEnd(),
                                     self.lines[0].getStart()))
        self.shapeIsClosed = True
        
    def isShapeClosed(self):
        if(len(self.lines) < 2): return False
        if(self.lines[0].start == self.lines[-1].end):
            return True
        return False
                                     
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
        points = []
        for line in self.lines:
            result, point = line.segmentsIntersect(testLine)
            if(result == 1):
                points.append(point)
                intersections += 1
        if(intersections >= 8):
            print 'Total Intersections: ' + str(intersections)
            for p1 in points:
                print p1
        return (True if intersections % 2 == 1 else False)
            
    