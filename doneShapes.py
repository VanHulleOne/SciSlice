# -*- coding: utf-8 -*-
"""
Created on Thu Dec 03 16:30:08 2015

@author: lvanhulle
"""

import Shape as s
import arc as a
import Point as p
from parameters import constants as c

    
def regularDogBone():    
    dogBone = s.Shape(None)
    dogBone.addLinesFromCoordinateList([[82.5, 0], [82.5, 9.5], [49.642, 9.5]])
    arc = a.Arc(p.Point(49.642, 9.5), p.Point(28.5, 6.5), c.CW, p.Point(28.5, 82.5), 20)
    dogBone.addLineGroup(arc)
    dogBone.addLinesFromCoordinateList([[28.5, 6.5], [0, 6.5]])
    dogBone.addLineGroup(dogBone.mirror(c.Y))
    dogBone.addLineGroup(dogBone.mirror(c.X))
    return dogBone.translate(82.5, 9.5)

def wideDogBone():
    halfWidth = 5.0    
    wideDogBone = s.Shape(None)
    wideDogBone.addLinesFromCoordinateList([[82.5, 0], [82.5, 9.5 + halfWidth], [49.642, 9.5 + halfWidth]])
    wideArc = a.Arc(p.Point(49.642, 9.5 + halfWidth), p.Point(28.5, 6.5 + halfWidth), c.CW, p.Point(28.5, 82.5 + halfWidth), 20)
    wideDogBone.addLineGroup(wideArc)
    wideDogBone.addLinesFromCoordinateList([[28.5, 6.5 + halfWidth], [0, 6.5 + halfWidth]])
    wideDogBone.addLineGroup(wideDogBone.mirror(c.Y))
    wideDogBone.addLineGroup(wideDogBone.mirror(c.X))
    return wideDogBone.translate(82.5, 9.5 + halfWidth)
    
def rightGrip():
    shape = s.Shape(None)
    shape.addLinesFromCoordinateList([[82.5, 0], [82.5, 9.5], [49.642, 9.5]])
    arc = a.Arc(p.Point(49.642, 9.5), p.Point(28.5, 6.5), c.CW, p.Point(28.5, 82.5), 20)
    shape.addLineGroup(arc)
    shape.addLinesFromCoordinateList([[28.5, 6.5], [28.5, 0]])
    shape.addLineGroup(shape.mirror(c.X))
    return shape.translate(82.5, 9.5)
    
def leftGrip():
    shape = rightGrip()
    shape = shape.translate(-82.5, -9.5)
    shape = shape.mirror(c.Y)
    return shape.translate(82.5, 9.5)
    
def grips():
    shape = leftGrip()
    shape.addLineGroup(rightGrip())
    return shape

def center():
    shape = s.Shape(None)
    shape.addLinesFromCoordinateList([[28.5, 6.5], [-28.5, 6.5], [-28.5, -6.5],
                                      [28.5, -6.5], [28.5, 6.5]])
    return shape.translate(82.5, 9.5)
    
def squareWithHole():
    shape = s.Shape(None)
    shape.addLinesFromCoordinateList([[0,0], [50,0], [50,50], [0,50], [0,0]])
    circle = a.Arc(p.Point(35,25), p.Point(35,25), c.CW, p.Point(25,25))
    shape.addLineGroup(circle)
    return shape
    
def circle(centerX, centerY, radius):
    startPoint = p.Point(centerX+radius, centerY)
    center = p.Point(centerX, centerY)
    return s.Shape(a.Arc(startPoint, startPoint, c.CW, center))