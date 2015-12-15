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
from parameters import constants as c
import InFill as inf
from itertools import islice
import LineGroup as lg
import doneShapes as ds

CW = -1
CCW = 1

X, Y = 0, 1

arc = a.Arc(p.Point(49.642, 9.5), p.Point(28.5, 6.5), CW, p.Point(28.5, 82.5), 20)

p1 = p.Point(-82.500, -9.500, 0)
p2 = p.Point(161.361, 111.157)
p3 = p.Point(28.5, 6.5)
p4 = p.Point(-82.501, -9.5)
p5 = p.Point(3,3.0001)
p6 = p.Point(3,4)
p7 = p.Point(5,6)
p8 = p.Point(7,8)
p9 = p.Point(5,10)
p10 = p.Point(3,12)

def nrVariables_gen(inList):
    varGens = []
    for sublist in inList:
        varGens.append(variable_gen(sublist))
        
    for i in range(len(max(inList, key=len))):
        tempList = []
        for VG in varGens:
            tempList.append(next(VG))
        yield tempList
    
def variable_gen(inList):
    while True:
        for var in inList:
            yield var

l1 = ['a','b','c']
l2 = [1,2]
l3 = ['Z','Y','X','W']
l4 = [47, 46, 45, 44, 43, 42]
l5 = ['Yes', 'No', 'Maybe']
l6 = 'Hello'  
       
nrGen = nrVariables_gen([l1,l2,l3,l4,l5,l6])

for sublist in nrGen:
    print sublist


#aHole = a.Arc(p.Point(4,0), p.Point(4,0), c.CW, p.Point(0,0))
#print isinstance(aHole, lg.LineGroup)

#def fib():
#    prev, cur = 0, 1
#    while True:
#        yield cur
#        prev, cur = cur, cur + prev
#        
#f = fib()



#se = set([p1, p2, p5, p6])
#
#l1 = l.Line(p1, p2)
#
#print l1
#l1.flip()
#print l1
#
#s1 = s.Shape(None)
#s1.addLinesFromCoordinateList([[0,-6.5], [10,-6.5], [10,6.5], [0,6.5], [-10,6.5], [-10,-6.5], [0, -6.5]])
#s1.closeShape()

