# -*- coding: utf-8 -*-
"""
Created on Thu Nov 19 16:45:00 2015

Figura takes all of the parameters and the input shape and creates each layer
for every part. These layers are then converted to Gcode in the form of a list
of strings. The list is stored in self.gcode which can then be accessed and written
to the correct output file by using join().

A layer in Figura starts as a list of LineGroups, typically shells in (Shapes)
and then an InFill but could also be a variety of different shapes all printed
at the same Z-height. The list of layers is then organized and turned into a single
LineGroup with the order of the lines being the print order of the layer. The
goal is to allow easy adjustability when deciding how to organize a layer.
Different organizedLayer() methods could be written calling different
organizing coroutines in the LineGroups to create an ideal print order.

The longest computation time is in creating the infill for the layers. As such
the namedtuple layerParam which is used as a key for the self.layers{}
dictionary. After the layer has been calculated it is stored in layers so that
if another layer with the same parameters is used it does not need to be recalculated.


@author: lvanhulle
"""

import Point as p
import InFill as InF
import LineGroup as lg
import constants as c
from Shape import Shape, Section
import trimesh

class Figura:  
    
    data_points =  open("data_points.txt", 'a')
    
    def __init__(self, stl, param, g_code):
        
        self.mesh = trimesh.load_mesh(stl)        
        
        self.gc = g_code
        self.pr = param
        
        self.maxZ = self.mesh.bounds[:,2:][1]
        
        self.numLayers = []
        
        for layerH in self.pr.layerHeight:
            self.numLayers.append(int((self.maxZ//layerH)[0]))       
        
        self.partCount = 1 # The current part number

        self.layers = {}
        """ The dictionary which stores the computed layers. The key is created in
        layer_gen(). """
        
    def masterGcode_gen(self):
        yield self.gc.startGcode()
        for partParams in self.pr.everyPartsParameters:
            """ pr.everyPartsParameters is a generator of the parameters for the parts.
            The generator stops yielding additional parameters when there are no
            more parts left to print. The parameters are sent to layer_gen() which
            yields each layer of the part. The generator is sent to setGcode()
            along with the partParameters (for printing in the gcode).
            """
            print('\nPart number: ' + str(self.partCount))            
            print(partParams)
           
            yield '\n\n;Part number: ' + str(self.partCount) + '\n'
            yield ';' + str(partParams) + '\n'
            
            yield from self.partGcode_gen(partParams)
                
            self.partCount += 1
        yield self.gc.endGcode()

    def layer_gen(self, partParams):
        """ Creates and yields each organized layer for the part.
        
        The parameters for the part are sent in and the layer parameters
        are called from parameters. If a layer is not in the self.layers dict
        then create the layer and add it to the dictionary. Then yield the
        layer.
        
        Parameters
        ----------
        partParams - a tuple of the parameters for the part
        
        Yields
        ------
        tuple - (LineGroup of the layer ordered for printing, the namedtuple of
        the layer parameters so they can be printed in the gcode.)
        """        
        
        layerParam_Gen = self.pr.layerParameters()
        currHeight = self.pr.firstLayerShiftZ
        
        while currHeight <= self.maxZ:
#            lay += 132
            """ Iterate through for the correct number of layers. """
            layerParam = next(layerParam_Gen)
            
            currHeight += layerParam.layerHeight

            sec = Section(self.mesh.section(plane_origin=[0,0,currHeight],plane_normal=[0,0,1]))#self.shape

            filledList = []

            for shellNumber in range(layerParam.numShells):
                offsetShape = sec.offset(layerParam.pathWidth*(shellNumber), c.INSIDE)
                if offsetShape is not None:
                    filledList.append(offsetShape)
                else:
                    break
                    
                """
                To help with problems that occur when an offset shape has its sides
                collide or if the infill liens are colinear with the trim lines we
                want to fudge the trimShape outward just a little so that we end
                up with the correct lines.
                """
            trimShape = sec.offset(layerParam.pathWidth * layerParam.numShells - 
                            layerParam.trimAdjust, c.INSIDE)
                            
            if trimShape is not None:
                infill = InF.InFill(trimShape,
                                    layerParam.pathWidth, layerParam.infillAngle,
                                    shiftX=layerParam.infillShiftX, shiftY=layerParam.infillShiftY,
                                    design=self.pr.pattern, designType=self.pr.designType)
    #                self.layers[layerParam] = self.organizedLayer(filledList + [infill])
                filledList.append(infill)
            ol = self.organizedLayer(filledList)
            """ a tuple of the organized LineGroup and the layer parameters. """
            yield (ol.translate(partParams.shiftX,
                                            partParams.shiftY, currHeight), layerParam)
#            yield (self.layers[layerParam].translate(partParams.shiftX,
#                                            partParams.shiftY, currHeight), layerParam)
    
    def partGcode_gen(self, partParams):        
        layerNumber = 1
        yield self.gc.newPart()
        totalExtrusion = 0
        
        for layer, layerParam in self.layer_gen(partParams):
            #creats text file of all data points
            data = []
            for line in layer:
                temp = []
                temp.append(str(line.start).replace("X", "").replace("Y", "").replace("Z", "").split(" "))
                temp.append(str(line.end).replace("X", "").replace("Y", "").replace("Z", "").split(" "))
                data.append(temp)
            for entry in data:
                self.data_points.write(str(entry) + "\n")
            extrusionRate = (partParams.solidityRatio*layerParam.layerHeight*
                            layerParam.pathWidth/self.pr.filamentArea)
            yield ';Layer: ' + str(layerNumber) + '\n'
            yield ';' + str(layerParam) + '\n'
            yield ';T' + str(self.partCount) + str(layerNumber) + '\n'
            yield ';M6\n'
            yield ('M117 Layer ' + str(layerNumber) + ' of ' +
                            str(self.numLayers) + '..\n')
            yield self.gc.rapidMove(layer[0].start, c.OMIT_Z)
            yield self.gc.firstApproach(totalExtrusion, layer[0].start)
            
            prevLoc = layer[0].start
            for line in layer:                
                if prevLoc != line.start:
                    if (prevLoc - line.start) < self.pr.MAX_FEED_TRAVERSE:
                        yield self.gc.rapidMove(line.start, c.OMIT_Z)
                    else:
                        yield self.gc.retractLayer(totalExtrusion, prevLoc)
                        yield self.gc.rapidMove(line.start, c.OMIT_Z)
                        yield self.gc.approachLayer(totalExtrusion, line.start)
                        
                line.extrusionRate = extrusionRate
                totalExtrusion += line.length*line.extrusionRate
                yield self.gc.feedMove(line.end, c.OMIT_Z, totalExtrusion,
                                          partParams.printSpeed)
                prevLoc = line.end
            
            yield self.gc.retractLayer(totalExtrusion, layer[-1].end)
            yield '\n'
            layerNumber += 1
        yield ';Extrusion amount for part is ({:.1f} mm)\n\n'.format(totalExtrusion)
                
    def organizedLayer(self, inShapes):
        """ Takes in a list of LineGroup objects and returns them as an organized layer.
        
        A dictonary was used to hold the coroutines from LineGroup since we
        will want to delete keys, value pairs while iterating throught the dict.
        
        The coroutines yield in a boolean and a Point and then yield back out
        the line which is 'closest' to the point. 'Closest' being in quotes
        because we could use any number of parameters to decide which line is
        closest from Euclidean distance of end points to time since its neighbor
        was printed (for cooling purposes). The yielded in boolean is whether or
        not the previous line was used.
        
        Currently if the LineGroup with the closest line is a Shape then the
        entire Shape is printed before checking any other LineGroups again.
        
        Parameters
        ----------
        inShapes - a list of LineGroups that make up the layer
        
        Return
        ------
        A single organized LineGroup 
        """
        layer = lg.LineGroup()
        
        lineCoros = {i : inShapes[i].nearestLine_Coro(i) for i in range(len(inShapes))}
        
        for coro in lineCoros.values():
            next(coro)
        
        lastPoint = p.Point(0,0) # The starting point is the origin of the printer
        indexOfClosest = -1 # A default value for the inital run
        while 1:
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
            if isinstance(inShapes[indexOfClosest], Shape):
                """ If the closest line was from a Shape then go around the whole
                shape without checking any other LineGroup. Shapes are required
                to be continuous contours (except if the have internal holes) so
                there is no need to check any other LineGroup for a closer line.
                Plus if the shape was being used as a brim to help start a print
                we would not want to stop party way through the brim.
                """
                while 1:
                    try:
                        line = lineCoros[indexOfClosest].send((c.USED, lastPoint))[0]
                    except StopIteration:
                        del lineCoros[indexOfClosest]
                        break
                    else:
                        """ A reminder than an else is run if there is no exception. """
                        lastPoint = line.end
                        layer.append(line)
        """
        #creats text file of all data points
        data = []
        for line in layer:
            temp = []
            temp.append(str(line.start).replace("X", "").replace("Y", "").replace("Z", "").split(" "))
            temp.append(str(line.end).replace("X", "").replace("Y", "").replace("Z", "").split(" "))
            data.append(temp)
        for entry in data:
            self.data_points.write(str(entry) + "\n")
        """
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
        
    def close_file(self):
        self.data_points.close()
    
