# -*- coding: utf-8 -*-
"""
Created on Tue Oct 27 13:13:34 2015

The Point module stores the X, Y, Z of a point and performs basic Point opeartions.
All Points are immutable so that they can be hashed and to prevent deep/shallow
copy problems.

@author: lvanhulle
"""
import numpy
import constants as c
import matrixTrans as mt


class Point(object):
    
    NUM_DEC = 3
    printFormat = 'X{:.%df} Y{:.%df} Z{:.%df}' % tuple([NUM_DEC]*3)
    
    """
    To prevent floating point problems the coordinates of a point are stored
    as integers. The input number is multiplied by COMPARE_PRECISION and
    then converted to an int.
    """        
    COMPARE_PRECISION = c.EPSILON
    
    """
    Each Point stores an X, Y, Z coordinate. All points must have at least
    an X and a Y with 0 being the defualt value of Z. You can intialize a point
    in two ways, one is with the individual axes seperated Point(1, 2, 3) or
    with just X as an interable or X,Y,X as in Point([X, Y, Z]).
    
    The normalVector is [X, Y, Z, 1] and is in that form to make matrix
    transformations possible.
    """
    def __init__(self, x, y=None, z=0):
        """ Test to see if the first argument is iterable. """
        try:
            len(x)
        except:
            """
            If it was not iterable then check to make sure a Y value was used
            and initialize the NumPy Array.
            """
            if y is None:
                raise Exception('You did not initialize a Point correctly')            
            self.__normalVector = numpy.array([x, y, z, 1])            
           
        else:
            """ If it was iterable create the array """ 
            self.__normalVector = numpy.array([x[c.X], x[c.Y], x[c.Z], 1])
       
        """
        This is where the rounding problem is worked around. Take each point
        in the normal vector, multiply by COMPARE_PRECISION, then round it,
        then convert it to an int.
        """
        self.__key = tuple(int(round(i*self.COMPARE_PRECISION))
                            for i in self.normalVector[:3])
        
    @property
    def x(self):
        return self.__normalVector[c.X]
        
    @property
    def y(self):
        return self.__normalVector[c.Y]
    
    @property
    def z(self):
        return self.__normalVector[c.Z]
        
    @property
    def normalVector(self):
        return numpy.array(self.__normalVector)
    
    """ iterate through the coordinates. I don't think this is used anywhere. """
    def __iter__(self):
        return(i for i in self.__normalVector[:3])
    
    """ Sometimes we just want the X and Y of a point """
    def get2DPoint(self):
        return self.__normalVector[:2]
    
    """ mirror about an axis, mirror about an arbitrary line not yet enabled """
    def mirror(self, axis):
        return self.transform(mt.mirrorMatrix(axis))
    
    """ rotate self about the input point by some angle """ 
    def rotate(self, angle, point=None):
        return self.transform(mt.rotateMatrix(angle, point))
    
    """ translate self by the input amounts """
    def translate(self, shiftX, shiftY, shiftZ=0):
        return self.transform(mt.translateMatrix(shiftX, shiftY, shiftZ))
    
    """
    All transformations, mirror, rotate, translate, simply create their appropriate
    transformation matricies and pass them to transform which performs
    the necessary dot product on the transMatrix and the normalVector and return
    the new Point.
    """    
    def transform(self, transMatrix):
        nv = numpy.dot(transMatrix, self.normalVector)
        return Point(nv)
        
    def __getitem__(self, index):
        return self.normalVector[index]
    
    """ Subtracting two points gives the distance between the points. """
    def __sub__(self, other):
        return numpy.linalg.norm(self.normalVector - other.normalVector)
        
    """ Makes x and Y the opposite sign. Can't remember why. """
    def __neg__(self):
        return Point(-self.x, -self.y, self.z)
    
    """
    Sometimes you just need the squaredDistance between two points. This is
    about twice as fast as subtraction.
    """
    def squareDistance(self, other):
        return ((self.x - other.x)**2 + (self.y - other.y)**2)
    
    """ All comparisons are element wise comparisons in the order X, Y, Z """
    def __lt__(self, other):
        return self.__key < other.__key
        
    def __gt__(self, other):
        return self.__key > other.__key

    def __eq__(self, other):
        return self.__key == other.__key
        
    def __ne__(self, other):
        return self.__key != other.__key
    
    """ Create the hash of the Point's key """    
    def __hash__(self):
        return hash(self.__key)
    """ Creates a string of just X and Y comma seperatred for gui output """
    def CSVstr(self):
        return '{:.4f},{:.4f}'.format(self.x, self.y)
    
    """ String for printing """
    def __str__(self):
        return self.printFormat.format(*self.__normalVector[:3])
        
    def __repr__(self):
        return 'Point(%f, %f, %f)'%tuple(self.__normalVector[:3])
    