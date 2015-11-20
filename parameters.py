# -*- coding: utf-8 -*-
"""
Created on Thu Nov 19 19:52:29 2015

@author: lvanhulle
"""

extrusionRate = 0.0212 #mm of filament/mm of travel
printSpeed = 2000 #mm/min head travel speed
pathWidth = 0.500 #mm distance between centerline of paths
layerHeight = 0.3 #mm height per layer
numLayers = 3 #number of layers to make

OMIT_Z = True
INCLUDE_Z = False
RAPID = 8000. #mm/min
TRAVERSE_RETRACT = 0.5 #mm to retract when traversing longer distances
MAX_EXTRUDE_SPEED = 100 #mm/min max speed to move filament
Z_CLEARANCE = 10.0 #mm to move Z up
APPROACH_FR = 2000 #mm/min aproach feedrate