# -*- coding: utf-8 -*-
"""
Created on Thu Nov 19 19:52:29 2015

@author: lvanhulle
"""
import math
from collections import namedtuple
import constants as c

"""
Part Parameters
"""
solidityRatio = [1.09]#12]#, 0.1, 0.05] solidityRatio = PathArea/beadArea
printSpeed = [2000] #mm/min head travel speed
shiftX = [10, 50, 70]
shiftY = [10, 35, 60]
firstLayerShiftZ = 0 #correct for bed leveling
numLayers = [8] #number of layers to make
trimAdjust = 1.0/c.EPSILON


"""
Layer Parameters
"""
infillAngleDegrees = [0, -45, 90, 45, 45, 90, -45, 0] #degrees infill angle 90 is in Y direction 0 is in X direction
pathWidth = [0.5] #mm distance between centerline of paths
layerHeight = [0.4] #mm height per layer
infillShiftX = [0]
infillShiftY = [0.25,0,0,0,0,0, 0, 0.25]
#flipLayer = [0] No longer implimented
numShells = [13,1,1,0,0,1,1,13] # the number of shells max is 13 if 0.4999 path width is used

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

LayerParams = namedtuple('LayerParams', ['infillShiftX', 'infillShiftY',
                                         'infillAngle', 'numShells', 'layerHeight',
                                         'pathWidth'])            
layerParameters = (infillShiftX, infillShiftY, infillAngleDegrees, numShells,
                   layerHeight, pathWidth)

PartParams = namedtuple('PartParams', ['solidityRatio', 'printSpeed',
                                                   'shiftX', 'shiftY',
                                                   'numLayers'])
everyPartsParameters = zipVariables_gen((
                          solidityRatio, printSpeed, shiftX, shiftY,
                          numLayers), namedTuple = PartParams)
                                                   

"""
Standard printing settings
"""
OMIT_Z = True
INCLUDE_Z = False
RAPID = 4000 #mm/min
TRAVERSE_RETRACT = 0.5 #mm of filament to retract when traversing longer distances
MAX_FEED_TRAVERSE = 10 # max mm to move without lifting the head
MAX_EXTRUDE_SPEED = 100 #mm/min max speed to move filament
Z_CLEARANCE = 10.0 #mm to move Z up
APPROACH_FR = 1500 #mm/min aproach feedrate
