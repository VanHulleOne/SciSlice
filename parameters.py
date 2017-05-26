# -*- coding: utf-8 -*-
"""
Created on Thu Nov 19 19:52:29 2015
Contains all of the print parameters

@author: lvanhulle
"""
""" Version Numbers: Main_Version.sub-version.Feature_Added.Bug_Fixed """
__version__ = '0.3.3.0'

from collections import namedtuple
import itertools
import math
import os
import inspect

import constants as c
import doneshapes as ds

paramDict = {}

def makeParamObj(param_data, dropdown_data, layerParamLabels, partParamLabels):
    for key, value in param_data.items():
        paramDict[key] = value
    
    currPath = os.path.dirname(os.path.realpath(__file__))
        
    paramDict['startEndSubDirectory'] = currPath + '\\Start_End_Gcode'
             
    for data in dropdown_data: #x in range(len(dropdown_data)):
            the_label = data[c.THE_LABEL]
            del data[c.THE_LABEL]
            paramDict[the_label] = getattr(ds, paramDict[the_label])(**data)
            
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
        self.Params = namedtuple('Params', self.globalParamLabels +
                                           self.partParamLabels +
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
        return self.Params(*[self.__dict__[label] for label in self.Params._fields])
        
    def parts(self):
        partParamGen = zipVariables_gen(self.partLists)
        
        partNum = 1
        for nextPartParams in partParamGen:
            self.currHeight = 0
            self.layerParamGen = zipVariables_gen(self.layerLists, repeat=True)
            for label, param in zip(self.partParamLabels, nextPartParams):
                setattr(self, label, param)
            yield self.layers()
            partNum += 1
            
    def layers(self):
        self.outline_gen = self.outline()
        next(self.outline_gen)
        layerNum = 1
        for nextLayerParam in self.layerParamGen:
            for label, param in zip(self.layerParamLabels, nextLayerParam):
                setattr(self, label, param)
            yield self.regions(self.outline_gen.send(self.params))
            layerNum += 1
            
    def regions(self, regions):
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

