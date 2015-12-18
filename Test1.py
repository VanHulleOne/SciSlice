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
from operator import itemgetter
import time

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

#def coro_avg():
#    total = 0.0
#    count = 0
#    current = yield
#    while True:
#        count += 1
#        total += current
#        current = yield total/count
#        
#avg = coro_avg()
#next(avg)
#for i in range(1,20,2):
#    print avg.send(i)
def min_gen(inList, index):
    seed = yield
    while len(inList) > 0:
        lowest, dist = min(((val, abs(val - seed)) for val in inList), key=itemgetter(1))     
        used, seed = yield lowest, dist, index
#        print inList
        if used:
            inList.remove(lowest)


l1 = [7,4,1, 99, 100, 103]
l2 = [2,5,6,10,-127, 96]
l3 = [-128]
l0 = [0.5, 1.5, 2.1, 7.8, 3.3, 1.0]
l4 = [l1,l2,l3, l0]

#g = min_gen(l3, 0)
#print next(g)
#print next(g)
#print g.send((True,0))
#print next(g)

print min(None, -1, 2)

genList = {i : min_gen(l4[i], i) for i in range(len(l4))}           

for key, gen in genList.iteritems():
    gen.next()

value, dist, index = min((genList[key].send(0) for key in genList), key=itemgetter(1))
while len(genList) > 0:
    time.sleep(0.5)    
    print value    
    if isinstance(value, float):
        while True:            
            try:
                value = genList[index].send((True, value))[0]
                print value
            except:
                break
        genList[index].close()
        del genList[index]
#    try:
    tempList = []
    delList = []
    for key, gen in genList.iteritems():
        try:
            tempList.append(gen.send((True if key == index else False, value)))
        except:
            delList.append(key)
        else:
            value, dist, index = min(tempList, key=itemgetter(1))
    for key in delList:
        del genList[key]
