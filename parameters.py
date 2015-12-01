# -*- coding: utf-8 -*-
"""
Created on Thu Nov 19 19:52:29 2015

@author: lvanhulle
"""
import math
#import Shape as s
#import arc as a
#import Point as p
#import premadeShapes as ps

"""
Printing Parameters.
"""
extrusionRate = 0.0212 #mm of filament/mm of travel
pathWidth = 0.5 #mm distance between centerline of paths
printSpeed = 2000 #mm/min head travel speed

"""
Part Parameters
"""
#mainShape = ps.wideDogBone
layerHeight = 0.3 #mm height per layer
numLayers = 1 #number of layers to make
infillAngleDegrees = 90 #degrees infill angle 90 is in Y direction 0 is in X direction

"""
File Parameters
"""
outputFileName = 'DB_10-23_Test.gcode' #the name of the file you want output. git will ignore all .gcode unless they start with SAVE
start_Gcode_FileName = 'Start_Gcode_Taz5.txt' #the file name for the starting gcode
end_Gcode_FileName = 'End_Gcode_Taz5.txt' #The file name for the end gcode
outputSubDirectory = 'Gcode'
startEndSubDirectory = 'Start_End_Gcode'

"""
Misc Parameters
"""
maxFeedStep = 5.0 #not implemented yet
slopeOverX = 0.0 #not yet implemented how much you want it to move over in X per level
slopeOverY = 0 #not implemented yet how much you want it to move over in Y per level
backgroundAngle = (infillAngleDegrees/360.0*2*math.pi) #angle of the paths in the layer 0 = X direction, PI/2 = Y direction
solidityRatio = None #get calculation from Karsten

"""
Standard printing settings
"""
OMIT_Z = True
INCLUDE_Z = False
RAPID = 8000. #mm/min
TRAVERSE_RETRACT = 0.5 #mm to retract when traversing longer distances
MAX_EXTRUDE_SPEED = 100 #mm/min max speed to move filament
Z_CLEARANCE = 10.0 #mm to move Z up
APPROACH_FR = 2000 #mm/min aproach feedrate

"""
Constants
"""
class constants:
    numPoints = 20
    CW = -1 #Circle direction clock wise
    CCW = 1 #circle direction counter clowise
    X, Y, Z = 0, 1, 2
    START = 0 #start of circle
    END = 1 #end of circle
    DIR = 2 #direction to travel
    CENTER = 3 #center of circle
    INSIDE = 1 #Point is inside shape
    OUTSIDE = 0 #point is outside shape
    
#class premadeShapes:
#    import constants as c
#    
#    dogBone = s.Shape(None)
#    dogBone.addLinesFromCoordinateList([[82.5, 0], [82.5, 9.5], [49.642, 9.5]])
#    arc = a.Arc(p.Point(49.642, 9.5), p.Point(28.5, 6.5), c.CW, p.Point(28.5, 82.5), 20)
#    dogBone.addLineGroup(arc)
#    dogBone.addLinesFromCoordinateList([[28.5, 6.5], [0, 6.5]])
#    dogBone.addLineGroup(dogBone.mirror(c.Y))
#    dogBone.addLineGroup(dogBone.mirror(c.X))
#    dogBone.translate(82.5, 9.5)
#    
#    halfWidth = 5.0    
#    wideDogBone = s.Shape(None)
#    wideDogBone.addLinesFromCoordinateList([[82.5, 0], [82.5, 9.5 + halfWidth], [49.642, 9.5 + halfWidth]])
#    wideArc = a.Arc(p.Point(49.642, 9.5 + halfWidth), p.Point(28.5, 6.5 + halfWidth), c.CW, p.Point(28.5, 82.5 + halfWidth), 20)
#    wideDogBone.addLineGroup(arc)
#    wideDogBone.addLinesFromCoordinateList([[28.5, 6.5 + halfWidth], [0, 6.5 + halfWidth]])
#    wideDogBone.addLineGroup(dogBone.mirror(c.Y))
#    wideDogBone.addLineGroup(dogBone.mirror(c.X))
#    wideDogBone.translate(82.5, 9.5 + halfWidth)
#    
    
    
    