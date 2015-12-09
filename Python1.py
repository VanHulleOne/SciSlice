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
import doneShapes as ds
import time

startTime = time.time()

t1 = ds.DoneShapes()
shape = t1.wideDogBone

print '\nGenerating code, please wait...\n'
#infill = InF.InFill()
fig = fg.Figura(shape)

print 'Code generated, writting file...\n'

f = open(pr.outputSubDirectory+'\\'+pr.outputFileName, 'w')
f.write(gc.startGcode())
f.write(fig.gcode)
f.write(gc.endGcode())

f.close()

print 'Dong writting: ' + pr.outputFileName

print '{:.3f} seconds to produce.'.format(time.time() - startTime)
