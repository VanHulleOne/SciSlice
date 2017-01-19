# -*- coding: utf-8 -*-
"""
Created on Thu Nov 19 19:52:29 2015
Contains all of the print parameters

@author: lvanhulle
"""
""" Version Numbers: Main_Version.sub-version.Feature_Added.Bug_Fixed """
__version__ = '0.2.4.0'

from collections import namedtuple
import itertools
import math
import os
import inspect

import constants as c
import doneshapes as ds

LayerParams = namedtuple('LayerParams', 'infillShiftX infillShiftY infillAngleDegrees '
                         + 'numShells layerHeight pathWidth trimAdjust')

PartParams = namedtuple('PartParams', 'solidityRatio printSpeed shiftX shiftY numLayers')

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
        for data in dropdown_data: #x in range(len(dropdown_data)):
            the_label = data[c.THE_LABEL]
            if type(getattr(self, the_label)) == str:
                del data[c.THE_LABEL]
                if the_label == 'outline':
                    args = {key:value for key,value in data.items()}
                    setattr(self, 'secgen', lambda:getattr(ds, self.outline)(**args))
                else:
                    setattr(self, the_label, getattr(ds, getattr(self, the_label))(**data))

        # to prevent having to type variable names three times we read in the fields from the namedtuple templates
        # and use them to generate the namedtuples
        layerParamLists = LayerParams(*[getattr(self, field) for field in LayerParams._fields]) 

        self.layerParameters = lambda : zipVariables_gen(layerParamLists, repeat=True)
        
        self.everyPartsParameters = zipVariables_gen(PartParams(*[getattr(self, field) for field in PartParams._fields]))                     
  
def zipVariables_gen(inputLists, repeat=False):
    if iter(inputLists) is iter(inputLists):
        # Tests if inputLists is a generator
        iterType = tuple
    else:
        iterType = type(inputLists)
    variableGenerators = list(map(itertools.cycle, inputLists))
        
    while True:
        for _ in max(inputLists, key=len):
            try:
                 # This is the logic for a namedtuple
                yield iterType(*list(map(next, variableGenerators)))
            except Exception:
                yield iterType(list(map(next, variableGenerators)))
        if not repeat:
            break    

