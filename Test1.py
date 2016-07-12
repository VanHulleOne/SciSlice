# -*- coding: utf-8 -*-
"""
Created on Wed Oct 28 10:16:22 2015

@author: lvanhulle
"""
import Point as p
import InFill as infill
import Shape as s
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
import sys
import trimesh
from stl import mesh
from shapely.geometry.polygon import LinearRing, Polygon
from shapely.geometry import *#MultiPolygon
import matplotlib.pyplot as plt
from shapely.ops import cascaded_union
from matplotlib import animation


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

COMMON = 0
PART = 1
LAYER = 2
FILE = 3
PRINT = 4

Menu = namedtuple('Menu', 'name group')
menus = [
        Menu('Common', COMMON),
        Menu('Part', PART),
        Menu('Layer', LAYER),
        Menu('File', FILE),
        Menu('Print', PRINT)
        ]

Par = namedtuple('Parameter', 'label type groups')
parameters = [
            Par('stl_file', str, (COMMON, PART)),
            Par('solidityRatio', float, (COMMON, PART)),
            Par('shiftX', float, (COMMON, PART)),
            Par('shiftY', float, (COMMON, PART)),
            Par('firstLayerShiftZ', float, (PART,)),
            Par('numLayers', int, (COMMON, PART)),
            Par('pattern', None, (PART,)),
            Par('designType', int, (PART,)),
            Par('infillAngleDegrees', float, (COMMON, LAYER)),
            Par('pathWidth', float, (LAYER,)),
            Par('layerHeight', float, (LAYER,)),
            Par('infillShiftX', float, (LAYER,)),
            Par('infillShiftY', float, (LAYER,)),
            Par('numShells', int, (COMMON, LAYER)),
            Par('trimAdjust', float, (LAYER,)),
            Par('start_Gcode_FileName', str, (FILE,)),
            Par('end_Gcode_FileName', str, (FILE,)),
            Par('outputFileName', str, (COMMON, FILE)),
            Par('bed_temp', int, (COMMON, PRINT)),
            Par('extruder_temp', int, (COMMON, PRINT)),
            ]

fields = []
for menu in menus:
    fields.append([par for par in parameters if menu.group in par.groups])
    

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
    
    