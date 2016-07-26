# -*- coding: utf-8 -*-
"""
Created on Thu Nov 19 19:52:29 2015
Contains all of the print parameters and the if __name__ == '__main__': logic
so the whole program can be run from here after making parameter changes.
Below is the command for NotePad++ to run this file.
C:\Anaconda3\python.exe -i "$(FULL_CURRENT_PATH)"
@author: lvanhulle
"""

__version__ = '2.0'

from collections import namedtuple
import itertools
import math
import os

import constants as c
import doneShapes as ds

class Parameters:
    
    def __init__(self, full_data):
        self.var_data = full_data[1]
        self.param_data = full_data[0]
        self.param_data['currPath'] = os.path.dirname(os.path.realpath(__file__))
        self.param_data['startEndSubDirectory'] = self.param_data['currPath'] + '\\Start_End_Gcode'
        self.param_data['filamentArea'] = math.pi*self.param_data['filamentDiameter']**2/4.0
        
        if self.param_data['outline'] == c.STL_FLAG:
            self.param_data['shape'] = None
        else:
            self.param_data['shape'] = getattr(ds, self.param_data['outline'])(**self.var_data)
        
        for key, value in self.param_data.items():
            setattr(self, key, value)
        
        self.LayerParams = namedtuple('LayerParams', 'infillShiftX infillShiftY infillAngle '
                                            + 'numShells layerHeight pathWidth trimAdjust')            
        self._layerParameters = self.LayerParams(self.infillShiftX, self.infillShiftY, self.infillAngleDegrees, 
                                                 self.numShells, self.layerHeight, self.pathWidth, self.trimAdjust)
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
