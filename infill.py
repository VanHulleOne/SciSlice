# -*- coding: utf-8 -*-
"""
Created on Thu Oct 29 15:45:02 2015

Infill inherits from linegroup and is the class responsible for creating the
pattern which will be used as the tool path inside the part.

The most basic operation is to send in a trimOutline (typically of type Outline),
a pathWidth, and and angle. From that information a field of lines is created
over trimOutline with those lines then being trimmed to trimOutline.

If a specific infill pattern is desired a design (typically of type LineGroup)
can be sent in. The design can be in one of several levels of completion.

PARTIAL_ROW
If the design is a partial row the first step is to extend the design by copying
it and placing the start of the first line onto the end of the last line, and
repeating until the design is sufficiently longer than the diagonal of
trimDesign. Although this method would allow for a vertical row the next method
FULL_ROW copies the line only in the Y direction so this outline should be made
to be in the X direction. From there the designed moves to FULL_ROW

FULL_ROW
This is a row that is assumed (and not checked) to be longer than trimOutline's
diagonal. This row is then copied in the Y direction until it is taller than
trimOutline's diagonal.

FULL_FIELD
This is a field of lines assumed to be wider and taller than trimOutline's diagonal.
The center of this field is found and then the field is translated to be at the
center of trimOutline

CENTERED_FIELD
This field is wider and taller than trimOutline and already centered over the
desired trimOutline. The only operation left is to trim all of the lines in the field
to the outline of trimOutline

TRIMMED_FIELD
This is a field which requires no additional operations. It is fully formed,
trimmed, and centered over trimOutline.

@author: lvanhulle
"""

from line import Line
from point import Point
from outline import Outline
from linegroup import LineGroup
import time
import matrixTrans as mt
import numpy as np
import constants as c
import doneshapes as ds

class Infill(LineGroup):
    
   
    
    def __init__(self, trimOutline, pathWidth, angleDegrees, shiftX=0, shiftY=0,
                 design=None, designType=c.PARTIAL_ROW):
        LineGroup.__init__(self, None)
        self.shiftX = shiftX
        self.shiftY = shiftY
        self.designType = designType
        self.trimOutline = Outline(trimOutline)
        self.angleRad = (angleDegrees/360.0*2*np.pi)
        self.pathWidth = pathWidth
        lowerLeft = Point(self.trimOutline.minX, self.trimOutline.minY)
        upperRight = Point(self.trimOutline.maxX, self.trimOutline.maxY)
        
        self.trimDiagonal = (lowerLeft - upperRight)*1.1       
        self.operations = (self.extendDesign, self.createField,
                           self.centerAndRotateField, self.trimField)
        
        try:
#            point1 = Point(-self.trimDiagonal-10, 0)
#            point2 = Point(self.trimDiagonal+10, 0)
            self.design = design(self.pathWidth, self.trimDiagonal, self.trimDiagonal) #ds.lineField(self.pathWidth, self.trimDiagonal, self.trimDiagonal)#lg.LineGroup([Line(point1, point2)])
            self.designType = c.FULL_FIELD
        except Exception:
            self.design = LineGroup(design)
        
#        print('\nInfill times:')
#        maxLength = max(len(f.__name__) for f in self.operations) + 2 
        for i in range(self.designType, c.TRIMMED_FIELD):
            startTime = time.time()
            self.operations[i]();
#            print((self.operations[i].__name__ +
#                    ''.ljust(maxLength - len(self.operations[i].__name__)) +
#                    '%.2f sec' %(time.time()-startTime)))
        
    def extendDesign(self):
        tempDesign = LineGroup(self.design.lines)
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
        trimOutlineCP = self.trimOutline.getMidPoint()
        transX = trimOutlineCP.x - designCP.x
        transY = trimOutlineCP.y - designCP.y
        self.design = self.design.transform(mt.combineTransformations(
                        [mt.translateMatrix(transX+self.shiftX, transY+self.shiftY),
                         mt.rotateMatrix(self.angleRad, trimOutlineCP)]))
                         
    def trimField(self):
        trimStarts = self.trimOutline.starts
        trimVectors = self.trimOutline.vectors
        fieldStarts = self.design.starts
        fieldVectors = self.design.vectors
        trimLen = len(self.trimOutline)
        fieldLen = len(self.design)
        Q_Less_P = fieldStarts - trimStarts.reshape(trimLen,1,2)
        denom = np.cross(trimVectors, fieldVectors.reshape(fieldLen,1,2))
        all_t = np.cross(Q_Less_P, trimVectors.reshape(trimLen,1,2)).transpose()/denom
        all_u = np.cross(Q_Less_P, fieldVectors).transpose()/denom
        
        for t, u, line in zip(all_t, all_u, self.design):
            if not self.trimOutline.lineOutsideBoundingBox(line):
                pointSet = set([line.start])
                t = t[(0 <= u) & (u <= 1) & (0 <= t) & (t <= 1)]

                pointSet |= set(Point(line.start.x + line.vector[c.X]*value,
                                    line.start.y+line.vector[c.Y]*value)
                                    for value in t)

                pointSet.add(line.end)
                pointList = sorted(list(pointSet))
                pointVectors = np.array([point.normalVector for point in pointList])
                
                """ Calculation for midPoints from here:
                http://stackoverflow.com/questions/23855976/middle-point-of-each-pair-of-an-numpy-array
                """
                midPoints = (pointVectors[1:] + pointVectors[:-1])/2.0
                for i in range(len(midPoints)):
                    if self.trimOutline.isInside(midPoints[i]):
                        self.lines.append(Line(pointList[i], pointList[i+1]))

                
                
                
                
                
                
                
                
                
        