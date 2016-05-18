# -*- coding: utf-8 -*-
"""
Created on Wed Oct 28 14:09:55 2015

Shape should probably have been called outline but I have not yet bothered to
rename it. It is a subclass of LineGroup with extra methods for checking if it
is a closed polygon. The shape can be manifold (have internal holes) as long
as they are fully enclosed inside of the boundry.

@author: lvanhulle
"""
import Line as l
import Point as p
from LineGroup import LineGroup as LG
import constants as c
from functools import wraps

def finishedOutline(func):
    """
    This method is used as a decorator to make sure that the Shape is valid
    before certian functions are used. See finishOutline() for what makes a 
    valid shape.
    """
    @wraps(func)
    def checker(self, *args):            
        if not self.outlineFinished:
            try:
                self.finishOutline()
            except Exception as e:
                raise Exception('Shape must have a continuous closed outline to use '
                            + func.__name__ + '()\n\t\t' + e.message)
        return func(self, *args)
    return checker

class Shape(LG):    
    def __init__(self, shape):
        LG.__init__(self, shape)
        self.outlineFinished = False
    
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
    
    @finishedOutline    
    def subShape_gen(self):
        tempLines = []
        for line in self:
            tempLines.append(line)
            if tempLines[0].start == tempLines[-1].end:
                yield tempLines
                tempLines = []
        if len(tempLines) != 0:
            yield tempLines
            
    
    def finishOutline(self):
        """
        Checks to see if the Shape is valid and can be finished. For a shape to
        be valid it must be continuous and closed. If a shape has subshapes those
        must also be continuous and closed. The lines must be in order as well.
        
        First this method uses sortNearest_gen() to organize all of its lines.
        Then it uses subShape_gen() to get the sub-shapes if there are any.
        If the start of the first point does not equal the end of the last point
        the shape is not closed.
        Next each line is tested to see if the end of one line is the same as
        the start of the next line. If not the gap distance is calculated and
        sent in the Exception message.
        """
        self.lines = list(self.sortNearest_gen())
        self.outlineFinished = True #to run subShape_gen this must be set to True since it uses the @finishedOutline decorator
        for subShape in self.subShape_gen():
            if subShape[0].start != subShape[-1].end:
                dist = subShape[0].start - subShape[-1].end
                raise Exception('Shape not closed. End gap of ' + str(dist))            
            for i in xrange(len(subShape)-1):                     
                if subShape[i].end != subShape[i+1].start:
                    dist = subShape[i].end - subShape[i+1].start
                    raise Exception('Outline has a gap of ' + str(dist))

    
    def closeShape(self):
        if(self[0].start != self[-1].end):
            self.append(l.Line(self[-1].end, self[0].start))

    @finishedOutline                                
    def offset(self, distance, desiredSide):
        tempLines = []
        for subShape in self.subShape_gen():
            trimJoin = self.trimJoin_Coro()
            next(trimJoin)
            for line in subShape:
                # TODO: Reorganize shape into a CCW direction so we know that
                # inside/outside is left/right of the line saving the extra
                # try and check.
                try1, try2 = line.getOffsetLines(distance)
                if self.isInside(try1.getMidPoint()) == desiredSide:
                    trimJoin.send(try1)
                else:
                    trimJoin.send(try2)
            tempLines.extend(trimJoin.send(None))
        return Shape(tempLines)
    
    def trimJoin_Coro(self):
        """ Yields a list of lines that have their ends properly trimmed/joined
        after an offset.
        
        When the lines are offset their endpoints are just moved away the offset
        distance. If you offset a circle to the inside this would mean that
        all of the lines would overlap. If the circle was offset to the outside
        none of the lines would be touching. This function trims the overlapping
        ends and extends/joins the non touching ends.
        
        Yields
        ------
        in - Lines
        out - one big List of lines at the end since in Python 2.7 a coroutine
        can't return a value.
        """
        offsetLines = []
        moveEnd = yield
        moveStart = yield
        while not(moveStart is None):
            _, point = moveEnd.segmentsIntersect(moveStart, c.ALLOW_PROJECTION)
            moveEnd = l.Line(moveEnd.start, point, moveEnd)
            moveStart = l.Line(point, moveStart.end, moveStart)
            offsetLines.append(moveEnd)
            moveEnd = moveStart
            moveStart = yield
        _, point = moveEnd.segmentsIntersect(offsetLines[0], c.ALLOW_PROJECTION)
        moveEnd = l.Line(moveEnd.start, point, moveEnd)
        offsetLines.append(moveEnd)
        offsetLines[0] = l.Line(point, offsetLines[0].end, offsetLines[0])
        yield offsetLines
    
    @finishedOutline    
    def isInside(self, point):
        """
        This method determines if the point is inside
        or outside the shape. Returns the side of the shape the point in on.
        
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
                return True
                
            result, intPoint = line.segmentsIntersect(downLine)
            if(result == 1): downSet.add(intPoint)         

        return (c.INSIDE if len(downSet) % 2 == 1 else c.OUTSIDE)
