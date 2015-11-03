# -*- coding: utf-8 -*-
"""
Created on Wed Oct 28 10:16:22 2015

@author: lvanhulle
"""
import Point as p
#import InFill as infill
import Shape as s
import Line as l

p1 = p.Point(0,0)
p2 = p.Point(1,1)
p3 = p.Point(5,0)

line1 = l.Line(p1, p2)
line2 = l.Line(p2, p3)


s1 = s.Shape(None)
s1.addLine(line1)
s1.addLine(line2)

print s1
