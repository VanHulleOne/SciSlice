# -*- coding: utf-8 -*-
"""
Created on Mon May 16 10:44:25 2016

Constants used across modules.

@author: lvanhulle
"""
import logging
import importlib

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
EPSILON = 1.0/10000 # The precision level to use when doing numerical comparisons
OMIT_Z = True # When moving to a new point this chooses the Z level should not be used
INCLUDE_Z = False
USED = True
NOT_USED = False
LEFT, ON_EDGE, RIGHT = -1,0,1
""" Used in InFill """
PARTIAL_ROW = 0
FULL_ROW = 1
FULL_FIELD = 2
CENTERED_FIELD = 3
TRIMMED_FIELD = 4 

GCODE = 0
ROBOTCODE = 1
STL_FLAG = 'stl_file'
THE_LABEL = 'the_label'
MODEL = 'model'

BED_TEMP_FLAG = '#BED_TEMP'
EXTRUDER_TEMP_FLAG = '#EXTRUDER_TEMP'

LOG_LEVEL = logging.WARN # logging.INFO
importlib.reload(logging)
logging.basicConfig(format='\n\nLog Message\n-----------\nModule: %(name)s\n' + 
                    'Log Level: %(levelname)s\nMsg: %(message)s', level=LOG_LEVEL)