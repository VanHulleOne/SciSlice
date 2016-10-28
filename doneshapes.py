# -*- coding: utf-8 -*-
"""
Created on Thu Dec 03 16:30:08 2015

Functions used to more quickly create commonly used shapes. Some of the functions
contain fully defined shapes while others allow parameter inputs to create a
custom outline. Type hints have been included to provide the user extra information
when entering parameters in the GUI.

@author: lvanhulle
"""

import math

import arc as a
import constants as c
from line import Line
from linegroup import LineGroup
from point import Point
from outline import Outline

def regularDogBone() ->Outline:    
    dogBone = Outline(None)
    dogBone.addLinesFromCoordinateList([[82.5, 0], [82.5, 9.5], [49.642, 9.5]])
    arc = a.Arc(Point(49.642, 9.5), Point(28.5, 6.5), c.CW, Point(28.5, 82.5), 20)
    dogBone.addLineGroup(arc)
    dogBone.addLinesFromCoordinateList([[28.5, 6.5], [0, 6.5]])
    dogBone.addLineGroup(dogBone.mirror(c.Y))
    dogBone.addLineGroup(dogBone.mirror(c.X))
    dogBone = dogBone.translate(82.5, 9.5)
    dogBone.finishOutline()
    return dogBone
    
def testSimpleDogBone() ->Outline:
    temp = Outline(None)
    temp.addLinesFromCoordinateList([[82.5,0],[82.5,9.5],[49.642, 9.5], [28.5,6.5],[0,6.5]])
    temp.addLineGroup(temp.mirror(c.Y))
    temp.addLineGroup(temp.mirror(c.X))
    temp = temp.translate(82.5, 9.5)
    temp.finishOutline()
    return temp
    
def wideDogBone() ->Outline:
    halfWidth = 5.0    
    wideDogBone = Outline(None)
    wideDogBone.addLinesFromCoordinateList([[82.5, 0], [82.5, 9.5 + halfWidth],
                                            [49.642, 9.5 + halfWidth]])
    wideArc = a.Arc(Point(49.642, 9.5 + halfWidth),
                    Point(28.5, 6.5 + halfWidth), c.CW,
                    Point(28.5, 82.5 + halfWidth), 20)
    wideDogBone.addLineGroup(wideArc)
    wideDogBone.addLinesFromCoordinateList([[28.5, 6.5 + halfWidth], [0, 6.5 + halfWidth]])
    wideDogBone.addLineGroup(wideDogBone.mirror(c.Y))
    wideDogBone.addLineGroup(wideDogBone.mirror(c.X))
    return wideDogBone.translate(82.5, 9.5 + halfWidth)
   
def rightGrip() ->Outline:
    outline = Outline(None)
    outline.addLinesFromCoordinateList([[82.5, 0], [82.5, 9.5], [49.642, 9.5]])
    arc = a.Arc(Point(49.642, 9.5), Point(28.5, 6.5), c.CW, Point(28.5, 82.5), 20)
    outline.addLineGroup(arc)
    outline.addLinesFromCoordinateList([[28.5, 6.5], [28.5, 0]])
    outline.addLineGroup(outline.mirror(c.X)) 
    return outline.translate(82.5, 9.5)

def leftGrip() ->Outline:
    outline = rightGrip()
    outline = outline.translate(-82.5, -9.5)
    outline = outline.mirror(c.Y)
    return outline.translate(82.5, 9.5)

def grips() ->Outline:
    outline = leftGrip()
    outline.addLineGroup(rightGrip())
    return outline

def center() ->Outline:
    outline = Outline(None)
    outline.addLinesFromCoordinateList([[28.5, 6.5], [-28.5, 6.5], [-28.5, -6.5],
                                      [28.5, -6.5], [28.5, 6.5]])
    return outline.translate(82.5, 9.5)
    
def squareWithHole() ->Outline:
    outline = Outline(None)
    outline.addLinesFromCoordinateList([[0,0], [50,0], [50,50], [0,50], [0,0]])
    circle = a.Arc(Point(35,25), Point(35,25), c.CW, Point(25,25))
    outline.addLineGroup(circle)
    return outline
    
def circle(centerX: float, centerY: float, radius: float) ->Outline:
    startPoint = Point(centerX+radius, centerY)
    center = Point(centerX, centerY)
    return Outline(a.Arc(startPoint, startPoint, c.CW, center))
    
def rect(lowerLeftX: float, lowerLeftY: float, width: float, height: float) ->Outline:
    rect = [Point(lowerLeftX, lowerLeftY)]
    rect.append(Point(lowerLeftX+width, lowerLeftY))
    rect.append(Point(lowerLeftX+width, lowerLeftY+height))
    rect.append(Point(lowerLeftX, lowerLeftY+height))
    rectLG = Outline(None)
    rectLG.addLinesFromPoints(rect)
    rectLG.closeShape()
    return rectLG
    
def polygon(centerX: float, centerY: float, radius: float, numCorners: int) ->Outline:
    angle = 1.5*math.pi
    points = []
    incAngle = 2*math.pi/numCorners
    for i in range(numCorners):
        x = math.cos(angle+incAngle*i)*radius+centerX
        y = math.sin(angle+incAngle*i)*radius+centerY
        points.append(Point(x,y))
    poly = Outline(None)
    poly.addLinesFromPoints(points)
    poly.closeShape()
    poly = poly.rotate(incAngle/2.0, Point(centerX, centerY))
    return poly
        
def lineField(space: float, length: float, height: float) ->LineGroup:
    lines = []
    currHeight = 0
    while currHeight < height:
        lines.append(Line(Point(0,currHeight), Point(length,currHeight)))
        currHeight += space
    group = LineGroup()
    group.lines = lines
    group.minX = 0
    group.minY = 0
    group.maxX = length
    group.maxY = currHeight-space
    return group
    

def hexField(side: float, space: float, length: float, height: float) -> LineGroup:
    baseLine = LineGroup(None)
    baseLine.addLinesFromCoordinateList([[0,0], [side, 0],
             [side+math.cos(math.pi/4)*side, math.cos(math.pi/4)*side],
              [side*2+math.cos(math.pi/4)*side, math.cos(math.pi/4)*side],
               [2*(side+math.cos(math.pi/4)*side), 0]])
    fullLine = LineGroup(baseLine)
    
    while fullLine.maxX - fullLine.minX < length:
        baseLine = baseLine.translate(baseLine.maxX - baseLine.minX, 0)
        fullLine.addLineGroup(baseLine)
        
    mirrorLine = LineGroup(fullLine)
    mirrorLine = mirrorLine.mirror(c.X)
    mirrorLine = mirrorLine.translate(0, -space)
    fullLine.addLineGroup(mirrorLine)
    field = LineGroup(fullLine)
    
    while field.maxY - field.minY < height:
        fullLine = fullLine.translate(0, fullLine.maxY-fullLine.minY+space)
        field.addLineGroup(fullLine)
    return field
    
def straightLines()  -> LineGroup:
    return lineField # return the lifeField method so the appropriate parameters
                        # can be called to efficiently generate the line field
    
def noInfill() -> LineGroup:
    return LineGroup()
    
