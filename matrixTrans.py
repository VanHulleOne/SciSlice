# -*- coding: utf-8 -*-
"""
Created on Thu Jan 07 17:44:20 2016

A module to store operations related to matrix tranformations. 

@author: Luke
"""

import point as p
import line as l
import constants as c
import numpy
import math

def translateMatrix(shiftX, shiftY, shiftZ=0):
    transMatrix = numpy.identity(4)
    transMatrix[c.X][3] = shiftX
    transMatrix[c.Y][3] = shiftY
    transMatrix[c.Z][3] = shiftZ
    return transMatrix
    
def rotateMatrix(angle, point=None):
    if point is None:
        point = p.Point(0,0)
        
    toOrigin = translateMatrix(-point.x, -point.y)
    rotateMatrix = numpy.identity(4)
    rotateMatrix[c.X][0] = math.cos(angle)
    rotateMatrix[c.Y][0] = math.sin(angle)
    rotateMatrix[c.X][1] = -rotateMatrix[c.Y][0]
    rotateMatrix[c.Y][1] = rotateMatrix[c.X][0]
    transBack = translateMatrix(point.x, point.y)        
    transMatrix = numpy.dot(transBack, numpy.dot(rotateMatrix, toOrigin))
    return transMatrix
    
def mirrorMatrix(axis):
    transMatrix = numpy.identity(4)
    if type(axis) is l.Line:
        mList = []
        mList.append(translateMatrix(-axis.start.x, -axis.start.y)) #toOrigin
        angle = math.asin((axis.end.y-axis.start.y)/axis.length) #angle
#            print 'Angle: %.2f'%(angle/(2*math.pi)*360)
        mList.append(rotateMatrix(-angle)) #rotate to X-axis
        xMirror = numpy.identity(4)
        xMirror[c.Y][c.Y] = -1
        mList.append(xMirror) #mirror about X axis
        mList.append(rotateMatrix(angle)) #rotate back
        mList.append(translateMatrix(axis.start.x, axis.start.y)) #translate back         
        for matrix in mList:
            transMatrix = numpy.dot(matrix, transMatrix)
        return transMatrix
    if(axis == c.X):
            transMatrix[c.Y][c.Y] *= -1
    else:
        transMatrix[c.X][c.X] *= -1
    return transMatrix
    
def combineTransformations(matrixList):
    transMatrix = numpy.identity(4)
    for matrix in matrixList:
        transMatrix = numpy.dot(matrix, transMatrix)
    return transMatrix
        