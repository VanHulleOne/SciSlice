# -*- coding: utf-8 -*-
"""
Created on Wed Oct 28 10:16:22 2015

@author: lvanhulle
"""
import Point as p
#import InFill as infill
#import Shape as s
import Line as l
#import arc as a
import math
import numpy as np
import copy
import gcode as gc
import parameters as pr
import constants as c
import InFill as InF
from itertools import islice
import LineGroup as lg
import doneShapes as ds
import itertools
from operator import itemgetter
import time
import timeit
import matrixTrans as mt
import random
import bisect
import collections as col
from collections import namedtuple


p1 = p.Point(2.073, 0.0806)
p2 = p.Point(2.1512, 0.0323)
p3 = p.Point(2.144081, 0.0389)
p4 = p.Point(2.0251, 0.1612)
p5 = p.Point(3,3.0001)
p6 = p.Point(-1,0)
p7 = p.Point(4,0)
p8 = p.Point(4,4)
p9 = p.Point(0,4)
p10 = p.Point(3,12)
p11 = p.Point(0,5)
p12 = p.Point(0,1)
p13 = p.Point(0,-1)
p14 = p.Point(0.0, 0,0)
p15 = p.Point(8.0, 0.0)
p16 = p.Point(10.0, 0.0)
p17 = p.Point(60.326, 19.517)
p18 = p.Point(61.100, 19.488)
p19 = p.Point(61.100, 19.512)
p20 = p.Point(60.326, 19.483)
p21 = p.Point(50.326152, 9.483299)
p22 = p.Point(51.550318, 9.528728)
p23 = p.Point(51.550318, 9.471272)
p24 = p.Point(50.326152, 9.516701)

points = [p1,p2,p3,p4,p5,p6,p7,p8,p9,p10,p11]

lines = [l.Line(points[i], points[i+1]) for i in range(len(points)-1)]


#d1 = ds.rect(0,0,10,10)
#sub1 = s.Shape()
#sub1.addLinesFromCoordinateList([[5,1],[4,5],[5,9],[6,5],[5,1]])
#sub1 = sub1.translate(-0.1,0)
#sub1.finishOutline()
#d1.addInternalShape(sub1)
#print('d1:')
#d1.finishOutline()

#d1 = ds.simpleDogBone()

#print('R1')
#r1 = ds.squareWithHole()
##r1 = ds.rect(0,0,10,20)
#print('R2')
#r2 = r1.offset(0.5, c.INSIDE)
#print('R3')
#r3 = r1.newOffset(0.5, c.INSIDE)

#def printG(shape):
#    for line in shape:
#        print(*line, sep='\n')
#
#def offsets(shape, num, dist=1):
#    print('G90 G1')
#    for i in range(num+1):
#        print('T',i+1,'\nM6',sep='')
#        printG(shape)
#        shape = shape.newOffset(dist, c.INSIDE)
#    
#in1 = ds.lineField(0.5, 185, 185)

""" An example of how to do other infills. """  
#currOutline = ds.rect(0,0,15,250)
#filledList = []
#
#for shellNumber in range(pr.numShells):
#    filledList.append(currOutline)
#    currOutline = currOutline.offset(pr.pathWidth, c.INSIDE)
#
##pattern = lg.LineGroup()
##pattern.addLinesFromCoordinateList([[0,0],[2,2],[4,0]])
#infill = InF.InFill(currOutline, pr.pathWidth, pr.infillAngleDegrees)#, pattern)
#
#filledList.append(infill)
    
    