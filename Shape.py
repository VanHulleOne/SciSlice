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
from LineGroup import LineGroup as LG
import constants as c
from functools import wraps
import numpy as np
import time
import Point as p
logger = c.logging.getLogger(__name__)
logger.setLevel(c.LOG_LEVEL)

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
                try:
                    raise Exception('Shape must have a continuous closed outline to use '
                                + func.__name__ + '()\n\t\t' + e.message)
                except Exception as _:
                    raise e
        return func(self, *args)
    return checker

class Shape(LG):    
    def __init__(self, shape=None):
        LG.__init__(self, shape)
        self.outlineFinished = False
    
    @finishedOutline
    def addInternalShape(self, inShape):
        if(not inShape.outlineFinished):
            print('********** Your internal shape was not a finished outline **********')
        if(not self.isInside(inShape.lines[0].start)):
            print('********** The internal shape is not inside the main shape. **********')
        if(self.doShapesIntersect(inShape)):
            print('********** Internal shape is not completely inside main shape. **********')
        
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
            
    def closeShape(self):
        if(self[0].start != self[-1].end):
            self.append(l.Line(self[-1].end, self[0].start))
            
    
    def finishOutline(self):
        """
        Finishes the outline with a companion methods or throws an exception if it fails.
        
        Calls the companion method self.__finishOutline() and if that method
        does not throw an eror it assigns the returned value to self.lines and
        sets the outline as finsihed.
        """  
        self.lines = self.__finishOutline()
        self.outlineFinished = True

    def __finishOutline(self, normList=None, finishedShape=None):
        """ A companion method for finishOutline.
        
        The method sorts the lines so the the end of one line is touching
        the start of the next line and orients the lines so that the left side
        of the line is inside the shape. The shapes are allowed to have internal
        features but every feature must be continuous and closed.
        
        Parameters
        ----------
        normList - A NumPy array containing the normalVectors for every point in self
        finsihedShape - A list of Lines which will define the new shape
        
        Return
        ------
        finishedShape
        """
        if normList is None:
            normList = np.array([point.normalVector for point in self.iterPoints()], dtype=np.float)     
        elif len(normList[(normList < np.inf)]) == 0:
            return
        if finishedShape is None:
            finishedShape = []

        """ Find the first index in normList that is not infinity. """
        firstLineIndex = np.where(normList[:,0] < np.inf)[0][0]//2
        
        """ firstLine is needed to know if the last line closes the shape. """
        firstLine = self[firstLineIndex]
        normList[firstLineIndex*2:firstLineIndex*2+2] = np.inf

        if not self.isInside(firstLine.getOffsetLine(c.EPSILON*2, c.INSIDE).getMidPoint()):
            """ Test if the inside (left) of the line is inside the part. If
            not flip the line. """
            firstLine = firstLine.fliped()
  
        testPoint = firstLine.end
        finishedShape.append(firstLine)
        
        while len(normList[(normList < np.inf)]) > 0:

            distances = np.linalg.norm(normList-testPoint.normalVector, None, 1)
            index = np.argmin(distances)
            nearestLine = self[index//2]
            
            if distances[index] > c.EPSILON:
                raise Exception('Shape has a gap of ' + str(distances[index]) +
                                ' at point ' + str(testPoint) + ', ' + 
                                str(p.Point(normList[index])))
            if index%2:
                """ If index is odd we are at the end of a line so the line needs to be flipped. """
                nearestLine = nearestLine.fliped()
            
            testPoint = nearestLine.end
            finishedShape.append(nearestLine)
            
            index //= 2
            """ Instead of deleting elements from the NumPy array we set the used
            vectors to infinity so they will not appear in the min. """
            normList[[index*2,index*2+1]] = np.inf
            
            if testPoint == firstLine.start:
                self.__finishOutline(normList, finishedShape)
                return finishedShape
        dist = firstLine.start - finishedShape[-1].end
        if dist < c.EPSILON:
            return finishedShape
        raise Exception('Shape not closed. There is a gap of {:0.5f} at point {}'.format(dist, testPoint))

    @finishedOutline                                
    def offset(self, distance, desiredSide):
        newShape = Shape()
        for subShape in self.subShape_gen():
            try:
                newShape.addLineGroup(self._offset(subShape, distance, desiredSide))
            except Exception as e:
                logger.info('One or more sub-shapes could not be offset. ' + str(e))
#        newShape.finishOutline()
        return newShape
    
    def _offset(self, subShape, distance, desiredSide):
        tempLines = []
        points = []
        prevLine = subShape[-1].getOffsetLine(distance, desiredSide)
        for currLine in (line.getOffsetLine(distance, desiredSide)
                                for line in subShape):
            _, point = prevLine.segmentsIntersect(currLine, c.ALLOW_PROJECTION)
            if prevLine.calcT(point) > 0:
                points.append(point)
            else:
                points.append(prevLine.end)
                points.append(currLine.start)
            prevLine = currLine
        tempLines.extend(l.Line(p1, p2) for p1, p2 in self.pairwise_gen(points))
        splitLines = []
        extraLines = []
        for iLine in iter(tempLines):
            pointList = [iLine.start, iLine.end]
            for jLine in iter(tempLines):
                if jLine != iLine:
                    interSecType, point = iLine.segmentsIntersect(jLine)
                    
                    if interSecType == 2.5 and jLine not in extraLines:
                        print('Overlap Lines - shape line 202')
                        extraLines.append(iLine)
#                    if interSecType > 2:
#                        colinearPoints = list(sorted(set([iLine.start, iLine.end,
#                                                     jLine.start, jLine.end])))
#                        extraLines = [l.Line(colinearPoints[i], colinearPoints[i+1]) for i in range(len(colinearPoints)-1)]                             
                                                     

                    if point is not None and interSecType > 0 and point not in pointList:
                        pointList.append(point)
            pointList = sorted(pointList, key=lambda x: x-iLine.start)

            splitLines.extend(l.Line(pointList[i], pointList[i+1]) for i in range(len(pointList)-1))

        tempShape = Shape(splitLines)
        shapeLines = []
        for line in splitLines:
            if(tempShape.isInside(line.getOffsetLine(2*c.EPSILON, c.INSIDE).getMidPoint())):
                shapeLines.append(line)

        offShape = Shape(shapeLines)
#        map(offShape.append, extraLines)
        if len(extraLines):
            for line in extraLines:
#                print('Line')
#                print(line)
                offShape.append(line)
#                print('shape Again')
#                for line2 in offShape:
#                    print(line2)
#        offShape.finishOutline()
#        map(offShape.append, extraLines)
        return offShape
              
    def pairwise_gen(self, l1):
        l1Iter = iter(l1)
        first = pre = next(l1Iter)
        for curr in l1Iter:
           yield pre, curr
           pre = curr
        yield pre, first            
    
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
    
    def isInside(self, point, ray=np.array([0.998, 0.067])):
        """
        This method determines if the point is inside
        or outside the shape. Returns the side of the shape the point is on.
        
        If a line is drawn from the point to outside of the shape the number
        of times that line intersects with the shape determines if the point was inside
        or outside. If the number of intersections is even then the point was outside
        of the shape. If the number of intersections is odd then the point is inside.
        
        Problems arise if the line passes through the endpoints of two lines so
        if that happens draw a new line and test again. This redraw is handled
        through recursion.
        
        The default ray is at an angle of about 3.6 degrees. A little testing
        showed this angle to be fairly unlikely to cause endpoint collisions.
        When a collision does occur we draw the new ray at the current angle plus
        90 degrees plus a random value between [0-1). The 90 degrees is to make
        the new ray perpendicular to the current one and hopefully less likely
        to hit another point. The random amount is to avoid hitting another endpoint
        which are usually at a regular interval.
        """
#        print('New isInside test')
#        print('Point: ', point)
        if(point[c.X] > self.maxX or point[c.X] < self.minX): return c.OUTSIDE
        if(point[c.Y] > self.maxY or point[c.Y] < self.minY): return c.OUTSIDE

        Q_Less_P = point[:2] - self.starts
        denom = 1.0*np.cross(self.vectors, ray)
        all_u = np.cross(Q_Less_P, self.vectors)/denom # the intersection ratio on ray
        all_t = np.cross(Q_Less_P, ray)/denom # The intersection ratio on self.lines 

#        print('all_u')
#        print(all_u)
#        print('all_t')
#        print(all_t)
        all_t = all_t[all_u > 0]

        endPoints = (np.abs(all_t) < c.EPSILON) | (np.abs(1-all_t) < c.EPSILON)
        if np.any(endPoints):
            time.sleep(0.5)
            oldAngle = np.arctan2(*ray[::-1])
            newAngle = oldAngle+(90+np.random.rand())/360.0*2*np.pi
            logger.info('Recursion made in isInside()\n\tcollision at angle: ' +
                            '{:0.1f} \n\tnext angle attempt: {:0.1f} \
                            \n\tPoint: {}'.format(
                            oldAngle*360/2.0/np.pi, newAngle*360/2/np.pi, point))
            newRay=np.array([np.cos(newAngle), np.sin(newAngle)])
            return  self.isInside(point, newRay)
            
        intersections = (0 < all_t) & (all_t < 1)
#        print('Intersections: ', intersections)
        return (c.INSIDE if np.sum(intersections) % 2 else c.OUTSIDE)
