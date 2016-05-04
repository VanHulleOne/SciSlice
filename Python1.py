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
   
currOutline = ds.regularDogBone()
#currOutline = ds.rect(0,0,15,250)
filledList = []

for shellNumber in range(pr.numShells):
    filledList.append(currOutline)
    currOutline = currOutline.offset(pr.pathWidth, c.INSIDE)

#pattern = lg.LineGroup()
#pattern.addLinesFromCoordinateList([[0,0],[2,2],[4,0]])
infill = InF.InFill(currOutline, pr.pathWidth, pr.infillAngleDegrees)#, pattern)

filledList.append(infill)


print 'Created Infill: {:.2f}'.format(time.time()-startTime)


fig = fg.Figura(filledList)
generateTime = time.time()

print '\nCode generated, writting file...\n'

with open(pr.outputSubDirectory+'\\'+pr.outputFileName, 'w') as f:
    string = ''
    f.write(string.join(fig.gcode))

endTime = time.time()
print 'Done writting: ' + pr.outputFileName + '\n'

print '{:.2f} seconds to generate code.'.format(generateTime - startTime)
print '{:.2f} seconds to write.'.format(endTime - generateTime)
print '______'
print '{:.2f} total time'.format(endTime - startTime)