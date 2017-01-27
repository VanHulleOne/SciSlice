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
                         + 'numShells layerHeight pathWidth infillOverlap pattern')

PartParams = namedtuple('PartParams', 'extrusionFactor printSpeed shiftX shiftY shiftZ')

paramDict = {}

def makeParamObj(param_data, dropdown_data, layerParamLabels, partParamLabels):
    for key, value in param_data.items():
        paramDict[key] = value
    
    currPath = os.path.dirname(os.path.realpath(__file__))
        
    paramDict['startEndSubDirectory'] = currPath + '\\Start_End_Gcode'
             
    for data in dropdown_data: #x in range(len(dropdown_data)):
            the_label = data[c.THE_LABEL]
            if type(paramDict[the_label]) == str:
                del data[c.THE_LABEL]
                if the_label == 'outline':
                    args = {key:value for key,value in data.items()}
                    paramDict['_outline_gen'] = getattr(ds, paramDict['outline'])(**args)
                else:
                    paramDict[the_label] = [getattr(ds, paramDict[the_label])(**data)]
                    
    return Parameters(layerParamLabels, partParamLabels)

class Parameters:
    def __init__(self, layerParamLabels, partParamLabels):
        self.layerParamLabels = layerParamLabels
        self.partParamLabels = partParamLabels
        self.globalParamLabels = []
        nonGlobalLabels = set(layerParamLabels + partParamLabels)
        for key, value in paramDict.items():
            if key not in nonGlobalLabels:
                setattr(self, key, value)
                self.globalParamLabels.append(key)
                
        self.globalParamLabels.sort()
                
        self.partLists = [paramDict[label] for label in partParamLabels]
        self.layerLists = [paramDict[label] for label in layerParamLabels]
        self.layerParamGen = None
        self.outline_gen = None
        self.currHeight = 0
        
        self.LayerParams = namedtuple('LayerParams', self.layerParamLabels)
        self.PartParams = namedtuple('PartParams', self.partParamLabels)
        self.GlobalParams = namedtuple('GlobalParams', self.globalParamLabels)
        self.Params = namedtuple('Params', self.globalParamLabels,
                                           self.partParamLabels,
                                           self.layerParamLabels)
        
    @property
    def layerParams(self):
        return self.LayerParams(*[self.__dict__[label] for label in self.layerParamLabels])
    
    @property
    def partParams(self):
        return self.PartParams(*[self.__dict__[label] for label in self.partParamLabels])
    
    @property
    def globalParams(self):
        return self.GlobalParams(*[self.__dict__[label] for label in self.globalParamLabels])
    
    @property
    def params(self):
        return self.Params(self.__dict__[label] for label in self.Params._fields)
        
    def parts(self):
        partParamGen = zipVariables_gen(self.partLists)
        
        partNum = 1
        for nextPartParams in partParamGen:
            self.layerParamGen = zipVariables_gen(self.layerLists, repeat=True)
            for label, param in zip(self.partParamLabels, nextPartParams):
                setattr(self, label, param)
            yield self.layers()
            partNum += 1
            
    def layers(self):
        self.outline_gen = self._outline_gen()
        next(self.outline_gen)
        layerNum = 1
        for nextLayerParam in self.layerParamGen:
            for label, param in zip(self.layerParamLabels, nextLayerParam):
                setattr(self, label, param)
            yield self.regions(next(self.outline_gen(self.params)))
            layerNum += 1
            
    def region_gen(self, regions):
        global_params = self.params
        
        try:
            outlines, regionParams, self.currHeight = regions
        except Exception:
            outlines, regionParams = regions
            self.currHeight += self.layerHeight
        
        for outline, params in zip(outlines, regionParams):
            self._updateAttributes(params)
            yield outline
            self._updateAttributes(global_params)
    
    def _updateAttributes(self, namedTuple):
        for key, value in namedTuple._asdict().items():
                setattr(self, key, value)
    
    
    

class Parameters2:
    
    def __init__(self, param_data, dropdown_data, layerParamLabels, partParamLabels):
        
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
                    setattr(self, 'outline_gen', getattr(ds, self.outline)(**args)) #lambda:getattr(ds, self.outline)(**args))
                else:
                    setattr(self, the_label, [getattr(ds, getattr(self, the_label))(**data)])

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
            varList = list(map(next, variableGenerators))
            try:
                """ This is the logic for a namedtuple. """
                yield iterType(*varList)
#            except TypeError:
#                """ If we get a TypeError then then we had a namedtuple but the fields
#                are inforrect for some reason.
#                """
#                message = 'In parameters.py namedtuple ' + iterType.__name__ + ' could not be created.'
#                if '' in inputLists:
#                    missing = iterType._fields[inputLists.index('')]
#                    message += ' Variable ' + missing + ' does not contain a value.'
#                else:
#                    message += ' Check spelling of field names.'
#                raise Exception(message)
                
            except Exception:
                yield iterType(varList)
        if not repeat:
            break    

