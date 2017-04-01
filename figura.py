# -*- coding: utf-8 -*-
"""
Created on Thu Nov 19 16:45:00 2015

Figura takes all of the parameters and the input outline and creates each layer
for every part. These layers are then converted to Gcode in the form of a list
of strings. The list is stored in self.gcode which can then be accessed and written
to the correct output file by using join().

A layer in Figura starts as a list of LineGroups, typically shells in (Outlines)
and then an Infill but could also be a variety of different outlines all printed
at the same Z-height. The list of layers is then organized and turned into a single
LineGroup with the order of the lines being the print order of the layer. The
goal is to allow easy adjustability when deciding how to organize a layer.
Different organizedLayer() methods could be written calling different
organizing coroutines in the LineGroups to create an ideal print order.


@author: lvanhulle
"""

from point import Point
from infill import Infill
from linegroup import LineGroup
from line import Line
import constants as c
from outline import Outline, Section
from functools import lru_cache
import math
import os
import random

class Figura:  
    
    def __init__(self, param, g_code):
        
        self.data_points =  []
        
        self.gc = g_code
        self.pr = param
        
        self.partCount = 1 # The current part number

    def masterGcode_gen(self):
        yield self.gc.startGcode(bed_temp = self.pr.bed_temp, extruder_temp = self.pr.extruder_temp)
        for layers in self.pr.parts():
            """ pr.everyPartsParameters is a generator of the parameters for the parts.
            The generator stops yielding additional parameters when there are no
            more parts left to print. The parameters are sent to layer_gen() which
            yields each layer of the part. The generator is sent to setGcode()
            along with the partParameters (for printing in the gcode).
            """
            print('\nPart number: ' + str(self.partCount))            
            print('Part Params: ', self.pr.partParams)
           
            yield '\n\n' + self.gc.comment('Part number: ' + str(self.partCount) + '\n')
            yield self.gc.comment(str(self.pr.partParams) + '\n')
            
            yield from self.partGcode_gen(layers)
                
            self.partCount += 1
        yield self.gc.endGcode()

    def layer_gen(self, layers):
        """
        Creates and yields each organized layer for the part.
        
        Parameters
        ----------
        partParams - a tuple of the parameters for the part
        
        Yields
        ------
        tuple - (LineGroup of the layer ordered for printing, the namedtuple of
        the layer parameters so they can be printed in the gcode.)
        """  
        layerCountdown = self.pr.numLayers
        isFirstLayer = True
        random.seed(self.pr.randomStartLocation) # Seed the random so the results are repeatable

        for regions in layers:
            if layerCountdown == 0:
                break
                    
            fullLayer = self.make_layer(isFirstLayer, regions)
            
            yield fullLayer.translate(self.pr.shiftX, self.pr.shiftY,
                                self.pr.currHeight+self.pr.shiftZ)
            layerCountdown -= 1
            isFirstLayer = False

    def make_layer(self, isFirstLayer, regions):
        filledList = []
        for outline in regions:
            region = make_region(outline, self.pr.horizontalExpansion, self.pr.nozzleDiameter,
                                          isFirstLayer, self.pr.brims, self.pr.numShells,
                                          self.pr.infillOverlap, self.pr.pattern, self.pr.pathWidth,
                                          self.pr.infillAngleDegrees, self.pr.infillShiftX,
                                          self.pr.infillShiftY, self.pr.designType,
                                          self.pr.extrusionFactor)

            filledList.extend(region)

        layer = organizedLayer(tuple(filledList),
                               random.random() if self.pr.randomStartLocation
                                               else 0)
        if not layer:
            raise(Exception('Parameter setting produced no tool path. \n' +
                            'Ensure numLayers is >0 and there is at least one ' +
                            'shell if no infill is used.'))
        return layer
    

    
    def partGcode_gen(self, layers):        
        layerNumber = 1
        yield self.gc.newPart()
        totalExtrusion = 0
        part = []
        
        for layer in self.layer_gen(layers):
            layer_hold = []
            extrusionRate = (self.pr.layerHeight*
                            self.pr.nozzleDiameter/(math.pi * self.pr.filamentDiameter**2/4.0))
            yield self.gc.comment('Layer: ' + str(layerNumber) + '\n')
            yield self.gc.comment(str(self.pr.layerParams) + '\n')
            yield self.gc.comment('T' + str(self.partCount) + str(layerNumber) + '\n')
            yield self.gc.comment('M6\n')
            yield self.gc.operatorMessage('Layer', layerNumber, 'of', self.pr.numLayers)
            yield self.gc.rapidMove(layer[0].start, atClearance = True)
            yield self.gc.firstApproach(totalExtrusion, layer[0].start)
            
            prevLoc = layer[0].start
            for line in layer:
                layer_hold.extend(point.point for point in line)
                if prevLoc != line.start:
                    if (prevLoc - line.start) < self.pr.retractMinTravel:
                        yield self.gc.rapidMove(line.start)
                    else:
                        yield self.gc.retractLayer(totalExtrusion, prevLoc)
                        yield self.gc.rapidMove(line.start, atClearance=True)
                        yield self.gc.approachLayer(totalExtrusion, line.start)
                        
                totalExtrusion += line.length*line.extrusionFactor*extrusionRate
                yield self.gc.feedMove(line.end, totalExtrusion,
                                          self.pr.printSpeed)
                prevLoc = line.end

            part.append(layer_hold)
            yield self.gc.retractLayer(totalExtrusion, layer[-1].end)
            yield '\n'
            layerNumber += 1
        yield self.gc.comment('Extrusion amount for part is ({:.1f} mm)\n\n'.format(totalExtrusion))
        self.data_points.append(part)

