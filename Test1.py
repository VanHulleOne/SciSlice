# -*- coding: utf-8 -*-
"""
Created on Wed Oct 28 10:16:22 2015

@author: lvanhulle
"""
import Point as p
import Line as l

point1 = p.Point(1,1)
point2 = p.Point(1,5)

line1 = l.Line(point2, point1)

line1.printBoudningBox()
