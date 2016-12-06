# -*- coding: utf-8 -*-
"""
Created on Fri Nov 06 10:30:44 2015

Used creating all of the lines of Gcode.

@author: lvanhulle
"""
import constants as c
class Gcode:
    
    def __init__(self, param):
        self.pr = param

    def feedMove(self, endPoint, omitZ, extrudeTo, printSpeed):
        if omitZ:
            tempString = ('X{:.3f} Y{:.3f} E{:.3f}'.format(endPoint.x,
                          endPoint.y, extrudeTo))
        else:
            tempString = ('X{:.3f} Y{:.3f} Z{:.3f} E{:.3f}\n'.format(endPoint.x,
                          endPoint.y, endPoint.z, extrudeTo))
    
        return 'G01 ' + tempString + ' F{:.0f}\n'.format(printSpeed)
    
                    
    
    def rapidMove(self, endPoint, omitZ):
        if omitZ:
            return ('G00 X{:.3f} Y{:.3f} F{:.0f}\n'.format(endPoint.x, endPoint.y,
                    self.pr.RAPID))
        else:
            return ('G00 X{:.3f} Y{:.3f} Z{:.3f} F{:.3f}\n'.format(endPoint.x, endPoint.y, endPoint.z,
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
            lines = endFile.readlines()       
        tempString = ''
        for line in lines:
            tempString += str(line)
        return tempString
        
class RobotCode:
    def __init__(self, param):
        self.pr = param
        self.tool = 'tNozzle'
        self.work = 'wobjPlatform'
        self.pZero = 'pZero'
        self.currZ = 50
        self.BLR = "DO6_Between_Layer_Retract"
        self.program_feed = "DO5_Program_Feed"
        self.printing = False
        
    def setDO(self, name, value):
        tempString = '\t\tWaitRob \InPos;\n'
        tempString += '\t\tSetDO {}, {};\n'.format(name, value)
        return tempString
    
    def feedMove(self, endPoint, omitZ, extrudeTo, printSpeed):
        moveString = ''
        if not self.printing:
            moveString = self.setDO(self.program_feed, 1)
        moveString += self._linearMove(endPoint, omitZ, printSpeed)
        return moveString                    
    
    def rapidMove(self, endPoint, omitZ):
        tempString = ''
        if self.printing:
            tempString = self.setDO(self.program_feed, 0)
        tempString += self._linearMove(endPoint, omitZ, self.pr.RAPID)
        return tempString
                    
    def _linearMove(self, endPoint, omitZ, speed):
        if omitZ:
            tempString = ','.join(str(round(i,3)) for i in endPoint[:2]) + ', ' + str(self.currZ)
        else:
            tempString = ','.join(str(round(i,3)) for i in endPoint[:3])
            self.currZ = endPoint[c.Z]
    
        return ('\t\tMoveL Offs(' + self.pZero + ', ' + tempString +
                '), v{:.0f}, z0, '.format(speed) + self.tool + ', \\Wobj := ' + self.work + ';\n')        
                    
    def retractLayer(self, currentE, currentPoint):
        tempString = self.setDO(self.BLR, 1)
        cpVect = currentPoint[:3]
        cpVect[c.Z] += self.pr.Z_CLEARANCE
        tempString += self._linearMove(cpVect, c.INCLUDE_Z, self.pr.RAPID)
        return tempString
        
    def approachLayer(self, lastE, startPoint):
        tempString = self.setDO(self.BLR, 0)
        tempString += self._linearMove(startPoint, c.INCLUDE_Z, self.pr.APPROACH_FR)
        return tempString
    
    def firstApproach(self, lastE, startPoint):
        tempString = self._linearMove(startPoint, c.INCLUDE_Z, self.pr.APPROACH_FR)
        tempString += self.setDO(self.BLR, 0)
        return tempString
#        return 'G1 Z{:.3f} F{:.0f} E{:.3f}\n'.format(startPoint.z, self.pr.APPROACH_FR, lastE)
        
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
            lines = endFile.readlines()       
        tempString = ''
        for line in lines:
            tempString += str(line)
        return tempString