@lru_cache(maxsize=16)            
def organizedLayer(inOutlines, randStart):
    """ Takes in a list of LineGroup objects and returns them as an organized layer.
    
    A dictonary was used to hold the coroutines from linegroup since we
    will want to delete keys, value pairs while iterating throught the dict.
    
    The coroutines yield in a boolean and a Point and then yield back out
    the line which is 'closest' to the point. 'Closest' being in quotes
    because we could use any number of parameters to decide which line is
    closest from Euclidean distance of end points to time since its neighbor
    was printed (for cooling purposes). The yielded in boolean is whether or
    not the previous line was used.
    
    Currently if the LineGroup with the closest line is a outline then the
    entire outline is printed before checking any other LineGroups again.
    
    Parameters
    ----------
    inOutlines - a list of LineGroups that make up the layer
    
    Return
    ------
    A single organized LineGroup 
    """
    layer = LineGroup()
    
    lineCoros = {i : inOutlines[i].nearestLine_Coro(i) for i in range(len(inOutlines))}
    
    for coro in lineCoros.values():
        next(coro)
    
    """
    Find the lower left most point of the boudnding box which encloses
    the layer and use that as the starting point for the sort.
    """
    minX = min(i.minX for i in inOutlines)
    minY = min(i.minY for i in inOutlines)    
    
    if randStart:
        farthestLeftOutline = min(inOutlines, key=lambda x:x.minX)
        startPoint = random.choice(farthestLeftOutline.lines).start
        
#        maxX = min(i.maxX for i in inOutlines)
#        maxY = min(i.maxY for i in inOutlines)
#
#        line = Line(Point(minX, minY), Point(maxX, maxY))
#                          
#        angle = 2*math.pi*randStart
#        startX = line.getMidPoint().x + line.length/2*math.cos(angle)
#        startY = line.getMidPoint().y + line.length/2*math.sin(angle)
#        
#        startPoint = Point(startX, startY)
    else:
        startPoint = Point(minX, minY)
        
    lastPoint = startPoint # The starting point for the sort
    indexOfClosest = -1 # A default value for the inital run
    while True:
        results = []
        for key in list(lineCoros.keys()):
            try:
                results.append(lineCoros[key].send(
                    (c.USED if key == indexOfClosest else c.NOT_USED, lastPoint)))
            except StopIteration:
                """ If we get a StopIteration exception from the coroutine
                that means the LineGroup has no more Lines and we can remove
                it from the dictionary. """                    
                del lineCoros[key]
                
        if len(results) == 0: break # No more items in the dictionary
        result = min(results, key=lambda x:x.distance)
        line = result.line
        indexOfClosest = result.name
        lastPoint = line.end
        layer.append(line)
        if isinstance(inOutlines[indexOfClosest], Outline):
            """ If the closest line was from an Outline then go around the whole
            outline without checking any other LineGroup. Outlines are required
            to be continuous contours (except if the have internal holes) so
            there is no need to check any other LineGroup for a closer line.
            Plus if the outline was being used as a brim to help start a print
            we would not want to stop partially through the brim.
            """
            while True:
                try:
                    line = lineCoros[indexOfClosest].send((c.USED, lastPoint)).line
                except StopIteration:
                    del lineCoros[indexOfClosest]
                    break
                else:
                    """ A reminder than an else is run if there is no exception. """
                    lastPoint = line.end
                    layer.append(line)
    return layer

@lru_cache(maxsize=16)
def make_region(outline, horizontalExpansion, nozzleDiameter, isFirstLayer, brims, numShells,
                infillOverlap, pattern, pathWidth, infillAngleDegrees, infillShiftX,
                infillShiftY, designType, extrusionFactor):
    region = []
    new_outline = outline.offset(horizontalExpansion-nozzleDiameter/2.0, c.OUTSIDE) 
    if isFirstLayer and brims:
        region.extend(new_outline.shell_gen(number=brims,
                                            dist = nozzleDiameter,
                                            side = c.OUTSIDE,
                                            ))

    region.extend(new_outline.shell_gen(number = numShells,
                                        dist = nozzleDiameter,
                                        side = c.INSIDE,
                                        ))
            
    """
    To help with problems that occur when an offset outline has its sides
    collide or if the infill lines are co-linear with the trim lines we
    want to fudge the trimOutline outward just a little so that we end
    up with the correct lines.
    """
    trimOutline = new_outline.offset(infillOverlap
                                 - nozzleDiameter * numShells,
                                 c.OUTSIDE)
                    
    if trimOutline and pattern: # If there is an outline to fill and we want an infill
        infill = Infill(trimOutline,
                            pathWidth, infillAngleDegrees,
                            shiftX=infillShiftX, shiftY=infillShiftY,
                            design=pattern, designType=designType)
        region.append(infill)
        
    for group in region:
        for line in group:
            line.extrusionFactor = extrusionFactor
    return region


#    def __str__(self):
#        tempString = ''
#        layerNumber = 1
#        for layer in self.layers:
#            tempString += self.pr.comment + 'T' + str(layerNumber) + '\n'
#            tempString += self.pr.comment + 'M6\n'
#            tempString += str(layer)
#            layerNumber += 1
#        return tempString