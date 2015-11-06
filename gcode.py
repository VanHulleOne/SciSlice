# -*- coding: utf-8 -*-
"""
Created on Fri Nov 06 10:30:44 2015

@author: lvanhulle
"""
import InFill
import Shape

class Gcode:
    
    MAX_PRINT_STEP = 2.0
    Z_RETRACT = 2.0
    E_RETRACT = 0.1
    Z_UP_CLEARANCE = 10.0
    NEXT_LINE_TOL = 0.001
    
    def __init__(self, lineGroup, Zstep, Zheight, extrusionRate, travelSpeed):
        if(type(lineGroup) is list):
            self.lineGroup = lineGroup
        else:
            self.lineGroup = [lineGroup]
            
        self.Zstep = Zstep
        self.Zheight = Zheight
        self.extrusionRate = extrusionRate
        self.travelSpeed = travelSpeed
        self.gcodeString = None
        self.totalExtrude = 0
        
        
        for group in lineGroup:
            if(isinstance(group, Shape)):
                self.toGcode(group.lines)
            else:
                lines = self.orderedLines(group)
                self.toGcode(lines)
        
    def orderedLines(self, group):
        lines = group.getLines()
        lines.sort()
        tempLines = [lines.pop(0)]
        if(tempLines[0].start > tempLines[0].end):
            tempLines[0].flip()
            
        while(len(lines) > 0):
            flip = False
            leastDist = tempLines[-1].end.squareDistance(lines[0].start)
            leastOffset = 0
            for i in range(len(lines)):
                tempDist = tempLines[-1].end.squareDistance(lines[i].start)
                if(tempDist < self.NEXT_LINE_TOL):
                    leastOffset = i
                    flip = False
                    break
                if(tempDist < leastDist):
                    leastOffset = i
                    leastDist = tempDist
                    flip = False
                    
                tempDist = tempLines[-1].end.squareDistance(lines[i].end)
                if(tempDist < self.NEXT_LINE_TOL):
                    leastOffset = i
                    flip = True
                    break
                if(tempDist < leastDist):
                    leastOffset = i
                    leastDist = tempDist
                    flip = True
            holdLine = lines.pop(leastOffset)
            if(flip): holdLine.flip()
            tempLines.append(holdLine)
        return tempLines
            
        
        
    
        
    