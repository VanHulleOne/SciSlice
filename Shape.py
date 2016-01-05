# -*- coding: utf-8 -*-
"""
Created on Wed Oct 28 14:09:55 2015

@author: lvanhulle
"""
import Line as l
import Point as p
from LineGroup import LineGroup as LG
from parameters import constants as c
from functools import wraps

def finishedOutline(func):
    @wraps(func)
    def checker(self, *args):            
        if self.outlineFinished:
            return func(self, *args)
        else:
            try:
                self.outlineFinished = self.finishOutline()
            except Exception as e:
                raise Exception('Shape must have a continuous closed outline to use '
                            + func.__name__ + '()\n\t\t' + e.message)
            else:
                return func(self, *args)
    return checker

class Shape(LG):    
    def __init__(self, shape):
        LG.__init__(self, shape)
        self.outlineFinished = False
        try:
            pass
#            self.outlineFinished = self.__finishOutline()
        except:
            pass
    
    @finishedOutline
    def addInternalShape(self, inShape):
        if(not inShape.outlineFinished):
            print '********** Your internal shape was not a finished outline **********'
        if(not self.isInside(inShape.lines[0].start)):
            print '********** The internal shape is not inside the main shape. **********'
        if(self.doShapesIntersect(inShape)):
            print '********** Internal shape is not completely inside main shape. **********'
        
        for line in inShape:
            self.append(line)
    
    @finishedOutline
    def doShapesIntersect(self, inShape):
        for line in self.lines:
            for line2 in inShape.lines:
                result, point = line.segmentsIntersect(line2)
                if(result > 0):
                    return True
        return False
   
    def addLineGroup(self, inGroup):
        super(Shape, self).addLineGroup(inGroup)
        self.outlineFinished = False
    
    def finishOutline(self):
        if(len(self) < 3):
            raise Exception('Cannot finish outline. Min shape length == 3')
        tempLines = [self.pop(0)]
        while len(self) > 0:
            if(tempLines[-1].end.distance(self[0].start) == 0):
                tempLines.append(self.pop(0))
            else:
                nearestDist = tempLines[-1].end.distance(self[0].start)
                for i in xrange(len(self)):
                    dist = tempLines[-1].end.distance(self[i].start)
                    if dist == 0:
                        nearestDist = dist                        
                        tempLines.append(self.pop(i))
                        break
                    elif dist < nearestDist:
                        nearestDist = dist
                    dist = tempLines[-1].end.distance(self[0].end)
                    if dist == 0:
                        nearestDist = dist 
                        self[i].flip()
                        tempLines.append(self.pop(i))
                        break
                    elif dist < nearestDist:
                        nearestDist = dist
                if nearestDist != 0:
                    raise Exception('Outline has a gap of ' + str(nearestDist))
        self.lines = tempLines
        return True 
    
    def closeShape(self):
        if(self[0].start != self[-1].end):
            self.append(l.Line(self[-1].end, self[0].start))

    @finishedOutline                                
    def offset(self, distance, desiredSide):
        trimJoin = self.trimJoin_Coro()
        next(trimJoin)
        for line in self:
            try1, try2 = line.getOffsetLines(distance)
            if self.isInside(try1.getMidPoint()) == desiredSide:
                trimJoin.send(try1)
            else:
                trimJoin.send(try2)
        return Shape(trimJoin.send(None))
    
    def trimJoin_Coro(self):
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
    
#    @finishedOutline    
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

