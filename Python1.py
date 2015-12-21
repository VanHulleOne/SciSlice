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

ds1 = ds.DoneShapes()
leftGrip = ds1.leftGrip
center = ds1.center
rightGrip = ds1.rightGrip
grips = ds1.grips
regDB = ds1.regularDogBone


pattern = lg.LineGroup()
pattern.addLinesFromCoordinateList([[0,0], [4,4], [8,0]])

#print pattern

#filledLeft = InF.InFill(leftGrip, pr.pathWidth, 90)
#filledCenter = InF.InFill(center, pr.pathWidth, 90)
#filledRight = InF.InFill(rightGrip, pr.pathWidth, 90)
#filledGrips = InF.InFill(grips, pr.pathWidth, 90)
filledDB = InF.InFill(regDB, pr.pathWidth, 20, pattern, 0)
print 'Created Infill: {:.2f}'.format(time.time()-startTime)
#with open('I:\RedBench\static\data\LineList.txt', 'w') as f:
#    f.write('test\n')
#    f.write(filledDB.CSVstr())

#for line in filledGrips:
#    line.extrusionRate = pr.fullExtrusionRate
#    line.freezeExRate = True
#
filledList = [filledDB]
#

#
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

