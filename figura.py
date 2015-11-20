# -*- coding: utf-8 -*-
"""
Created on Thu Nov 19 16:45:00 2015

@author: lvanhulle
"""

import gcode as gc
import parameters as para

class Figura:
    
    def __init__(self, layer, zStep, numLayers):
        self.layers = [layer.translate(0, 0, zStep*currentLayer) for currentLayer in range(1, numLayers+1)]
        self.gcode = ''
    
    def getgcode(self):
        layerNumber = 1
        for layer in self.layers:
            self.gcode += ';Layer: ' + str(layerNumber)
            self.gcode += ';T' + str(layerNumber) + '\n'
            self.gcode += ';M6\n'
            self.gcode += gc.rapidMove(layer.lines[0].start)
            self.gcode += gc.firstApproach(layer.lines[0].start)
            
            
    
    def __str__(self):
        tempString = ''
        layerNumber = 1
        for layer in self.layers:
            tempString += ';T' + str(layerNumber) + '\n'
            tempString += ';M6\n'
            tempString += str(layer)
        return tempString
    