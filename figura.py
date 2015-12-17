# -*- coding: utf-8 -*-
"""
Created on Thu Nov 19 16:45:00 2015

@author: lvanhulle
"""

import gcode as gc
import parameters as pr
import Point as p
import InFill as Inf
import LineGroup as lg
from parameters import constants as c
import itertools

class Figura:
    
    def __init__(self, inShapes):
        layer = lg.LineGroup(self.organizeLines(list(itertools.chain.from_iterable(inShapes))))
        self.gcode = '' + gc.startGcode()
        partCount = 1
        for partParams in pr.everyPartsParameters:
            print 'Part Count: ' + str(partCount)            
            print 'Part Params: ' + str(partParams)
            part = [layer.translate(partParams[c.SHIFT_X],partParams[c.SHIFT_Y],
                                      partParams[c.LAYER_HEIGHT]*(currentLayer+1))
                                      for currentLayer in range(partParams[c.NUM_LAYERS])]
            self.gcode += ';\n\nPart number: ' + str(partCount) + '\n'
            self.gcode += ';Parameters: ' + str(partParams) + '\n'
            self.setGcode(part, partParams[c.PRINT_SPEED], partParams[c.EXTRUSION_RATE])
            partCount += 1
        self.gcode += gc.endGcode()
    
    def setGcode(self, part, printSpeed, extrusionRate):
        layerNumber = 1
        self.gcode += gc.newPart()
        totalExtrusion = 0
        
        for layer in part:
            self.gcode += ';Layer: ' + str(layerNumber) + '\n'
            self.gcode += ';T' + str(layerNumber) + '\n'
            self.gcode += ';M6\n'
            self.gcode += gc.rapidMove(layer[0].start, pr.INCLUDE_Z)
            self.gcode += gc.firstApproach(layer[0].start)
            
            for line in layer:
                line.extrusionRate = extrusionRate
                totalExtrusion += line.length*line.extrusionRate
                self.gcode += gc.rapidMove(line.start, pr.OMIT_Z)
                self.gcode += gc.feedMove(line.end, pr.OMIT_Z, totalExtrusion, printSpeed)
            
            self.gcode += gc.retractLayer(totalExtrusion, layer[-1].end)
            self.gcode += '\n\n'
            layerNumber += 1        
                           
    def organizeLines(self, lines):
        lines.sort()
        organizedLines = [lines.pop(0)]
        
        while len(lines) > 0:
            nearestEnd = lines[0].start
            nearestOffset = 0
            dist = nearestEnd.distance(organizedLines[0].end)
            isStart = True
            
            for i in range(len(lines)):
                tempDist = organizedLines[-1].end.distance(lines[i].start)
                if(tempDist < dist):
                    nearestEnd = lines[i].start
                    dist = tempDist
                    isStart = True
                    nearestOffset = i
                tempDist = organizedLines[-1].end.distance(lines[i].end)
                if(tempDist < dist):
                    nearestEnd = lines[i].end
                    dist = tempDist
                    isStart = False
                    nearestOffset = i
                if(dist == 0): break
            if(not isStart):
                lines[nearestOffset].flip()
            organizedLines.append(lines.pop(nearestOffset))
            
        return organizedLines
    
    def __str__(self):
        tempString = ''
        layerNumber = 1
        for layer in self.layers:
            tempString += ';T' + str(layerNumber) + '\n'
            tempString += ';M6\n'
            tempString += str(layer)
            layerNumber += 1
        return tempString
    