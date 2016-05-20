# -*- coding: utf-8 -*-
"""
Created on Thu Nov 19 19:52:29 2015

Contains all of the print parameters and the if __name__ == '__main__': logic
so the whole program can be run from here after making parameter changes.

@author: lvanhulle
"""
import math
from collections import namedtuple
import constants as c
import doneShapes as ds
import figura as fg
import time
import itertools

"""
Part Parameters
"""
outline = ds.regularDogBone() # The shape we will be printing
solidityRatio = [1.09]#12]#, 0.1, 0.05] solidityRatio = PathArea/beadArea
printSpeed = [2000] #mm/min head travel speed
shiftX = [10, 50] # amount to shift part from printer origin in X
shiftY = [10, 35, 60] # amount to shift part from printer origin in Y
firstLayerShiftZ = 0 #correct for bed leveling
numLayers = [8] #number of layers to make
trimAdjust = c.EPSILON
pattern = None
# pattern = lg.LineGroup()
# pattern.addLinesFromCoordinateList([[0,0],[2,2],[4,0]])
designType = 0

"""
Layer Parameters
"""
infillAngleDegrees = [0, -45, 90, 45, 45, 90, -45] #degrees infill angle 90 is in Y direction 0 is in X direction
pathWidth = [0.5] #mm distance between centerline of paths
layerHeight = [0.4] #mm height per layer
infillShiftX = [0]
infillShiftY = [0]
#flipLayer = [0] No longer implimented
numShells = [13,1,1,0,0,1,1] # the number of shells max is 13 if 0.4999 path width is used

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

"""
Standard printing settings
"""
RAPID = 4000 #mm/min
TRAVERSE_RETRACT = 0.5 #mm of filament to retract when traversing longer distances
MAX_FEED_TRAVERSE = 10 # max mm to move without lifting the head
MAX_EXTRUDE_SPEED = 100 #mm/min max speed to move filament
Z_CLEARANCE = 10.0 #mm to move Z up
APPROACH_FR = 1500 #mm/min aproach feedrate

def zipVariables_gen(inputLists, repeat=False):
    if iter(inputLists) is iter(inputLists):
        # Tests if inputLists is a generator
        iterType = tuple
    else:
        iterType = type(inputLists)
    variableGenerators = map(itertools.cycle, inputLists)
        
    while 1:
        for _ in max(inputLists, key=len):
            try:
                 # This is the logic for a namedtuple
                yield iterType(*map(next, variableGenerators))
            except Exception:
                yield iterType(map(next, variableGenerators))
        if not repeat:
            break

LayerParams = namedtuple('LayerParams', 'infillShiftX infillShiftY infillAngle \
                                        numShells layerHeight pathWidth')            
_layerParameters = LayerParams(infillShiftX, infillShiftY, infillAngleDegrees, numShells,
                   layerHeight, pathWidth)

def layerParameters():
    return zipVariables_gen(_layerParameters, repeat=True)

PartParams = namedtuple('PartParams', 'solidityRatio printSpeed shiftX shiftY numLayers')
everyPartsParameters = zipVariables_gen(PartParams(
                          solidityRatio, printSpeed, shiftX, shiftY,
                          numLayers))
                          
if __name__ == '__main__':
    startTime = time.time()
    print '\nGenerating code, please wait...'
    
    fig = fg.Figura(outline)
    
    with open(outputSubDirectory+'\\'+outputFileName, 'w') as f:      
        for string in fig.masterGcode_gen():
            f.write(string)
    
    endTime = time.time()
    
    print '\nCode generated.'
    print 'Done writting: ' + outputFileName + '\n'
    print '{:.2f} total time'.format(endTime - startTime)
    
    
    