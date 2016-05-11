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
import numpy as np
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
import timeit
import matrixTrans as mt
import random
import bisect
import collections as col

CW = -1
CCW = 1

#X, Y = 0, 1
#
arc = a.Arc(p.Point(49.642, 9.5), p.Point(28.5, 6.5), CW, p.Point(28.5, 82.5), 20)
#
p1 = p.Point(2.073, 0.0806)
p2 = p.Point(2.1512, 0.0323)
p3 = p.Point(2.144081, 0.0389)
p4 = p.Point(2.0251, 0.1612)
p5 = p.Point(3,3.0001)
p6 = p.Point(0,0)
p7 = p.Point(4,0)
p8 = p.Point(4,4)
p9 = p.Point(0,4)
p10 = p.Point(3,12)
p11 = p.Point(0,5)


def endPoints(points):
    end = []
    current = [] 
    num = 0
    for cur_point in points:
        num+=1
        if(num==1): 
            first = cur_point 
        previous = current 
        current = [] 
        previous.append(cur_point) 
        current.append(cur_point) 
        if(num>1): 
            end.append(previous) 
    current.append(first)
    end.append(current) 
    return end
    
def pairwise(l1):
    l1Iter = iter(l1)
    first = pre = next(l1Iter)
    result = []
    for curr in l1Iter:
        result.append([pre, curr])
        pre = curr
    result.append([pre, first])
    return result
    
def pairwise_gen(l1):
    l1Iter = iter(l1)
    first = pre = next(l1Iter)
    for curr in l1Iter:
       yield [pre, curr]
       pre = curr
    yield [pre, first]
    
    
    
NT = col.namedtuple('NT', ['X', 'Y', 'Z'])

    
# https://en.wikipedia.org/wiki/Pairing_function#Cantor_pairing_function
    
def cantorPairing(l1):
    if len(l1) == 1:
        return l1[0]
    k2 = l1[-1]
    k1 = cantorPairing(l1[:-1])
    return (0.5*(k1+k2)*(k1+k2+1)+k2)

    
    
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
    
    