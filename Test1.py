# -*- coding: utf-8 -*-
"""
Created on Wed Oct 28 10:16:22 2015

@author: lvanhulle
"""
from point import Point
from infill import Infill
from outline import Outline
from line import Line
#import arc as a
import math
import numpy as np
import copy
import gcode as gc
import parameters as pr
import constants as c
from infill import Infill
from itertools import islice
import linegroup as lg
import doneshapes as ds
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
import inspect


p1 = Point(2.073, 0.0806)
p2 = Point(2.1512, 0.0323)
p3 = Point(2.144081, 0.0389)
p4 = Point(2.0251, 0.1612)
p5 = Point(3,3.0001)
p6 = Point(-1,0)
p7 = Point(4,0)
p8 = Point(4,4)
p9 = Point(0,4)
p10 = Point(3,12)
p11 = Point(0,5)
p12 = Point(0,1)
p13 = Point(0,-1)
p14 = Point(0.0, 0,0)
p15 = Point(8.0, 0.0)
p16 = Point(10.0, 0.0)
p17 = Point(60.326, 19.517)
p18 = Point(61.100, 19.488)
p19 = Point(61.100, 19.512)
p20 = Point(60.326, 19.483)
p21 = Point(50.326152, 9.483299)
p22 = Point(51.550318, 9.528728)
p23 = Point(51.550318, 9.471272)
p24 = Point(50.326152, 9.516701)

points = [p1,p2,p3,p4,p5,p6,p7,p8,p9,p10,p11]

lines = [Line(points[i], points[i+1]) for i in range(len(points)-1)]

sq = ds.squareWithHole()




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
    
    