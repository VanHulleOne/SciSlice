# -*- coding: utf-8 -*-
"""
Created on Wed Oct 28 10:16:22 2015

@author: lvanhulle
"""
import Point as p
import numpy

point1 = p.Point(0,0)
point2 = p.Point(0,2)
point3 = p.Point(2,0)

def getArea(p1, p2, p3):
    matrix = [p1.getNormalVector(), p2.getNormalVector(), p3.getNormalVector()]
    matrix = numpy.rot90(matrix)
    return abs(numpy.linalg.det(matrix))

print getArea(point2, point1, point3)