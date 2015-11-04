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

numPoints = 20
CW = -1
CCW = 1
circle = [[2,0],[2,0],[CCW], [0,0]]
arc1 = [[49.642, 9.5], [28.5, 6.5], [CW],[28.5, 82.5]]
X, Y =0, 1
START = 0
END = 1
DIR = 2
CENTER = 3
INSIDE = 1
OUTSIDE = 0

#fifferShape = [[0.0,0.0],[10.0,0.0],[18.1212,10.0],[22.9353,20.0],[26.1426,30.0],
#               [28.292,40.0],[29.6285,50.0],[30.2716,60.0],[30.2716,85.0],
#                [25.7716,85.0]]

outputFileName = 'DB_10-23_Test.gcode' #the name of the file you want output. git will ignore all .gcode unless they start with SAVE
start_Gcode_FileName = 'Start_Gcode_Taz5.txt' #the file name for the starting gcode
end_Gcode_FileName = 'End_Gcode_Taz5.txt' #The file name for the end gcode
beadWidth = 0.5
airGap = 0.0
ZStep = 0.4     #layer height
ZHeight = 3.201  #Total Height of the part
extrusionRate = 0.03 #mm of extrusion per mm of XY travel
travelSpeed = 2000 #mm per min
maxFeedStep = 5.0 #not implemented yet
slopeOverX = 0.0 #how much you want it to move over in X per level
slopeOverY = 0 #how much you want it to move over in Y per level
backgroundAngle = math.pi/2.0 #angle of the paths in the layer 0 = X direction, PI/2 = Y direction

outputSubDirectory = 'Gcode'
startEndSubDirectory = 'Start_End_Gcode'

tempShape1 = [[[]]]
    
def squareDistance(first, second):
    """Returns the squared distance between two points to save on computation time"""
    return ((first[X] - second[X])**2 + (first[Y] - second[Y])**2)
   
def getLineAngle(p1, p2):
    angle = math.atan2((p2[Y]-p1[Y]), (p2[X] - p1[X]))
    return angle if angle >= 0 else angle + 2*math.pi

#TODO: change the offset method to make the offset lines parallel with the exhisting lines   
def offset(shape, dist, side):
    """
    Given an input shape, distance, and if you want inside or outside, this
    method will return a new shape that is offset from the original. Currently
    if measures the offset distance along an angular bisector of each corner
    but this should be changed to make it calculate from a line normal to the
    exhisting line.
    """
    tempShape = [[]]
    line1Angle = getLineAngle(shape[0], shape[len(shape)-2])
    line2Angle = getLineAngle(shape[0], shape[1])
    halfAngle1 = (line1Angle + line2Angle)/2
    halfAngle2 = halfAngle1 + math.pi
    try1 = [shape[0][X] + dist*math.cos(halfAngle1), shape[0][Y] + dist*math.sin(halfAngle1)]
    try2 = [shape[0][X] + dist*math.cos(halfAngle2), shape[0][Y] + dist*math.sin(halfAngle2)]
    firstPoint = try1 if(isInside(try1, shape) == side) else try2
#    print 'Try1: ', try1, ' side: ', side, ' firstPoint: ', firstPoint
    tempShape[0] = firstPoint
    
    for i in range(1, len(shape)-1):
        line1Angle = getLineAngle(shape[i], shape[i-1])
        line2Angle = getLineAngle(shape[i], shape[i+1])
        halfAngle1 = (line1Angle + line2Angle)/2
        halfAngle2 = halfAngle1 + math.pi
        try1 = [shape[i][X] + dist*math.cos(halfAngle1), shape[i][Y] + dist*math.sin(halfAngle1)]
        try2 = [shape[i][X] + dist*math.cos(halfAngle2), shape[i][Y] + dist*math.sin(halfAngle2)]
        if(isInside(try1, shape)):
            tempShape.append(try1)
        elif(isInside(try2, shape)):
            tempShape.append(try2)              
                
    tempShape.append(firstPoint)
    return tempShape

#start from begining and compare from end
#When an intersection is found add the checked points to a list
#adjust the end points as needed on the new shape and the old
#recursively call the method with the old shape less the new shape  
#TODO: Does not handle a shape that intersects without forming a negative area
#or a shape that only forms a negative area without becoming positive again  
def intersectParser(shape, positiveArea):
    newShape = [[]]
    if(positiveArea): newShape[0] = shape[0]
    for i in range(len(shape)-2):
        point = []
        for j in range(len(shape)-2, i+2, -1):
            value, point = segmentsIntersect(shape[i], shape[i+1], shape[j], shape[j-1])
            if(value == 0): print 'Build something to handle this, intersectParser segments are co-linear'
            if(value == 1):
#                print 'Intersect Detected: ', point
                if(positiveArea):
                    newShape.append(point)
                    newShape.extend(shape[j:len(shape)])
                tempShape = [[]]
                tempShape[0] = point
                tempShape.extend(shape[i+1:j])
                tempShape.append(point)
                index = intersectParser(tempShape, not positiveArea)
                if(newShape != [[]]):
                    tempShape1.append(newShape)
                    return index+1
                return index
        if(positiveArea):
            newShape.append(shape[i+1])
    tempShape1[0] = newShape
    return 1


