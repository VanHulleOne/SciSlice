# -*- coding: utf-8 -*-
"""
Created on Tue Oct 27 13:40:56 2015

Line stores a start and end points of a line. The module also provides many of
the important line checking fucntions such as hceking intersection and offsets.
Line start/end points are immutable but the extrusion rate and freezeExRate
can be changed.

@author: lvanhulle
"""
import point as p
import numpy as np
import constants as c
import time
logger = c.logging.getLogger(__name__)

class Line(object):
    def __init__(self, start, end, oldLine = None):
        """
        Takes in the start and end points of a line plus an optional "oldLine".
        oldLine is used when a new line is created from an exhisting line and
        the operator wants the new line to have the same extrusion properties
        as the exhisting line. This is used for all of the line transformations.
        """
        self.__start = start
        self.__end = end
        if(self.__start == self.__end):
            """
            If a zero length line is created that most likely means there is a
            logic problem somewhere in the program. This does not throw and error
            so that the output can still be examined to help diagnose the problem.
            """
#            raise Exception('Zero length line')
            logger.warning('A line was created with no length at: ' + 
                            str(self.start))
        """ The Point which is the upper left corner of the line's bounding box """
        self.__upperLeft = None
        """ The Point of the lower right corner of the bounding box. """
        self.__lowerRight = None
        self.__extrusionRate = 0
        self.freezeExRate = False
        if not(oldLine is None):
            self.__extrusionRate = oldLine.extrusionRate
            self.freezeExRate = oldLine.freezeExRate
        self.vector = np.array([self.end.x-self.start.x,
                                self.end.y-self.start.y])
                                
    
    @property
    def upperLeft(self):
        if self.__upperLeft is None:            
            tempList = [[self.start.x, self.end.x],
                         [self.start.y, self.end.y]]
            for row in tempList:
                row.sort()
            self.__upperLeft = p.Point(tempList[0][0], tempList[1][1])
            self.__lowerRight = p.Point(tempList[0][1], tempList[1][0])
        return self.__upperLeft
        
    @property
    def lowerRight(self):
        if self.__lowerRight is None:
            tempList = [[self.start.x, self.end.x],
                     [self.start.y, self.end.y]]
            for row in tempList:
                row.sort()
            self.__upperLeft = p.Point(tempList[0][0], tempList[1][1])
            self.__lowerRight = p.Point(tempList[0][1], tempList[1][0])
        return self.__lowerRight
    
    @property
    def start(self):
        return self.__start
        
    @property
    def end(self):
        return self.__end
  
    @property
    def length(self):
        return self.start - self.end
        
    @property
    def extrusionRate(self):
        return self.__extrusionRate
        
    @extrusionRate.setter
    def extrusionRate(self, value):
        """
        If the extrusion rate is not frozen then change the extrusion rate
        """
        if (not self.freezeExRate):
            self.__extrusionRate = value
            
    def __iter__(self):
        yield self.start
        yield self.end
    
    @property
    def angle(self):
        angle = np.arctan2(self.end.y-self.start.y, self.end.x-self.start.x)
        return angle if angle >= 0 else angle + 2*np.pi

    def calcT(self, point):
        """ Returns a constant representing point's location along self.
        
        The point is assumed to be on self. T is the constant along self
        where point is located with start being 0, end being 1, <0 is behind
        the line and >0 is past the line segment
        
        Parameters
        ----------
        point - The test point.
        
        Return
        ------
        A constant representing point's location along self.
        """
        index = np.argmax(np.abs(self.start.normalVector[:2]-self.end.normalVector[:2]))
        return (point[index] - self.start[index])/(self.end[index]-self.start[index])
        
    def areParallel(self, line):
        """
        returns True if the two lines are parallel
        
        This method tests if two lines are parallel by finding the angle
        between the perpendicular vector of the first line and the second line.
        If the dot product between perpVect and the vect of line2 is zero then
        line1 and line2 are parallel. Farin and Hansford recommend checking within
        a physically meaningful tolerance so equation 3.14 from pg 50 of
        Farin-Hansford Geometry Toolbox is used to compute the cosine of the angle
        and compare that to our ANGLE_EPS. If cosTheda < ANGLE_EPS then the lines
        are parallel.
        
        Parameters
        ----------
        line1 - the first line
        line2 - the second line
        
        Return
        ------
        True if lines are parallel within ANGLE_EPS else False
        """
        # A vector perpendicular to line1
        perpVect = np.array([-self.vector[c.Y], self.vector[c.X]])
        # Farin-Hansford eq 3.14
        cosTheda = (np.dot(perpVect, line.vector)/
                    (np.linalg.norm(perpVect)*np.linalg.norm(line.vector)))
        # if cosTheda is < c.EPSILON then the lines are parallel and we return True
        return abs(cosTheda) < c.EPSILON   

    def segmentsIntersect(self, other, allowProjInt = False):
        """
        Probably the most important method in the Line module. This tests to
        see if two line segments intersect and returns a tuple containing
        a number code for the type of intersection and the Point of intersection
        or projected point of intersection if there is one and it was allowed.
        
        The calculation of t and u is stable but testing to make sure that the
        point in on the line is the difficult part of this method. A better
        solution should probably be found.
        
        -3 = bounding boxes do not intersect
        3 = lines were colinear and shared an end point
        3 = lines were colinear and did not share an end point
        -1 = Projected intersection of non-colinear lines
        1 = intersection of non-colinear lines
        """
        
        """
        If we are not allowing projected intersection and the bounding boxes
        do not intersect then return -3, None.
        """
        if(not(allowProjInt) and not(self.doBoundingBoxesIntersect(other))): return -3, None #return if bounding boxes do not intersect
        """ A special case for colinear lines. """        
        if(self.areColinear(other)):
            """
            First place all four endpoint into a set. This will elliminate shared
            end points. Next, convert the set back into a list so it can
            finally be sorted.
            """
            pointList = sorted(list(set([self.start, self.end, other.start, other.end])), key=self.calcT)            
            if len(pointList) == 3:
                """
                if there are only three points in the list then return 2, the
                middle point in the list since it is the shared point of the
                two lines.
                """
                return 2, pointList[1] #if they are colinear and two ends have the same point return that point
            elif len(pointList) == 2:
                """ If the two lines have the same endpoints. """
                return 2.5, self.getMidPoint()
            else:
                """
                If the length was not three then we know it is length 4 in which case
                we turn the two middle points into a line and return 3, the line's
                midpoint.
                """
                tempLine = Line(pointList[1], pointList[2])
                return 3, tempLine.getMidPoint() #If they are colinear return half way inbetween middle two points
        """
        To calculate the intersection of two points we put the lines into the
        form P+tr and Q+us where P and Q are the starting points of the lines
        r and s are vectors form the starting point to the end point, and
        t and u are scalars. Set the two equations equal to each other and 
        then solve for t and u. If t and u are in the range [0-1] then the
        intersection point lines on the lines, else it is a projected point.
        """
        r = np.subtract(self.end.get2DPoint(), self.start.get2DPoint())
        s = np.subtract(other.end.get2DPoint(), other.start.get2DPoint())
        Q_Less_P = np.subtract(other.start.get2DPoint(), self.start.get2DPoint())
        denom = np.cross(r, s)*1.0
        t = np.cross(Q_Less_P, s)/denom
        u = np.cross(Q_Less_P, r)/denom 
        point = p.Point(self.start.x + r[c.X]*t, self.start.y+r[c.Y]*t)         
        #If t or u are not in the range 0-1 then the intersection is projected
        if(t > 1 or u > 1 or t < 0 or u < 0):
            """
            Due to floating point problems sometimes if t or u is outside the 0-1
            range we end up inside this if statement but are actually at the end
            of one of the lines. I can't figure out how to properly add in a tolerance
            so we are taking the four end points putting them into a list,
            then comparing them to the calculated point. The Point module is
            properly handling tolerances so if the point == any of the end
            points then we should not return a projected point.
            """
            if not any(point == lineEnd for lineEnd in (self.start, self.end,
                                                        other.start, other.end)):
                return -1, point #return for projected intersection of non-colinear lines
        return 1, point #lines intersect at given point

    def isOnLine(self, point):
        """ Tests to see if a point is on the line. """
        if((point < self.start and point < self.end) or (
            point > self.start and point > self.end)):
            return False #point is not between the start and end of self
        
        if(self.getArea(self.start, self.end, point) > c.EPSILON):
            return False #points are not co-linear
        
        return True
    
    def getArea(self, p1, p2, p3):
        """
        Uses the determinant of a matrix containing the three to find the area
        of the triangle formed by the three points.
        """
        matrix = [p1.normalVector, p2.normalVector, p3.normalVector, [1,1,1,1]]
        matrix = np.rot90(matrix)
        return abs(np.linalg.det(matrix))/2.0

    def areColinear(self, other):
        """returns True if the two lines are colinear
        
        This method tests if two lines are colinear by finding the angle
        between the perpendicular vector of self and lines created from self to
        both ends of other.
        If the dot product between perpVect and both of the new vectors is zero then
        they are colinear. Farin and Hansford recommend checking within
        a physically meaningful tolerance so equation 3.14 from pg 50 of
        Farin-Hansford Geometry Toolbox is used to compute the cosine of the angle
        and compare that to our ANGLE_EPS. If cosTheda < ANGLE_EPS then the lines
        """
        perpVect = np.array([-self.vector[c.Y], self.vector[c.X]])
        vect1 = other.end[:2]-self.start[:2]
        vect2 = other.start[:2]-self.start[:2]
        cosTheda1 = (np.dot(perpVect, vect1)/
                    (np.linalg.norm(perpVect)*np.linalg.norm(vect1)))
        if abs(cosTheda1) > 0.0001:
            return False
        cosTheda2 = (np.dot(perpVect, vect2)/
                    (np.linalg.norm(perpVect)*np.linalg.norm(vect2)))
        return not(abs(cosTheda2) > 0.0001)            
    
    def doBoundingBoxesIntersect(self, other):
        """
        The bounding box of the line is represented be the upper left and
        lower right corners of the smallest box which contains the line. If
        the bounding boxes for two lines do not intersect then we know that the
        two lines do not intersect and we can save a bunch of work.
        """
        if(self.upperLeft.x <= other.lowerRight.x and
            self.lowerRight.x >= other.upperLeft.x and
            self.upperLeft.y >= other.lowerRight.y and
            self.lowerRight.y <= other.upperLeft.y):
                return True
        return False 
        
    def translate(self, shiftX, shiftY, shiftZ=0):
        newStart = self.start.translate(shiftX, shiftY, shiftZ)
        newEnd = self.end.translate(shiftX, shiftY, shiftZ)
        return Line(newStart, newEnd, self)
        
    def mirror(self, axis):
        newStart = self.start.mirror(axis)
        newEnd = self.end.mirror(axis)
        return Line(newStart, newEnd, self)
    
    def rotate(self, angle, point):
        if(point is None): point = p.Point(0,0)
        newStart = self.start.rotate(angle, point)
        newEnd = self.end.rotate(angle, point)
        return Line(newStart, newEnd, self)

    def fliped(self):
        """ returns a line with the start and end points flipped form self. """
        return Line(self.end, self.start, self)
    
    def getOffsetLine(self, distance, side=c.INSIDE):
        """ Calculates and returns the two lines on either side of self offset distance."""
        StartA = np.array([self.start.x, self.start.y])
        EndA = np.array([self.end.x, self.end.y])
        r = StartA - EndA #The slope vector of self
        rn = np.array([-r[c.Y], r[c.X]]) #flip x and y and inverse y to get the normal vector of the slope
        rn = rn/np.linalg.norm(rn)*distance #normalize by dividing by its magnitude and multipy by distance to get the correct length
        
        if side == c.INSIDE:
            return self.translate(-rn[c.X], -rn[c.Y]) #the "minus" side line is the left side which is inside.
        
        return self.translate(rn[c.X], rn[c.Y]) #the "Plus" side of the line is the right side which is outside.
        
    def sideOfLine(self, point):
        dist = self.pointToLineDist(point)
        if abs(dist) < c.EPSILON:
            return 0
        return  c.LEFT if dist < 0 else c.RIGHT
    
    def pointToLineDist(self, point):
        perpVect = np.array([self.vector[c.Y], -self.vector[c.X]])
        difPoint = point.get2DPoint()-self.start.get2DPoint()
        return np.dot(perpVect, difPoint)/np.linalg.norm(perpVect)
        
    
    def getMidPoint(self):
        """ Calculate and return the midpoint of self. """
        return p.Point((self.start.normalVector + self.end.normalVector)/2.0)
    
    def __lt__(self, other):
        """
        Sort the points of the lines first and then compare their lowest Points.
        If those points are equal then compare the other points.
        
        Please also read __eq__ for more about line comparisons.
        """
        selfList = sorted(list([self.start, self.end]))
        otherList = sorted(list([other.start, other.end]))
        if(selfList[0] < otherList[0]):
            return True
        if(selfList[0] > otherList[0]):
            return False
        return (selfList[1] < otherList[1])
        
    def __eq__(self, other):
        """
        If the start point and end point of the two lines are the same then
        the lines are equal. Note that this means that self != flipped(self).
        I don't know if that is necessary but that hasn't caused me any problems...
        yet.
        """
        return (self.start == other.start and self.end == other.end)      
    
    def __repr__(self):
        """ The string of the line. """
        return str(self.start) + '    \t' + str(self.end)
    
    def CSVstr(self):
        """ A comma seperated form for the gui. """
        return self.start.CSVstr() + ',' + self.end.CSVstr()
    
    def printBoudningBox(self):
        print('Bounding Box for: ' + str(self))
        print(str(self.upperLeft) + ', ' + str(self.lowerRight))