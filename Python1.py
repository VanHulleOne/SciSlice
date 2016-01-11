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
import LineGroup as lg
import InFill as InF
import arc as a
import figura as fg
import parameters as pr
import gcode as gc
from parameters import constants as c
import doneShapes as ds
import time

startTime = time.time()
print '\nGenerating code, please wait...\n'

bigTest = True

if bigTest:
    leftGrip = ds.leftGrip()
    center = ds.center()
    center.addLineGroup(ds.circle(82.5, 9.5, 4))
    rightGrip = ds.rightGrip()
    grips = ds.grips()
    grips2 = grips.offset(1, c.INSIDE)
    regDB = ds.regularDogBone()
    regDB1 = regDB.offset(0.5, c.OUTSIDE)
    regDB2 = regDB1.offset(0.5, c.OUTSIDE)
    sq1 = ds.squareWithHole()
    sq2 = sq1.offset(1, c.INSIDE)
    sq3 = sq2.offset(1, c.INSIDE)
    
    pattern = lg.LineGroup()
    pattern.addLinesFromCoordinateList([[0,0], [2,2], [4,0]])
    
    filledLeft = InF.InFill(leftGrip, pr.pathWidth, 45, pattern)
    filledCenter = InF.InFill(center, pr.pathWidth, 90, pattern)
    filledRight = InF.InFill(rightGrip, pr.pathWidth, -45, pattern)
    filledList = [filledLeft, filledCenter, filledRight, regDB1, regDB2]
    
else:
    regDB = ds.regularDogBone()
    filledDB = InF.InFill(regDB, pr.pathWidth, 90)
    filledList = [filledDB]

print 'Created Infill: {:.2f}'.format(time.time()-startTime)

#for line in filledGrips:
#    line.extrusionRate = pr.fullExtrusionRate
#    line.freezeExRate = True

fig = fg.Figura(filledList)
generateTime = time.time()

print '\nCode generated, writting file...\n'

with open(pr.outputSubDirectory+'\\'+pr.outputFileName, 'w') as f:
    f.write(fig.gcode)

endTime = time.time()
print 'Dong writting: ' + pr.outputFileName + '\n'

print '{:.2f} seconds to generate code.'.format(generateTime - startTime)
print '{:.2f} seconds to write.'.format(endTime - generateTime)
print '______'
print '{:.2f} total time'.format(endTime - startTime)

