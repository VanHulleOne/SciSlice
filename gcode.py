# -*- coding: utf-8 -*-
"""
Created on Fri Nov 06 10:30:44 2015

Used creating all of the lines of Gcode.

@author: lvanhulle
"""
from collections import defaultdict
import constants as c
from point import Point

class Gcode:
    
    def __init__(self, param):
        self.pr = param

    def feedMove(self, endPoint, extrudeTo, printSpeed):
        tempString = ('X{:.3f} Y{:.3f} E{:.3f}'.format(endPoint.x,
                      endPoint.y, extrudeTo))
        return 'G01 ' + tempString + ' F{:.0f}\n'.format(printSpeed)                    
    
    def rapidMove(self, endPoint, atClearance=False):
        return ('G00 X{:.3f} Y{:.3f} Z{:.3f} F{:.3f}\n'.format(endPoint.x,
                                                                endPoint.y,
                                                                endPoint.z + atClearance*self.pr.Z_CLEARANCE,
                                                                self.pr.RAPID))
                    
    def retractLayer(self, currentE, currentPoint):
        tempString = 'G1 E{:.3f} F{:.0f}\n'.format(currentE-self.pr.TRAVERSE_RETRACT, self.pr.MAX_EXTRUDE_SPEED)
        tempString += 'G00 Z{:.3f} F{:.0f}\n'.format(currentPoint.z+self.pr.Z_CLEARANCE, self.pr.RAPID)
        return tempString
        
    def approachLayer(self, lastE, startPoint):
        tempString = 'G1 Z{:.3f} F{:.0f} E{:.3f}\n'.format(startPoint.z+self.pr.Z_CLEARANCE/2.0,
                        self.pr.RAPID, lastE-self.pr.TRAVERSE_RETRACT*0.75)
        tempString += 'G1 Z{:.3f} F{:.0f} E{:.3f}\n'.format(startPoint.z,
                        self.pr.APPROACH_FR, lastE)
        return tempString
    
    def firstApproach(self, lastE, startPoint):
        return 'G1 Z{:.3f} F{:.0f} E{:.3f}\n'.format(startPoint.z, self.pr.APPROACH_FR, lastE)
        
    def newPart(self):
        return 'G92 E0\n'
        
    def operatorMessage(self, *args, sep=' '):
        return 'M117 '+ sep.join(str(arg) for arg in args) + '.\n'
        
    def comment(self, comment):
        return self.pr.comment + ' ' + comment
    
    def startGcode(self,*, extruder_temp=0, bed_temp=0):
        with open(self.pr.startEndSubDirectory + '\\' + self.pr.start_Gcode_FileName) as startFile:
            lines = startFile.readlines()   
            tempString = []
            for line in lines:
                line = str(line).replace(c.EXTRUDER_TEMP_FLAG, 'S'+str(extruder_temp))
                line = line.replace(c.BED_TEMP_FLAG, 'S'+str(bed_temp))
                tempString.append(line)
            return ''.join(tempString)
    
    def endGcode(self):
        with open(self.pr.startEndSubDirectory + '\\' + self.pr.end_Gcode_FileName) as endFile:
            return ''.join(endFile.readlines())
        
class RobotCode:
    
    def __init__(self, param):
        self.pr = param
        self.tool = 'tNozzle'
        self.work = 'wobjPlatform'
        self.pZero = 'pZero'
 #       self.currZ = 50
        self.BLR = "DO6_Between_Layer_Retract"
        self.program_feed = "DO5_Program_Feed"
        self.currOutputs = defaultdict(int)
        self.currOutputs.setdefault(0)
        
    def setDO(self, name, value, *args):
        tempList = []
        iterator = iter((name, value) + args)
        for _name, _value in zip(iterator, iterator):
            if self.currOutputs[_name] != _value:
                tempList.append('\t\tSetDO {}, {};\n'.format(_name, _value))
                self.currOutputs[_name] = _value
        if tempList:
            return  '\t\tWaitRob \InPos;\n' + ''.join(tempList)              
        return ''
    
    def feedMove(self, endPoint, extrudeTo, printSpeed):
        moveString = self.setDO(self.program_feed, 1)
        moveString += self._linearMove(endPoint, printSpeed)
        return moveString                    
    
    def rapidMove(self, endPoint, *, atClearance=False):
        tempString = self.setDO(self.program_feed, 0)
        tempString += self._linearMove(endPoint, self.pr.RAPID, atClearance=atClearance)
        return tempString
                    
    def _linearMove(self, endPoint, speed, *, atClearance=False):
        tempString = ', '.join(str(round(i,3)) for i in (endPoint.x,
                                                         endPoint.y,
                                                         endPoint.z + atClearance*self.pr.Z_CLEARANCE)) 
        
        return ('\t\tMoveL Offs(' + self.pZero + ', ' + tempString +
                '), v{:.0f}, z0, '.format(speed) + self.tool + ', \\Wobj := ' + self.work + ';\n')        
                    
    def retractLayer(self, currentE, currentPoint):
        tempString = self.setDO(self.BLR, 1, self.program_feed, 0)
        tempString += self._linearMove(currentPoint, self.pr.RAPID, atClearance=True)
        return tempString
        
    def approachLayer(self, lastE, startPoint):
        tempString = self.setDO(self.BLR, 0)
        tempString += self._linearMove(startPoint, self.pr.APPROACH_FR)
        return tempString
    
    def firstApproach(self, lastE, startPoint):
        tempString = self._linearMove(startPoint, self.pr.APPROACH_FR)
        tempString += self.setDO(self.BLR, 0)
        return tempString
        
    def newPart(self):
        return '\n'#'G92 E0\n'
    
    def operatorMessage(self, *args, sep=' '):
        return '\t\tTPWRITE "'+ sep.join(str(arg) for arg in args) + '";\n'
        
    def comment(self, comment):
        return '\t\t' + self.pr.comment + ' ' + comment
        
    def startGcode(self,*, extruder_temp=0, bed_temp=0):
        with open(self.pr.startEndSubDirectory + '\\' + self.pr.start_Gcode_FileName) as startFile:
            lines = startFile.readlines()   
            tempString = []
            for line in lines:
                line = str(line).replace(c.EXTRUDER_TEMP_FLAG, 'S'+str(extruder_temp))
                line = line.replace(c.BED_TEMP_FLAG, 'S'+str(bed_temp))
                tempString.append(line)
            return ''.join(tempString)
    
    def endGcode(self):
        with open(self.pr.startEndSubDirectory + '\\' + self.pr.end_Gcode_FileName) as endFile:
            return ''.join(endFile.readlines())

