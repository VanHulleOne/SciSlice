# -*- coding: utf-8 -*-
"""
Created on Wed Oct 28 14:09:55 2015

@author: lvanhulle
"""
import Line as l
import Point as p
from LineGroup import LineGroup as LG
from parameters import constants as c

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
        
        for line in inShape:
            self.append(line)
    
    def doShapesIntersect(self, inShape):
        for line in self.lines:
            for line2 in inShape.lines:
                result, point = line.segmentsIntersect(line2)
                if(result > 0):
                    return True
        return False
    
    def addLineGroup(self, inGroup):
        super(Shape, self).addLineGroup(inGroup)
        self.shapeIsClosed = self.isShapeClosed()
    
    def closeShape(self):
        if(self[0].start != self[-1].end):
            self.append(l.Line(self[-1].end, self[0].start))
        self.shapeIsClosed = True
        
    def isShapeClosed(self):
        if(len(self) <= 2): return False
        if(self[0].start == self[-1].end):
            return True
        return False
                                     
    def offset(self, distance, desiredSide):
        trimJoin = self.trimJoin_coro()
        next(trimJoin)
        for line in self:
            try1, try2 = line.getOffsetLines(distance)
            if self.isInside(try1.getMidPoint()) is desiredSide:
                trimJoin.send(try1)
            else:
                trimJoin.send(try2)
        return Shape(trimJoin.send(None))
       
    def trimJoin_coro(self):
        offsetLines = []
        moveEnd = yield
        moveStart = yield
        while not(moveStart is None):
            _, point = moveEnd.segmentsIntersect(moveStart, c.ALLOW_PROJECTION)
            moveEnd.end = point
            moveStart.start = point
            offsetLines.append(moveEnd)
            moveEnd = moveStart
            moveStart = yield
        _, point = moveEnd.segmentsIntersect(offsetLines[0], c.ALLOW_PROJECTION)
        moveEnd.end = point
        offsetLines.append(moveEnd)
        offsetLines[0].start = point
        yield offsetLines
    
    def isInside(self, point):
        """
        This method determines if the point is inside
        or outside the shape. Returns 1 if inside and 0 if outside.
        
        If a line is drawn from the point down to the outside of the part, the number
        of times that line intersects with the shape determines if the point was inside
        or outside. If the number of intersections is even then the point was outside
        of the shape. If the number of intersections is odd then the point is inside.
        """
        if(point.x > self.maxX or point.x < self.minX): return False
        if(point.y > self.maxY or point.y < self.minY): return False
        
        downLine = l.Line(point, p.Point(point.x, self.minY - 10, point.z))

        downSet = set([]) 
        for line in self:
            if(line.isOnLine(point)):
#                print 'Line: ' + str(line) + ' Point: ' + str(point)                
                return True
                
            result, intPoint = line.segmentsIntersect(downLine)
            #print 'Result: ' + str(result) + ' Point: ' + str(point)
            if(result == 1): downSet.add(intPoint)
#        print 'Len: ' + str(len(downSet)) + ' Point: ' + str(point)    
        return (True if len(downSet) % 2 == 1 else False)
