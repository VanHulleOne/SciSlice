# -*- coding: utf-8 -*-
"""
Created on Wed Oct 28 10:16:22 2015

@author: lvanhulle
"""
import Point as p
#import InFill as infill
import Shape as s
import Line as l
import arc as a
import math
import numpy
import copy
import gcode as gc
import parameters as pr
from parameters import constants as c
import InFill as InF
from itertools import islice
import LineGroup as lg
import doneShapes as ds
import itertools
from operator import itemgetter
import time
import matrixTrans as mt

CW = -1
CCW = 1

#X, Y = 0, 1
#
arc = a.Arc(p.Point(49.642, 9.5), p.Point(28.5, 6.5), CW, p.Point(28.5, 82.5), 20)
#
p1 = p.Point(-82.500, -9.500, 0)
p2 = p.Point(74, -101.5052)
p3 = p.Point(74, 101.5052)
p4 = p.Point(-82.501, -9.5)
p5 = p.Point(3,3.0001)
p6 = p.Point(0,0)
p7 = p.Point(4,0)
p8 = p.Point(4,4)
p9 = p.Point(0,4)
p10 = p.Point(3,12)
p11 = p.Point(0,5)

tLine = l.Line(p2, p3)

s1 = s.Shape(None)
s1.addLinesFromCoordinateList([[0,0],[0,19],[74,19],[74,0]])
s1 = s1 + s1.mirror(c.X)

s1.finishOutline()
print s1
s1Filled = InF.InFill(s1, 1, 90)
__
    