#TODO: Currently picks the next closest point, for some shapes this might
#       not be the best strategy, should print so that a new bead is always next
#       to an exhisting bead
def linesToPath(lineSet):
    Start, End = 0, 1
    path = [lineSet[0][Start], lineSet[0][End]]
    lineSet.pop(0)
    while(len(lineSet) != 0):
        current = path[-1]
        holdNext = lineSet[0][Start]
        leastSqDistance = squareDistance(current, holdNext)
        pointIsEnd = False
        storedIndex = 0
        for i in range(len(lineSet)):
            tempSqDistance = squareDistance(current, lineSet[i][Start])
            if(tempSqDistance < leastSqDistance):
                pointIsEnd = False
                leastSqDistance = tempSqDistance
                holdNext = lineSet[i][Start]
                storedIndex = i
            tempSqDistance = squareDistance(current, lineSet[i][End])
            if(tempSqDistance < leastSqDistance):
                pointIsEnd = True
                leastSqDistance = tempSqDistance
                holdNext = lineSet[i][End]
                storedIndex = i
        path.append(holdNext)
        path.append(lineSet[storedIndex][not pointIsEnd])
        lineSet.pop(storedIndex)            
    return path

    
"""
dogBone = [[82.5, 0], [82.5, 9.5], [49.642, 9.5]]
dogBone.extend(arcToLineList(arc1))
dogBone.append([0,6.5])
dogBone.extend(mirror(dogBone, Y))
dogBone.extend(mirror(dogBone, X))

dogBone = removeDuplicates(dogBone)
dogBone = translate(dogBone, 120, 40)
finalShape = dogBone
"""
#arc1 = [[49.642, 9.5], [28.5, 6.5], [CW],[28.5, 82.5]]

dogBone = s.Shape(None)
dogBone.addLinesFromCoordinateList([[82.5, 0], [82.5, 9.5], [49.642, 9.5]])
arc = a.Arc(p.Point(49.642, 9.5), p.Point(28.5, 6.5), CW, p.Point(28.5, 82.5), 20)
dogBone.addLineGroup(arc)
dogBone.addLineGroup(dogBone.mirror(Y))
dogBone.addLineGroup(dogBone.mirror(X))

infill = InF.InFill(dogBone, backgroundAngle, beadWidth, None, None)
print infill

#finalShape = closeShape(fifferShape)
"""
stepOver = beadWidth+airGap
numZSteps = int(ZHeight/ZStep)

background = setOfLines(stepOver, backgroundAngle, finalShape)

background = trimBackground(background, finalShape)

#for line in fillPattern:
#    for point in line:
#        print '{:.3f}\t{:.3f}'.format(point[X],point[Y])
        
pathPoints = linesToPath(background)

#pathPoints.reverse()
              
f = open(outputSubDirectory+'\\'+outputFileName, 'w')

f.write(';File Name: ' + outputFileName + '\n')
f.write(';Start Gcode from: ' + startEndSubDirectory + '\\' + start_Gcode_FileName)
f.write('\n')

with open(startEndSubDirectory + '\\' + start_Gcode_FileName) as startFile:
    lines = startFile.readlines()   
    for line in lines:    
        f.write(str(line))

f.write('\n\nG90 G21\n')

lineNumber = 1
totalExtrusion = 0
for level in range(1, numZSteps+1):
    f.write('\n; Level {:.0f} Z Height {:.3f}\n'.format(level, (level*ZStep)))
    f.write(';T{:.0f}\n'.format(level))
    f.write(';M6\n')
    f.write('G01 Z{:.3f} F{:.0f}\n'.format((level*ZStep+10), travelSpeed))
    f.write('G00 X{:.3f} Y{:.3f}\n'.format(pathPoints[0][X]+(level-1)*slopeOverX, pathPoints[0][Y]+(level-1)*slopeOverY))
    f.write('G01 Z{:.3f} F{:.0f} E{:.3f}\n'.format((level*ZStep), (travelSpeed/2), totalExtrusion))
    
    for i in range(len(pathPoints)-1):
        f.write('G01 X{:.3f} Y{:.3f} '.format(pathPoints[i+1][X]+(level-1)*slopeOverX, pathPoints[i+1][Y]+(level-1)*slopeOverY))
        f.write('F{:.0f} '.format(travelSpeed))
        extrusionAmount = extrusionRate * distance(pathPoints[i], pathPoints[i+1])
        totalExtrusion += extrusionAmount
        f.write('E{:.3f}\n'.format(totalExtrusion))     
        
    f.write('G01 Z{:.3f} F{:.0f} E{:.3f}\n'.format(((level+1)*ZStep+10), travelSpeed, (totalExtrusion-1)))

f.write('\n')
f.write(';End Gcode from: ' + startEndSubDirectory + '\\' + end_Gcode_FileName)
f.write('\n')

with open(startEndSubDirectory + '\\' + end_Gcode_FileName) as endFile:
    lines = endFile.readlines()       
    for line in lines:    
        f.write(str(line))
f.close()
print 'Done writing File.'
"""

"""
for loop in fullPath:
    f.write('(Loop Number {:.0f})\n'.format(loopNumber))
    f.write('T{:.0f}\nM6\n'.format(loopNumber))
    loopNumber += 1
    for point in loop:
        f.write('N{:.0f} X{:.3f} Y{:.3f}\n'.format(lineNumber, point[X],point[Y]))
        lineNumber+=1

for i in range(numOffsets):
    holdPath = offset(fullPath[i], beadWidth+airGap, INSIDE)
    if(intersectParser(holdPath, True) == 1):
        fullPath.append(holdPath)
    else:
        for path in tempShape1:
            fullPath.append(path)
            for j in range(i, numOffsets):
                fullPath.append(offset(fullPath[len(fullPath)-1], beadWidth+airGap, INSIDE))
        break
"""
