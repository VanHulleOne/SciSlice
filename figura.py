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
import numpy as np

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
        used, testPoint = yield
        normList = []
        for line in inGroup:
            normList.append(line.start.normalVector)
            normList.append(line.end.normalVector)
        normList = np.array(normList)
        while len(inGroup) > 0:
            """
            This got a little complicated but sped up this section by about 10X
            This next line inside out does as follows:
            1) take the normList and subtract the normVector from the test point
                This actually subtracts the testPointNormVector from each individual
                element in the normList
            2) Use numpy.linalg.norm to get the length of each element. The first
                object is out subtracted array, None is for something I don't understand
                1 is so that it takes the norm of each element and not of the whole
                array
            3) enumerate over the array of norms so we can later have the index
            4) enumerate is a generator, for our using a for comprehension to
                send the tuple (index, dist) to the min function. The norm stored
                in each element of the array is the distance from the testPoint to
                the point which was at that index
            5) Find the min of the tuples (index, dist) key-itemgetter(1) is telling min
                to look at dist when comparing the tuples
            6) min returns the lowest tuple, which we split into index and dist
            """
            index, dist = min(((index, dist) for index, dist in
                enumerate(np.linalg.norm(normList-testPoint.normalVector, None, 1))),
                key=itemgetter(1))
            if index%2: #If index is odd we are at the end of a line so the line needs to be flipped
                inGroup[index/2].flip()
            index /= 2
            used, testPoint = yield inGroup[index], key, dist
            if used:
                inGroup.pop(index)
                normList = np.delete(normList, [index*2, index*2+1],0)
    
    def __str__(self):
        tempString = ''
        layerNumber = 1
        for layer in self.layers:
            tempString += ';T' + str(layerNumber) + '\n'
            tempString += ';M6\n'
            tempString += str(layer)
            layerNumber += 1
        return tempString
    
