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

CW = -1
CCW = 1

arc = a.Arc(p.Point(49.642, 9.5), p.Point(28.5, 6.5), CW, p.Point(28.5, 82.5), 20)

p1 = p.Point(0,0)
p2 = p.Point(0,4)
p3 = p.Point(4,2)
p4 = p.Point(2,2)

line1 = l.Line(p1, p2)
line2 = l.Line(p3, p4)

test, p = line1.segmentsIntersect(line2)
#print test
