# -*- coding: utf-8 -*-
"""
Created on Thu Oct 29 15:45:02 2015

InFill inherits from LineGroup and is the class responsible for creating the
pattern which will be used as the tool path inside the part.

The most basic operation is to send in a trimShape (typically of type Shape),
a pathWidth, and and angle. From that information a field of lines is created
over trimShape with those lines then being trimmed to trimShape.

If a specific infill pattern is desired a design (typically of type LineGroup)
can be sent in. The design can be in one of several levels of completion.

PARTIAL_ROW
If the design is a partial row the first step is to extend the design by copying
it and placing the start of the first line onto the end of the last line, and
repeating until the design is sifficiently longer than the diagonal of
trimDesign. Although this method would allow for a vertical row the next method
FULL_ROW copies the line only in the Y direction so this shape should be made
to be in the X direction. From there the designed moves to FULL_ROW

FULL_ROW
This is a row that is assumed (and not checked) to be longer than trimShape's
diagonal. This row is then copied in the Y direction until it is taller than
trimShape's diagonal.

FULL_FIELD
This is a field of lines assumed to be wider and taller than trimShape's diagonal.
The center of this field is found and then the field is translated to be at the
center of trimShape

CENTERED_FIELD
This field is wider and taller than trimShape and already centered over the
desired trimShape. The only operation left is to trim all of the lines in the field
to the outline of trimShape

TRIMMED_FIELD
This is a field which requires no additional operations. It is fully formed,
trimmed, and centered over trimShape.

@author: lvanhulle
"""

import Line as l
import Point as p
import Shape as s
from LineGroup import LineGroup as LG
import LineGroup as lg
from math import pi
import time
import matrixTrans as mt
import numpy as np
import constants as c

class InFill(LG):
    
    PARTIAL_ROW = 0
    FULL_ROW = 1
    FULL_FIELD = 2
    CENTERED_FIELD = 3
    TRIMMED_FIELD = 4    
    
    def __init__(self, trimShape, pathWidth, angleDegrees, shiftX=0, shiftY=0,
                 design=None, designType=PARTIAL_ROW):
        LG.__init__(self, None)
        self.shiftX = shiftX
        self.shiftY = shiftY
        self.designType = designType
        self.trimShape = s.Shape(trimShape)
        self.angleRad = (angleDegrees/360.0*2*pi)
        self.pathWidth = pathWidth
        lowerLeft = p.Point(self.trimShape.minX, self.trimShape.minY)
        upperRight = p.Point(self.trimShape.maxX, self.trimShape.maxY)
        
        self.trimDiagonal = (lowerLeft - upperRight)*1.1       
        self.operations = (self.extendDesign, self.createField,
                           self.centerAndRotateField, self.trimField)
        
        if(design is None):
            point1 = p.Point(-self.trimDiagonal-10, 0)
            point2 = p.Point(self.trimDiagonal+10, 0)
            self.design = lg.LineGroup([l.Line(point1, point2)])
            self.designType = self.PARTIAL_ROW
        else:
            self.design = lg.LineGroup(design)
        
        print '\nInFill times:'
        maxLength = max(len(f.__name__) for f in self.operations) + 2 
        for i in range(self.designType, self.TRIMMED_FIELD):
            startTime = time.time()
            self.operations[i]();
            print (self.operations[i].__name__ +
                    ''.ljust(maxLength - len(self.operations[i].__name__)) +
                    '%.2f sec' %(time.time()-startTime))
        
    def extendDesign(self):
        tempDesign = lg.LineGroup(self.design.lines)
        designWidth = self.design.maxX - self.design.minX        
        while(designWidth <= self.trimDiagonal):
            shiftX = self.design[-1].end.x - tempDesign[0].start.x
            shiftY = self.design[-1].end.y - tempDesign[0].start.y
            self.design.addLineGroup(tempDesign.translate(shiftX, shiftY))
            designWidth = self.design.maxX - self.design.minX
        
    def createField(self):
        tempDesign = self.design.translate(0, self.pathWidth)
        designHeight = 0 # abs(self.design.maxY - self.design.minY)
        while(designHeight < self.trimDiagonal):
            self.design.addLineGroup(tempDesign)
            tempDesign = tempDesign.translate(0, self.pathWidth)
            designHeight += self.pathWidth
    
    def centerAndRotateField(self):
        designCP = self.design.getMidPoint()
        trimShapeCP = self.trimShape.getMidPoint()
        transX = trimShapeCP.x - designCP.x
        transY = trimShapeCP.y - designCP.y
        self.design = self.design.transform(mt.combineTransformations(
                        [mt.translateMatrix(transX+self.shiftX, transY+self.shiftY),
                         mt.rotateMatrix(self.angleRad, trimShapeCP)]))
                         
    def trimField(self):
#        startTime = time.time()
        trimStarts = self.trimShape.starts
        trimVectors = self.trimShape.vectors
        fieldStarts = self.design.starts
        fieldVectors = self.design.vectors
        trimLen = len(self.trimShape)
        fieldLen = len(self.design)
        Q_Less_P = fieldStarts - trimStarts.reshape(trimLen,1,2)
        denom = np.cross(trimVectors, fieldVectors.reshape(fieldLen,1,2))
        all_t = np.cross(Q_Less_P, trimVectors.reshape(trimLen,1,2)).transpose()/denom
        all_u = np.cross(Q_Less_P, fieldVectors).transpose()/denom
        
#        print 'Time for all t,u: {:0.3f}'.format(time.time()-startTime)
#        midTime = time.time()
        for t, u, line in zip(all_t, all_u, self.design):
            if not self.trimShape.lineOutsideBoundingBox(line):
                pointSet = set([line.start])
                t = t[(0 <= u) & (u <= 1) & (0 <= t) & (t <= 1)]

                pointSet |= set(p.Point(line.start.x + line.vector[c.X]*value,
                                    line.start.y+line.vector[c.Y]*value)
                                    for value in t)

                pointSet.add(line.end)
                pointList = sorted(list(pointSet))
                for i in xrange(len(pointList)-1):                
                    tempLine = l.Line(pointList[i], pointList[i+1])
                    if(self.trimShape.isInside(tempLine.getMidPoint())):
                        self.lines.append(tempLine)

                
                
                
                
                
                
                
                
                
        