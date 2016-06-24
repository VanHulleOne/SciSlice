# -*- coding: utf-8 -*-
"""
Created on Thu Jun  9 13:12:35 2016
@author: adiebold
"""

import figura as fg
from gcode import Gcode
import time
from parameters import Parameters
import json
import os
import doneShapes as ds
import constants as c

class Main:
  
    main_data = {}
    outline_options = {}
    trimAdjust_options = {}
    
    TRIMADJUST = 'trimAdjust'
    REGULARDOGBONE = 'regularDogBone'
    EPSILON = 'EPSILON'
    STL_FILE = 'stl_file'
    
    def __init__(self, name):
        with open(name, 'r') as fp:
            self.main_data = json.load(fp)
#        self.outline_options[self.REGULARDOGBONE] = ds.regularDogBone()
        self.trimAdjust_options[self.EPSILON] = c.EPSILON
        for key in self.trimAdjust_options:              
            if key in self.main_data[self.TRIMADJUST][0]:
                option = self.trimAdjust_options[key]
                if any(char.isdigit() for char in self.main_data[self.TRIMADJUST][0]):
                    number = int(''.join(t for t in self.main_data[self.TRIMADJUST][0] if t.isdigit()))
                    option *= number
                self.main_data[self.TRIMADJUST][0] = option
        self.pr = Parameters(self.main_data)
        self.gc = Gcode(self.pr)
    
    def run(self):
        startTime = time.time()
        print('\nGenerating code, please wait...')
        
        #creates new, blank file for use
        temp = open("data_points.txt", 'w')
        temp.close()
        
        fig = fg.Figura(self.main_data[self.STL_FILE], self.pr, self.gc)
        
        with open(self.pr.outputSubDirectory+'\\'+self.pr.outputFileName, 'w') as f:      
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
            
            