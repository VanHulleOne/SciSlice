# -*- coding: utf-8 -*-
"""
Created on Thu Nov 19 19:52:29 2015
Contains all of the print parameters

@author: lvanhulle
"""

__version__ = '2.2.2'

from collections import namedtuple
import itertools
import math
import os
import inspect

import constants as c
import doneshapes as ds

class Parameters:
    
    def __init__(self, param_data, dropdown_data):
        
        for key, value in param_data.items():
            setattr(self, key, value)
        
        self.currPath = os.path.dirname(os.path.realpath(__file__))
        
        self.startEndSubDirectory = self.currPath + '\\Start_End_Gcode'
        self.filamentArea = math.pi * self.filamentDiameter**2 / 4.0

        #goes through each dictionary, check the 'the_label' dictionary entry
        #that has the dropdown.label as the value and using that value
        #along with setattr and getattr to set the appropriate variable
        #to the appropriate doneshape menu
        for x in range(len(dropdown_data)):
            the_label = dropdown_data[x][c.THE_LABEL]
            if getattr(self, the_label) != c.STL_FLAG:
                if len(dropdown_data[x]) > 1:
                    if type(getattr(self, the_label)) == str:
                        del dropdown_data[x][c.THE_LABEL]
                        setattr(self, the_label, getattr(ds, getattr(self, the_label))(**dropdown_data[x]))

                else:
                    if getattr(self, the_label) != '':
                        setattr(self, the_label, getattr(ds, getattr(self, the_label))())          
        
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
