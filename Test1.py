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
from parameters import constants as const
import InFill as inf

CW = -1
CCW = 1

X, Y = 0, 1

arc = a.Arc(p.Point(49.642, 9.5), p.Point(28.5, 6.5), CW, p.Point(28.5, 82.5), 20)

p1 = p.Point(-82.500, -9.500, 0)
p2 = p.Point(161.361, 111.157)
p3 = p.Point(28.5, 6.5)
p4 = p.Point(-82.5, -9.5)
p5 = p.Point(2,2.00001)
p6 = p.Point(2,2)

se = set([p1, p2, p5, p6])

print p1 == p4

s1 = s.Shape(None)
s1.addLinesFromCoordinateList([[0,-6.5], [10,-6.5], [10,6.5], [0,6.5], [-10,6.5], [-10,-6.5], [0, -6.5]])
s1.closeShape()

#print s1.isInside(p1)
#
#line1 = l.Line(p2, p1)
#line2 = l.Line(p3, p4)
#
#result, point = line2.segmentsIntersect(line1)
#
#print str(result) + ' ' + str(point)