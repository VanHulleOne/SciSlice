# -*- coding: utf-8 -*-
"""
Created on Wed Oct 28 10:16:22 2015

@author: lvanhulle
"""
import Point as p
import InFill as infill
import Shape as s
import Line as l
#import arc as a
import math
import numpy as np
import copy
import gcode as gc
import parameters as pr
import constants as c
import InFill as InF
from itertools import islice
import LineGroup as lg
import doneShapes as ds
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


p1 = p.Point(2.073, 0.0806)
p2 = p.Point(2.1512, 0.0323)
p3 = p.Point(2.144081, 0.0389)
p4 = p.Point(2.0251, 0.1612)
p5 = p.Point(3,3.0001)
p6 = p.Point(-1,0)
p7 = p.Point(4,0)
p8 = p.Point(4,4)
p9 = p.Point(0,4)
p10 = p.Point(3,12)
p11 = p.Point(0,5)
p12 = p.Point(0,1)
p13 = p.Point(0,-1)
p14 = p.Point(0.0, 0,0)
p15 = p.Point(8.0, 0.0)
p16 = p.Point(10.0, 0.0)
p17 = p.Point(60.326, 19.517)
p18 = p.Point(61.100, 19.488)
p19 = p.Point(61.100, 19.512)
p20 = p.Point(60.326, 19.483)
p21 = p.Point(50.326152, 9.483299)
p22 = p.Point(51.550318, 9.528728)
p23 = p.Point(51.550318, 9.471272)
p24 = p.Point(50.326152, 9.516701)

points = [p1,p2,p3,p4,p5,p6,p7,p8,p9,p10,p11]

lines = [l.Line(points[i], points[i+1]) for i in range(len(points)-1)]

mesh1 = trimesh.load_mesh('Arch3.stl')
print(mesh1.area)
sec = mesh1.section(plane_origin=[0,0,37],plane_normal=[0,0,1])
lr0 = LinearRing(sec.discrete[0])

colors = [i + '-' for i in 'bgrcmyk']
colorCycle = itertools.cycle(colors)
po = [Polygon(i) for i in sec.discrete]

def plotPoly(poly, style='r-'):
    n = np.array(poly.exterior.coords)
    plt.plot(n[:,0], n[:,1], style)
    for inter in poly.interiors:
        n = np.array(inter.coords)
        plt.plot(n[:,0], n[:,1], style)

def multiPlot(mlt, style=None):
    if style is None:
        style = next(colorCycle)
    try:
        for poly in mlt:
            try:
                plotPoly(poly, style)
            except Exception:
                for pol in poly: 
                    plotPoly(pol, style)
    except Exception:
        plotPoly(mlt, style)
        
class PolySide:
    def __init__(self, poly, level):
        self.poly = poly
        self.level = level
        self.isFeature = not level%2
    def contains(self, other):
        return self.poly.contains(other)
    def plot(self):
        n = np.array(self.poly.exterior.coords)
        plt.plot(n[:,0], n[:,1], 'r-' if self.isFeature else 'b-')

    def offset(self, dist, side):
        if dist == 0:
            return PolySide(self.poly, self.level)
        if dist < 0:
            raise Exception('Offset distance must be >=0')
        if (side == c.OUTSIDE and self.isFeature) or (side == c.INSIDE and not self.isFeature):
            return PolySide(self.poly.buffer(dist), self.level)
        try:
            buffPoly = self.poly.exterior.buffer(dist)
            if len(buffPoly.interiors) > 1:
                inPoly = cascaded_union([Polygon(i) for i in buffPoly.interiors])            
            else:
                inPoly = Polygon(buffPoly.interiors[0])
            return PolySide(inPoly, self.level)
        except Exception:
            return None
    
    def brim(self, dist):
        return self.offset(dist, c.OUTSIDE)
    
    def shell(self, dist):
        return self.offset(dist, c.INSIDE)        

def IO2(polies):
    polySides = []
    polies = sorted(polies, key = lambda x: x.area, reverse=True)
    def io(thisPoly, index=0):
        while index < len(polies):
            if thisPoly.contains(polies[index]):
                new = PolySide(polies[index], thisPoly.level+1)
                polySides.append(new)
                polies.pop(index)
                io(new, index)
            else:
                index += 1
    while polies:
        first = PolySide(polies.pop(0), 0)
        polySides.append(first)
        io(first)
    return polySides
hs = []
fs = []
#features = []
def re_union(polies):
    final = None
    for ps in polies:
        if final is None:
            if ps.isFeature:
                final = ps.poly
        elif ps.isFeature:
            final = final.union(ps.poly)
        else:
            final = final.difference(ps.poly)
    return final

def shellRun(outerShell):
    io = IO2(outerShell)
    step = 0.25
    run = True
    i = 1
    while i <20:
        run = re_union(filter(None, (j.offset(step*i, c.OUTSIDE) for j in io)))
        yield run
        i += 1

fig = plt.figure()
ax = plt.axes(xlim=(-1,100), ylim=(-1,25))
lines = [ax.plot([], [], lw=1)[0] for _ in range(150)]

def layer(zHeight):
#    zHeight = 37/0.2
    step = 0.2
    print('Z height++: ', zHeight*step)
    sec = mesh1.section(plane_origin=[0,0,zHeight*step],plane_normal=[0,0,1])
    pl = [Polygon(i) for i in sec.discrete]
    xy = []
    for multi in shellRun(pl):        
        try:
            for poly in multi:
                xy.append(np.array(poly.exterior.coords))
                try:
                    for inner in poly.interiors:
                        xy.append(np.array(inner.coords))
                except Exception:
                    print('No interiors')
        except Exception:
            print('Not a multi')
            try:
                xy.append(np.array(multi.exterior.coords))
                for inner in multi.interiors:
                    xy.append(np.array(inner.coords))
                print('Just a polygon')
            except Exception:
                print('double fail')

    for i in range(150):
        if i < len(xy):
            lines[i].set_data(xy[i][:,0], xy[i][:,1])
        else:
            lines[i].set_data([],[])
    return lines



def init():
    for line in lines:
        line.set_data([],[])
    return lines
    
    

ani = animation.FuncAnimation(fig, layer, init_func=init, frames = 350, blit=True, interval=0)
plt.show()
#d1 = ds.rect(0,0,10,10)
#sub1 = s.Shape()
#sub1.addLinesFromCoordinateList([[5,1],[4,5],[5,9],[6,5],[5,1]])
#sub1 = sub1.translate(-0.1,0)
#sub1.finishOutline()
#d1.addInternalShape(sub1)
#print('d1:')
#d1.finishOutline()

#d1 = ds.simpleDogBone()

#print('R1')
#r1 = ds.squareWithHole()
##r1 = ds.rect(0,0,10,20)
#print('R2')
#r2 = r1.offset(0.5, c.INSIDE)
#print('R3')
#r3 = r1.newOffset(0.5, c.INSIDE)

#def printG(shape):
#    for line in shape:
#        print(*line, sep='\n')
#
#def offsets(shape, num, dist=1):
#    print('G90 G1')
#    for i in range(num+1):
#        print('T',i+1,'\nM6',sep='')
#        printG(shape)
#        shape = shape.newOffset(dist, c.INSIDE)
#    
#in1 = ds.lineField(0.5, 185, 185)

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
    
    