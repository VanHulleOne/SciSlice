# -*- coding: utf-8 -*-
"""
Created on Mon Sep 21 09:51:36 2015

@author: lvanhulle
"""

import figura as fg
import parameters as pr
import doneShapes as ds
import time


startTime = time.time()
print '\nGenerating code, please wait...'
   
currOutline = ds.regularDogBone()

fig = fg.Figura(currOutline)
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