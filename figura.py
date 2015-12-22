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
from Shape import Shape
from operator import itemgetter

class Figura:
    
    def __init__(self, inShapes):
        layer = self.organizedLayer(inShapes)
        with open('I:\RedBench\static\data\LineList.txt', 'w') as f:
            f.write('test\n')
            f.write(layer.CSVstr())
        self.gcode = '' + gc.startGcode()
        self.partCount = 1
        for partParams in pr.everyPartsParameters:
            print 'Part Count: ' + str(self.partCount)            
            print 'Part Params: ' + str(partParams)
            part = [layer.translate(partParams[c.SHIFT_X],partParams[c.SHIFT_Y],
                                      partParams[c.LAYER_HEIGHT]*(currentLayer+1))
                                      for currentLayer in range(partParams[c.NUM_LAYERS])]
            self.gcode += ';\n\nPart number: ' + str(self.partCount) + '\n'
            self.gcode += ';Parameters: ' + str(partParams) + '\n'
            self.setGcode(part, partParams[c.PRINT_SPEED], partParams[c.EXTRUSION_RATE])
            self.partCount += 1
        self.gcode += gc.endGcode()
    
    def setGcode(self, part, printSpeed, extrusionRate):
        layerNumber = 1
        self.gcode += gc.newPart()
        totalExtrusion = 0
        
        for layer in part:
            self.gcode += ';Layer: ' + str(layerNumber) + '\n'
            self.gcode += ';T' + str(self.partCount) + str(layerNumber) + '\n'
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
                
    def organizedLayer(self, inShapes):
        layer = lg.LineGroup()
        
        lineGens = {i : self.nearestLine_gen(inShapes[i], i) for i in range(len(inShapes))}
        for key, gen in lineGens.iteritems():
            next(gen)
        
        lastPoint = p.Point(0,0)
        index = -1
        while True:
            results = []
            for key in lineGens.keys():
                try:
                    results.append(lineGens[key].send(
                        (True if key == index else False, lastPoint)))
                except StopIteration:
                    del lineGens[key]
            if len(results) == 0: break
            line, index = min(results, key=itemgetter(2))[:2]
            lastPoint = line.end
            layer.append(line)
            if isinstance(inShapes[index], Shape):
                try:
                    line = lineGens[index].send((True, lastPoint))[0]
                except StopIteration:
                    del lineGens[index]
                    break
                else:
                    lastPoint = line.end
                    layer.append(line)
        return layer

    def nearestLine_gen(self, inGroup, key):
        #create a list with all of the point in order, the divide the index by to to get the nearest line
        used, testPoint = yield
        while len(inGroup) > 0:                
            index, sDistance = min(((index, testPoint.distance(line.start))\
                for index, line in enumerate(inGroup)), key=itemgetter(1))
            eIndex, eDistance = min(((index, testPoint.distance(line.end))\
                for index, line in enumerate(inGroup)), key=itemgetter(1))

            if eDistance < sDistance:
                tempLine = inGroup[eIndex]
                tempLine.flip()
                index = eIndex
                used, testPoint = yield tempLine, key, eDistance
            else:
                used, testPoint = yield inGroup[index], key, sDistance
            if used:
                inGroup.pop(index)
    
    def __str__(self):
        tempString = ''
        layerNumber = 1
        for layer in self.layers:
            tempString += ';T' + str(layerNumber) + '\n'
            tempString += ';M6\n'
            tempString += str(layer)
            layerNumber += 1
        return tempString
    
