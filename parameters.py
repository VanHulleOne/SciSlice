# -*- coding: utf-8 -*-
"""
Created on Thu Nov 19 19:52:29 2015

@author: lvanhulle
"""
import math
import numpy
from collections import namedtuple

"""
Printing Parameters.
"""
solidityRatio = [1.09]#12]#, 0.1, 0.05] solidityRatio = PathArea/beadArea
pathWidth = 0.5 #mm distance between centerline of paths
printSpeed = [2000] #mm/min head travel speed
shiftX = [10, 50, 70]
shiftY = [10, 35, 60]
firstLayerShiftZ = 0 #correct for bed leveling

"""
Part Parameters
"""
#mainShape = ps.wideDogBone
layerHeight = [0.4] #mm height per layer
numLayers = [4] #number of layers to make
infillAngleDegrees = [0, -45, 90, 45, 45, 90, -45, 0] #degrees infill angle 90 is in Y direction 0 is in X direction
numShells = 1 # the number of shells max is 13

"""
Layer Parameters Only parameters that don't require the layer to be
re-organized are allowed
"""
layerShiftX = [0]
layerShiftY = [0]
flipLayer = [0]


"""
File Parameters
"""
outputFileName = 'ZigZag.gcode' #the name of the file you want output. git will ignore all .gcode unless they start with SAVE
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
filamentDiameter = 3.0 #mm dia of incoming filament
filamentArea = math.pi*filamentDiameter**2/4.0
nozzleDiameter = 0.5 #mm


def zipVariables_gen(inputLists, namedTuple = None, repeat=False):
    if namedTuple is None:
        namedTuple = namedtuple('n', ('n_'+str(i) for i in xrange(len(inputLists))))
    variableGenerators = [infinit_gen(sublist) for sublist in inputLists]
        
    while 1:
        for _ in max(inputLists, key=len):
            yield namedTuple(*(next(varGen) for varGen in variableGenerators))
        if not repeat:
            break
    
def infinit_gen(variableList):
    while 1:
        for var in variableList: 
            yield var

LayerParams = namedtuple('LayerParams', ['layerShiftX', 'layerShiftY', 'flipLayer'])            
layerParameters = (layerShiftX, layerShiftY, flipLayer)

PartParams = namedtuple('PartParams', ['solidityRatio', 'printSpeed',
                                                   'shiftX', 'shiftY', 'layerHeight',
                                                   'numLayers'])
everyPartsParameters = zipVariables_gen((
                          solidityRatio, printSpeed, shiftX, shiftY,
                          layerHeight, numLayers), namedTuple = PartParams)
                                                   

"""
Standard printing settings
"""
OMIT_Z = True
INCLUDE_Z = False
RAPID = 4000 #mm/min
TRAVERSE_RETRACT = 0.5 #mm to retract when traversing longer distances
MAX_EXTRUDE_SPEED = 100 #mm/min max speed to move filament
Z_CLEARANCE = 10.0 #mm to move Z up
APPROACH_FR = 2000 #mm/min aproach feedrate

"""
Constants
"""
class constants:
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
    SOLIDITY_RATIO = 0
    PRINT_SPEED = 1
    SHIFT_X = 2
    SHIFT_Y = 3
    LAYER_HEIGHT = 4
    NUM_LAYERS = 5
    LAYERSHIFT_X = 0
    LAYERSHIFT_Y = 1
    FLIP_LAYER = 2
