# -*- coding: utf-8 -*-
"""
Created on Thu Nov 19 16:45:00 2015

@author: lvanhulle
"""

import gcode as gc
import parameters as pr

#Test for this comment here

class Figura:
    
    def __init__(self, layer):
        self.layers = [layer.translate(0, 0, pr.layerHeight*(currentLayer+1)) for currentLayer in range(pr.numLayers)]
        self.gcode = ''
        self.setGcode()
    
    def setGcode(self):
        self.gcode += gc.startGcode()
        layerNumber = 1
        for layer in self.layers:
            lines = self.organizeLines(layer.getLines())
            self.gcode += '\n\n;Layer: ' + str(layerNumber) + '\n'
            self.gcode += ';T' + str(layerNumber) + '\n'
            self.gcode += ';M6\n'
            self.gcode += gc.rapidMove(lines[0].start, pr.INCLUDE_Z)
            self.gcode += gc.firstApproach(lines[0].start)
            
            totalExtrusion = 0
            for line in lines:
                totalExtrusion += line.length*pr.extrusionRate
                self.gcode += gc.rapidMove(line.start, pr.OMIT_Z)
                self.gcode += gc.feedMove(line.end, pr.OMIT_Z, totalExtrusion)
            
            self.gcode += gc.retractLayer(totalExtrusion, lines[-1].end)
            layerNumber += 1
        self.gcode += gc.endGcode()
                
                
#TODO: change method to actually work for more than just 90 degree orientation            
    def organizeLines(self, lines):
        flip = False
        for line in lines:
            if flip:
                line.flip()
            flip = not flip
        return lines
        
    
    def __str__(self):
        tempString = ''
        layerNumber = 1
        for layer in self.layers:
            tempString += ';T' + str(layerNumber) + '\n'
            tempString += ';M6\n'
            tempString += str(layer)
            layerNumber += 1
        return tempString
    