# -*- coding: utf-8 -*-
"""
Created on Mon Sep 21 09:51:36 2015

@author: lvanhulle
"""
import math
import numpy
import operator
import Point as p
import Line as l
import Shape as s
import LineGroup as LG
import InFill as InF
import arc as a
import figura as fg
import parameters as pr
import gcode as gc
from parameters import constants as c

    
dogBone = s.Shape(None)
dogBone.addLinesFromCoordinateList([[82.5, 0], [82.5, 9.5], [49.642, 9.5]])
arc = a.Arc(p.Point(49.642, 9.5), p.Point(28.5, 6.5), c.CW, p.Point(28.5, 82.5), 20)
dogBone.addLineGroup(arc)
dogBone.addLinesFromCoordinateList([[28.5, 6.5], [0, 6.5]])
dogBone.addLineGroup(dogBone.mirror(c.Y))
dogBone.addLineGroup(dogBone.mirror(c.X))
dogBone.translate(82.5, 9.5)

halfWidth = 5.0    
wideDogBone = s.Shape(None)
wideDogBone.addLinesFromCoordinateList([[82.5, 0], [82.5, 9.5 + halfWidth], [49.642, 9.5 + halfWidth]])
wideArc = a.Arc(p.Point(49.642, 9.5 + halfWidth), p.Point(28.5, 6.5 + halfWidth), c.CW, p.Point(28.5, 82.5 + halfWidth), 20)
wideDogBone.addLineGroup(wideArc)
wideDogBone.addLinesFromCoordinateList([[28.5, 6.5 + halfWidth], [0, 6.5 + halfWidth]])
wideDogBone.addLineGroup(wideDogBone.mirror(c.Y))
wideDogBone.addLineGroup(wideDogBone.mirror(c.X))
wideDogBone.translate(82.5, 9.5 + halfWidth)

#print dogBone
 
infill = InF.InFill(wideDogBone)
fig = fg.Figura(infill)

#print infill

#print 'dogBone'
#print str(dogBone)
#print 'Fig:'
#print fig.gcode

print '\nGenerating File, please wait...\n'

f = open(pr.outputSubDirectory+'\\'+pr.outputFileName, 'w')
f.write(gc.startGcode())
f.write(fig.gcode)
f.write(gc.endGcode())

f.close()

print 'Dong writting: ' + pr.outputFileName
