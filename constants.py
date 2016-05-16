# -*- coding: utf-8 -*-
"""
Created on Mon May 16 10:44:25 2016

Constants used across modules.

@author: lvanhulle
"""

ARC_NUMPOINTS = 20
CW = -1 #Circle direction clock wise
CCW = 1 #circle direction counter clowise
X, Y, Z = 0, 1, 2
START = 0 #start of circle
END = 1 #end of circle
DIR = 2 #direction to travel
CENTER = 3 #center of circle
INSIDE = 1 #Point is inside shape
OUTSIDE = 0 #point is outside shape
ALLOW_PROJECTION = True
EPSILON = 10000 # The prcision level to use when doing numerical comparisons
OMIT_Z = True # When moving to a new point this chooses the Z level should not be used
INCLUDE_Z = False