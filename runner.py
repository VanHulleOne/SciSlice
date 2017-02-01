# -*- coding: utf-8 -*-
"""
Created on Thu Jun  9 13:12:35 2016
@author: adiebold
"""

import figura as fg
from gcode import Gcode, RobotCode
import time
from parameters import makeParamObj
import json
import constants as c

class Runner:
    
    def __init__(self, jsonName, outputFileName, gRobot, layerParamLabels, partParamLabels):
        self.outputFileName = outputFileName
        with open(jsonName, 'r') as fp:
            data = json.load(fp)

        self.pr = makeParamObj(data[0], data[1], layerParamLabels, partParamLabels)
        if gRobot == c.GCODE:
            self.gc = Gcode(self.pr)
        elif gRobot == c.ROBOTCODE:
            self.gc = RobotCode(self.pr)
    
    def run(self):
        startTime = time.time()
        print('\nGenerating code, please wait...')
        
        fig = fg.Figura(self.pr, self.gc)

        with open(self.outputFileName, 'w') as f:
            for string in fig.masterGcode_gen():
                f.write(string)
        
        endTime = time.time()
        print('\nCode generated.')
        print('Done calculating: ' + self.outputFileName + '\n')
        print('{:.2f} total time'.format(endTime - startTime))
        return fig.data_points


           