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
import itertools

CW = -1
CCW = 1

#X, Y = 0, 1
#
#arc = a.Arc(p.Point(49.642, 9.5), p.Point(28.5, 6.5), CW, p.Point(28.5, 82.5), 20)
#
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

ds1 = ds.DoneShapes()
s1 = ds1.regularDogBone
s2 = ds1.wideDogBone

<<<<<<< HEAD
def min_gen(inList, seed):
    while len(inList) > 0:
        lowest, dist = min(((val, abs(val - seed)) for val in inList), key=itemgetter(1))
        try:
            used, seed = yield lowest, dist 
        except:
            pass
        else:
            if used:
                inList.remove(lowest)


l1 = [7,4,1, 99, 100]
l2 = [2,5,6,10,-127, 96]
l3 = [3,9,8,1, 98]
l0 = [0.5, 1.5, 2.1, 7.8, 3.3, 1.0]
l4 = [l1,l2,l3, l0]

#g = min_gen(l3, 0)
#print next(g)
#print g.send((True,0))
#print next(g)

genList = []           
for sub in l4:
    genList.append(min_gen(sub, 98))
 
while len(genList) > 0:
    results = [next(gen) for gen in genList]
    index = min(enumerate(result[1] for result in results), key=itemgetter(1))[0]
    value = results[index][0]    
    print value    
    if isinstance(value, float):
        while True:            
            try:
                genList[index].send((True, value))
            except:
                break
            print next(genList[index])[0]
        genList.pop(index)
    else:
        removeList = []    
        for i in range(len(genList)):
            keep = False        
            if i == index:
                keep = True
            try:
                genList[i].send((keep, value))
            except:
                removeList.append(genList[i])
        
        for gen in removeList:
            genList.remove(gen)
for gen in genList:
    gen.close()
    
    
    
    
    
    
    
    
=======
sl1 = [s1, s2]
full = sum(sl1)

print full
>>>>>>> parent of 06c80e0... Getting close on nearest line test coroutine
