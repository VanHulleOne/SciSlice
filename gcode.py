# -*- coding: utf-8 -*-
"""
Created on Fri Nov 06 10:30:44 2015

@author: lvanhulle
"""

    
RAPID = 8000 #mm/min
TRAVERSE_RETRACT = 0.5 #mm to retract when traversing longer distances
MAX_EXTRUDE_SPEED = 100 #mm/min max speed to move filament
Z_CLEARANCE = 10.0 #mm to move Z up
APPROACH_FR = 2000 #mm/min aproach feedrate

def feedMove(endPoint, ommitZ, extrusionAmount, printSpeed):
    if ommitZ:
        return ('G01 X{:.3f} Y{:.3f} F{:.0f} E{:.3f}\n'.format(endPoint.x, endPoint.y,
                printSpeed, extrusionAmount))
    else:
        return ('G01 X{:.3f} Y{:.3f} Z{:.3f} F{:.0f} E{:.3f}\n'.format(endPoint.x, endPoint.y, endPoint.z,
                printSpeed, extrusionAmount))

def rapidMove(endPoint, ommitZ):
    if ommitZ:
        return ('G00 X{:.3f} Y{:.3f} F{:.0f}\n'.format(endPoint.x, endPoint.y,
                RAPID))
    else:
        return ('G00 X{:.3f} Y{:.3f} Z{:.3f} F{:.3f}\n'.format(endPoint.x, endPoint.y, endPoint.z,
                RAPID))
                
def retractLayer(currentE, currentPoint):
    tempString = 'G1 E{:.3f} F{:.0f}\n'.format(currentE-TRAVERSE_RETRACT, MAX_EXTRUDE_SPEED)
    tempString += 'G00 Z{:.3f} F{:.0f}\n'.format(currentPoint.z+Z_CLEARANCE, RAPID)
    return tempString
    
def approachLayer(lastE, startPoint):
    tempString = 'G1 Z{:.3} F{:.0} E{:.3}\n'.format(startPoint.z+Z_CLEARANCE/2.0,
                    APPROACH_FR, lastE-TRAVERSE_RETRACT*0.75)
    tempString += 'G1 Z{:.3} F{:.0} E{:.3}\n'.format(startPoint.z,
                    APPROACH_FR/2.0, lastE)
    return tempString

def firstApproach(startPoint):
    return 'G1 Z{:.3} F{:.0}\n'.format(startPoint.z)