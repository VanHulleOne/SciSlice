# -*- coding: utf-8 -*-
"""
Created on Mon Sep 21 09:51:36 2015

@author: lvanhulle
"""
import math
import numpy
import operator
import Point as p
import Line as l
import Shape as s
import LineGroup as LG
import InFill as InF
import arc as a
import figura as fg
import parameters as pr
import gcode as gc

#fifferShape = [[0.0,0.0],[10.0,0.0],[18.1212,10.0],[22.9353,20.0],[26.1426,30.0],
#               [28.292,40.0],[29.6285,50.0],[30.2716,60.0],[30.2716,85.0],
#                [25.7716,85.0]]

def getLineAngle(p1, p2):
    angle = math.atan2((p2[Y]-p1[Y]), (p2[X] - p1[X]))
    return angle if angle >= 0 else angle + 2*math.pi

#TODO: change the offset method to make the offset lines parallel with the exhisting lines   
def offset(shape, dist, side):
    """
    Given an input shape, distance, and if you want inside or outside, this
    method will return a new shape that is offset from the original. Currently
    it measures the offset distance along an angular bisector of each corner
    but this should be changed to make it calculate from a line normal to the
    exhisting line.
    """
    tempShape = [[]]
    line1Angle = getLineAngle(shape[0], shape[len(shape)-2])
    line2Angle = getLineAngle(shape[0], shape[1])
    halfAngle1 = (line1Angle + line2Angle)/2
    halfAngle2 = halfAngle1 + math.pi
    try1 = [shape[0][X] + dist*math.cos(halfAngle1), shape[0][Y] + dist*math.sin(halfAngle1)]
    try2 = [shape[0][X] + dist*math.cos(halfAngle2), shape[0][Y] + dist*math.sin(halfAngle2)]
    firstPoint = try1 if(isInside(try1, shape) == side) else try2
#    print 'Try1: ', try1, ' side: ', side, ' firstPoint: ', firstPoint
    tempShape[0] = firstPoint
    
    for i in range(1, len(shape)-1):
        line1Angle = getLineAngle(shape[i], shape[i-1])
        line2Angle = getLineAngle(shape[i], shape[i+1])
        halfAngle1 = (line1Angle + line2Angle)/2
        halfAngle2 = halfAngle1 + math.pi
        try1 = [shape[i][X] + dist*math.cos(halfAngle1), shape[i][Y] + dist*math.sin(halfAngle1)]
        try2 = [shape[i][X] + dist*math.cos(halfAngle2), shape[i][Y] + dist*math.sin(halfAngle2)]
        if(isInside(try1, shape)):
            tempShape.append(try1)
        elif(isInside(try2, shape)):
            tempShape.append(try2)              
                
    tempShape.append(firstPoint)
    return tempShape

dogBone = s.Shape(None)
dogBone.addLinesFromCoordinateList([[82.5, 0], [82.5, 9.5], [49.642, 9.5]])
arc = a.Arc(p.Point(49.642, 9.5), p.Point(28.5, 6.5), CW, p.Point(28.5, 82.5), 20)
dogBone.addLineGroup(arc)
dogBone.addLinesFromCoordinateList([[28.5, 6.5], [0, 6.5]])
dogBone.addLineGroup(dogBone.mirror(Y))
dogBone.addLineGroup(dogBone.mirror(X))

infill = InF.InFill(dogBone)
fig = fg.Figura(infill)

#print 'dogBone'
#print str(dogBone)
#print 'Fig:'
#print fig.gcode

print '\nGenerating File, please wait...\n'

f = open(pr.outputSubDirectory+'\\'+pr.outputFileName, 'w')
f.write(gc.startGcode())
f.write(fig.gcode)
f.write(gc.endGcode())

f.close()

print 'Dong writting: ' + pr.outputFileName
