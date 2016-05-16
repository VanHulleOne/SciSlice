# -*- coding: utf-8 -*-
"""
Created on Thu Nov 19 16:45:00 2015

@author: lvanhulle
"""

import gcode as gc
import parameters as pr
import Point as p
import InFill as InF
import LineGroup as lg
import constants as c
from Shape import Shape
from operator import itemgetter
import numpy as np
import time
import Line as l

class Figura:  
    
    def __init__(self, shape):
        self.shape = shape
#        startTime = time.time()
#        layer = self.organizedLayer(inShapes)
#        layer = layer.translate(0,0, pr.firstLayerShiftZ)
#        print '\nLayer organized in: %.2f sec\n' %(time.time() - startTime)
#        with open('I:\RedBench\static\data\LineList.txt', 'w') as f:
#            f.write('test\n')
#            f.write(layer.CSVstr())
        self.gcode = [gc.startGcode()]
        self.partCount = 1
        self.layers = {}
        for partParams in pr.everyPartsParameters:
            print '\nPart number: ' + str(self.partCount)            
            print partParams
            part = self.part_Gen(partParams)
            self.gcode += '\n\n;Part number: ' + str(self.partCount) + '\n'
            self.gcode += ';' + str(partParams) + '\n'
            self.setGcode(part, partParams)
            self.partCount += 1
        self.gcode += gc.endGcode()

    def part_Gen(self, partParams):
        layerParam_Gen = pr.zipVariables_gen(pr.layerParameters,
                                             namedTuple = pr.LayerParams, repeat=True)
        currHeight = pr.firstLayerShiftZ
        
        for i in range(partParams.numLayers):
            layerPar = next(layerParam_Gen)
            layerName = (layerPar.infillAngle, layerPar.numShells,
                         layerPar.infillShiftX, layerPar.infillShiftY)
            currHeight += layerPar.layerHeight
            
            if layerName not in self.layers:
                currOutline = self.shape
                filledList = []
                for shellNumber in xrange(layerPar.numShells):
                    filledList.append(currOutline)
                    currOutline = currOutline.offset(layerPar.pathWidth-pr.trimAdjust, c.INSIDE)
                    
                infill = InF.InFill(currOutline, layerPar.pathWidth, layerPar.infillAngle,
                                    shiftX=layerPar.infillShiftX, shiftY=layerPar.infillShiftY)
                self.layers[layerName] = self.organizedLayer(filledList + [infill])
                
            yield (self.layers[layerName].translate(partParams.shiftX,
                                            partParams.shiftY, currHeight), layerPar)
    
    def setGcode(self, part, partParams):
        
        layerNumber = 1
        self.gcode += gc.newPart()
        totalExtrusion = 0
        
        for layer, layerPar in part:
            extrusionRate = (partParams.solidityRatio*layerPar.layerHeight*
                            layerPar.pathWidth/pr.filamentArea)
            self.gcode += ';Layer: ' + str(layerNumber) + '\n'
            self.gcode += ';' + str(layerPar) + '\n'
            self.gcode += ';T' + str(self.partCount) + str(layerNumber) + '\n'
            self.gcode += ';M6\n'
            self.gcode += ('M117 Layer ' + str(layerNumber) + ' of ' +
                            str(partParams.numLayers) + '..\n')
            self.gcode += gc.rapidMove(layer[0].start, c.OMIT_Z)
            self.gcode += gc.firstApproach(totalExtrusion, layer[0].start)
            
            prevLoc = layer[0].start
            for line in layer:
                
                if prevLoc != line.start:
                    if (prevLoc - line.start) < pr.MAX_FEED_TRAVERSE:
                        self.gcode += gc.rapidMove(line.start, c.OMIT_Z)
                    else:
                        self.gcode += gc.retractLayer(totalExtrusion, prevLoc)
                        self.gcode += gc.rapidMove(line.start, c.OMIT_Z)
                        self.gcode += gc.approachLayer(totalExtrusion, line.start)
                        
                line.extrusionRate = extrusionRate
                totalExtrusion += line.length*line.extrusionRate
                self.gcode += gc.feedMove(line.end, c.OMIT_Z, totalExtrusion,
                                          partParams.printSpeed)
                prevLoc = line.end
            
            self.gcode += gc.retractLayer(totalExtrusion, layer[-1].end)
            self.gcode += '\n'
            layerNumber += 1
        self.gcode += ';Extrusion amount for part is ({:.1f} mm)\n\n'.format(totalExtrusion)
                
    def organizedLayer(self, inShapes):
        layer = lg.LineGroup()
        
        lineCoros = {i : inShapes[i].nearestLine_Coro(i) for i in range(len(inShapes))}
        for key, coro in lineCoros.iteritems():
            next(coro)
        
        lastPoint = p.Point(0,0)
        index = -1        
        while True:
            results = []
            for key in lineCoros.keys():
                try:
                    results.append(lineCoros[key].send(
                        (True if key == index else False, lastPoint)))
                except StopIteration:
                    del lineCoros[key]
            if len(results) == 0: break
            line, index = min(results, key=itemgetter(2))[:2]
            lastPoint = line.end
            layer.append(line)
            if isinstance(inShapes[index], Shape):
                while True:
                    try:
                        line = lineCoros[index].send((True, lastPoint))[0]
                    except StopIteration:
                        del lineCoros[index]
                        break
                    else:
                        lastPoint = line.end
                        layer.append(line)
        return layer
    
    def __str__(self):
        tempString = ''
        layerNumber = 1
        for layer in self.layers:
            tempString += ';T' + str(layerNumber) + '\n'
            tempString += ';M6\n'
            tempString += str(layer)
            layerNumber += 1
        return tempString
    
