# -*- coding: utf-8 -*-
"""
Created on Thu Jun  9 13:12:35 2016
@author: adiebold
"""

import sys
import os
#pathway = os.path.dirname(os.path.realpath(__file__)).split(sep='\\')
#pathway[-1] = 'DogBone'
#pathway = '\\'.join(pathway)
#
#sys.path.append(pathway)

import figura as fg
from gcode import Gcode, RobotCode
import time
from parameters import Parameters
import json
import constants as c

class Runner:
    
    def __init__(self, name, gRobot):
        with open(name, 'r') as fp:
            data, var_data = json.load(fp)

        self.pr = Parameters(data, var_data)
        if gRobot == c.GCODE:
            self.gc = Gcode(self.pr)
        elif gRobot == c.ROBOTCODE:
            self.gc = RobotCode(self.pr)
    
    def run(self):
        startTime = time.time()
        print('\nGenerating code, please wait...')
        
        #creates new, blank file for use
        temp = open("data_points.txt", 'w')
        temp.close()
        
        fig = fg.Figura(self.pr, self.gc)

        with open(self.pr.outputFileName, 'w') as f:
            for string in fig.masterGcode_gen():
                f.write(string)
        
        fig.close_file()
        endTime = time.time()
        print('\nCode generated.')
        print('Done writting: ' + self.pr.outputFileName + '\n')
        print('{:.2f} total time'.format(endTime - startTime))
        """
        if c.LOG_LEVEL < c.logging.WARN:
            with open(self.outputSubDirectory+'\\'+self.outputFileName, 'r') as test,\
                 open(self.outputSubDirectory+'\\SAVE_master.gcode') as master:
                testLines = test.readlines()
                masterLines = master.readlines()
                i = 0
                numDiffs = 0
                for t,m in zip(testLines, masterLines):
                    i += 1
                    if t != m:
                        numDiffs += 1
                        if i%10**round(np.log10(i*2)-1)<1:
                            print('Diff at line: ', i)
                            print('Test: ' + t)
                            print('Master: ' + m)
                            print('---------------------------\n')
            print('\nTotal number of differences: ', numDiffs)
        """


           