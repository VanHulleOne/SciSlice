# -*- coding: utf-8 -*-
"""
Created on Thu Dec 03 16:30:08 2015

Functions used to more quickly create commonly used shapes. Some of the functions
contain fully defined shapes while others allow parameter inputs to create a
custom shape.

@author: lvanhulle
"""

import Shape as s
import LineGroup as lg
import arc as a
import Point as p
import constants as c
import math
import Line as l

def regularDogBone():    
    dogBone = s.Shape(None)
    dogBone.addLinesFromCoordinateList([[82.5, 0], [82.5, 9.5], [49.642, 9.5]])
    arc = a.Arc(p.Point(49.642, 9.5), p.Point(28.5, 6.5), c.CW, p.Point(28.5, 82.5), 20)
    dogBone.addLineGroup(arc)
    dogBone.addLinesFromCoordinateList([[28.5, 6.5], [0, 6.5]])
    dogBone.addLineGroup(dogBone.mirror(c.Y))
    dogBone.addLineGroup(dogBone.mirror(c.X))
    dogBone = dogBone.translate(82.5, 9.5)
    dogBone.finishOutline()
    return dogBone
    
def testSimpleDogBone():
    temp = s.Shape(None)
    temp.addLinesFromCoordinateList([[82.5,0],[82.5,9.5],[49.642, 9.5], [28.5,6.5],[0,6.5]])
    temp.addLineGroup(temp.mirror(c.Y))
    temp.addLineGroup(temp.mirror(c.X))
    temp = temp.translate(82.5, 9.5)
    temp.finishOutline()
    return temp
    
def wideDogBone():
    halfWidth = 5.0    
    wideDogBone = s.Shape(None)
    wideDogBone.addLinesFromCoordinateList([[82.5, 0], [82.5, 9.5 + halfWidth],
                                            [49.642, 9.5 + halfWidth]])
    wideArc = a.Arc(p.Point(49.642, 9.5 + halfWidth),
                    p.Point(28.5, 6.5 + halfWidth), c.CW,
                    p.Point(28.5, 82.5 + halfWidth), 20)
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
    
def rect(lowerLeftX, lowerLeftY, width, height):
    rect = [p.Point(lowerLeftX, lowerLeftY)]
    rect.append(p.Point(lowerLeftX+width, lowerLeftY))
    rect.append(p.Point(lowerLeftX+width, lowerLeftY+height))
    rect.append(p.Point(lowerLeftX, lowerLeftY+height))
    rectLG = s.Shape(None)
    rectLG.addLinesFromPoints(rect)
    rectLG.closeShape()
    return rectLG
    
def polygon(centerX, centerY, radius, numCorners):
    angle = 1.5*math.pi
    points = []
    incAngle = 2*math.pi/numCorners
    for i in range(numCorners):
        x = math.cos(angle+incAngle*i)*radius+centerX
        y = math.sin(angle+incAngle*i)*radius+centerY
        points.append(p.Point(x,y))
    poly = s.Shape(None)
    poly.addLinesFromPoints(points)
    poly.closeShape()
    poly = poly.rotate(incAngle/2.0, p.Point(centerX, centerY))
    return poly
        
def lineField(space, length, height):
    lines = []
    currHeight = 0
    while currHeight < height:
        lines.append(l.Line(p.Point(0,currHeight), p.Point(length,currHeight)))
        currHeight += space
    group = lg.LineGroup()
    group.lines = lines
    group.minX = 0
    group.minY = 0
    group.maxX = length
    group.maxY = currHeight-space
    return group
    

def hexField(side, space, length, height):
    baseLine = lg.LineGroup(None)
    baseLine.addLinesFromCoordinateList([[0,0], [side, 0],
             [side+math.cos(math.pi/4)*side, math.cos(math.pi/4)*side],
              [side*2+math.cos(math.pi/4)*side, math.cos(math.pi/4)*side],
               [2*(side+math.cos(math.pi/4)*side), 0]])
    fullLine = lg.LineGroup(baseLine)
    
    while fullLine.maxX - fullLine.minX < length:
        baseLine = baseLine.translate(baseLine.maxX - baseLine.minX, 0)
        fullLine.addLineGroup(baseLine)
        
    mirrorLine = lg.LineGroup(fullLine)
    mirrorLine = mirrorLine.mirror(c.X)
    mirrorLine = mirrorLine.translate(0, -space)
    fullLine.addLineGroup(mirrorLine)
    field = lg.LineGroup(fullLine)
    
    while field.maxY - field.minY < height:
        fullLine = fullLine.translate(0, fullLine.maxY-fullLine.minY+space)
        field.addLineGroup(fullLine)
    return field
    