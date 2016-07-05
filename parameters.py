# -*- coding: utf-8 -*-
"""
Created on Thu Nov 19 19:52:29 2015
Contains all of the print parameters and the if __name__ == '__main__': logic
so the whole program can be run from here after making parameter changes.
Below is the command for NotePad++ to run this file.
C:\Anaconda3\python.exe -i "$(FULL_CURRENT_PATH)"
@author: lvanhulle
"""
import math
from collections import namedtuple
import constants as c
import doneShapes as ds
import time
import itertools
import os
import numpy as np
import json
import trimesh
import Shape as s
import Point as p

class Parameters:

    """
    Part Parameters
    """
    outline = ds.regularDogBone() # The shape we will be printing
    solidityRatio = [1.09]#12]#, 0.1, 0.05] solidityRatio = PathArea/beadArea
    printSpeed = [2000] #mm/min head travel speed
    shiftX = [10, 50] # amount to shift part from printer origin in X
    shiftY = [10, 35, 60] # amount to shift part from printer origin in Y
    firstLayerShiftZ = 0 #correct for bed leveling
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
    numLayers = []
    infillShiftX = [0]
    infillShiftY = [0]
    #flipLayer = [0] No longer implimented
    numShells = [13,1,1,0,0,1,1] # the number of shells max is 13 if 0.4999 path width is used
    trimAdjust = [2*c.EPSILON]
    
    """
    File Parameters
    """
    outputFileName = 'Testing.gcode' #the name of the file you want output. git will ignore all .gcode unless they start with SAVE
    currPath = os.path.dirname(os.path.realpath(__file__))
    outputSubDirectory = currPath + '\\Gcode'
    startEndSubDirectory = currPath + '\\Start_End_Gcode'

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
    
    param_data = {}
    
    LayerParams = None
    _layerParameters = None
    
    def __init__(self, main_data): 
        for key in main_data:
            self.param_data[key] = main_data[key]          
        for key in self.param_data:
            setattr(self, key, self.param_data[key])
        print(self.outputFileName)
        self.param_data["outputFileName"] = self.outputFileName
        self.param_data["currPath"] = os.path.dirname(os.path.realpath(__file__))
        self.param_data["outputSubDirectory"] = self.currPath + '\\Gcode'
        self.param_data["startEndSubDirectory"] = self.currPath + '\\Start_End_Gcode'
        self.param_data["filamentDiameter"] = 3.0
        self.param_data["filamentArea"] = math.pi*self.filamentDiameter**2/4.0
        self.param_data["nozzleDiameter"] = 0.5
        self.param_data["RAPID"] = 4000
        self.param_data["TRAVERSE_RETRACT"] = 0.5
        self.param_data["MAX_FEED_TRAVERSE"] = 10
        self.param_data["MAX_EXTRUDE_SPEED"] = 100
        self.param_data["Z_CLEARANCE"] = 10.0
        self.param_data["APPROACH_FR"] = 1500
        self.LayerParams = namedtuple('LayerParams', 'infillShiftX infillShiftY infillAngle \
                                            numShells layerHeight pathWidth trimAdjust')            
        self._layerParameters = self.LayerParams(self.infillShiftX, self.infillShiftY, self.infillAngleDegrees, self.numShells,
                       self.layerHeight, self.pathWidth, self.trimAdjust)
        self.PartParams = namedtuple('PartParams', 'solidityRatio printSpeed shiftX shiftY numLayers')
        self.everyPartsParameters = self.zipVariables_gen(self.PartParams(
                              self.solidityRatio, self.printSpeed, self.shiftX, self.shiftY,
                              self.numLayers))                        
        
    def zipVariables_gen(self, inputLists, repeat=False):
        if iter(inputLists) is iter(inputLists):
            # Tests if inputLists is a generator
            iterType = tuple
        else:
            iterType = type(inputLists)
        variableGenerators = list(map(itertools.cycle, inputLists))
            
        while 1:
            for _ in max(inputLists, key=len):
                try:
                     # This is the logic for a namedtuple
                    yield iterType(*list(map(next, variableGenerators)))
                except Exception:
                    yield iterType(list(map(next, variableGenerators)))
            if not repeat:
                break    
    
    
    def layerParameters(self):
        return self.zipVariables_gen(self._layerParameters, repeat=True)
    
    
        
     
                              
if __name__ == '__main__':
    Parameters.run()