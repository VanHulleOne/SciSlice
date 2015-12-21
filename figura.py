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
import Line as l
from operator import itemgetter

class Figura:
    
    def __init__(self, inShapes):
        layer = self.organizedLayer2(inShapes)
#        with open('I:\RedBench\static\data\LineList.txt', 'w') as f:
#            f.write('test\n')
#            f.write(layer.CSVstr())
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
        for lineGroup in inShapes:
            firstLine = None
            if not isinstance(lineGroup, Shape):
                i = 1#TODO method to find first line
            nl_gen = self.nearestLine_gen(lineGroup, firstLine)
            for line in nl_gen:
                layer.append(line)
        return layer
                
    def organizedLayer2(self, inShapes):
        layer = lg.LineGroup()
        
        lineGens = {i : self.nearestLine_gen2(inShapes[i], i) for i in range(len(inShapes))}
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
            
            
    def nearestLine_gen2(self, inGroup, key):
        used, testPoint = yield
        while len(inGroup) > 0:
            startLine, startDist = min(((line, testPoint.distance(line.start))\
                for line in inGroup), key=itemgetter(1))
            endLine, endDist = min(((line, testPoint.distance(line.end))\
                for line in inGroup), key=itemgetter(1))
            if startDist <= endDist:
                sendLine = startLine
                sendDist = startDist
            else:
                endLine.flip()
                sendLine = endLine
                sendDist = endDist
            used, testPoint = yield sendLine, key, sendDist
            if used:
                inGroup.remove(sendLine)
    
    def nearestLine_gen(self, inGroup, prevLine=None):       
        if prevLine is None:
            prevLine = min(inGroup)
            inGroup.remove(prevLine)
        yield prevLine
        
        while len(inGroup) > 0:
            nearestEnd = inGroup[0].start
            nearestOffset = 0
            dist = nearestEnd.distance(prevLine.end)
            isStart = True
            
            for i in range(len(inGroup)):
                tempDist = prevLine.end.distance(inGroup[i].start)
                if(tempDist < dist):
                    nearestEnd = inGroup[i].start
                    dist = tempDist
                    isStart = True
                    nearestOffset = i
                tempDist = prevLine.end.distance(inGroup[i].end)
                if(tempDist < dist):
                    nearestEnd = inGroup[i].end
                    dist = tempDist
                    isStart = False
                    nearestOffset = i
                if(dist == 0): break
            if(not isStart):
                inGroup[nearestOffset].flip()
            yield inGroup.pop(nearestOffset)
    
    def __str__(self):
        tempString = ''
        layerNumber = 1
        for layer in self.layers:
            tempString += ';T' + str(layerNumber) + '\n'
            tempString += ';M6\n'
            tempString += str(layer)
            layerNumber += 1
        return tempString
    