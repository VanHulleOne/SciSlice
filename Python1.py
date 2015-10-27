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

def distance(first, second):
    """Returns the distance between two points"""
    return math.sqrt((first[X] - second[X])**2 + (first[Y] - second[Y])**2)
    
def squareDistance(first, second):
    """Returns the squared distance between two points to save on computation time"""
    return ((first[X] - second[X])**2 + (first[Y] - second[Y])**2)

def calcIncludedAngle(start, end, direction):
    """
    Given an input of two angles, calculated in unit circle fashion, and the
    direction around the circle you want to travel, this method will return
    the total included angle.
    """    
    t = end - start
    if(direction == CW and t > 0):
        return t - 2*math.pi
    elif(direction == CCW and t < 0):
        return 2*math.pi+t
    elif(t == 0):
        return 2*math.pi
    else:
        return t

#TODO: Convert this method to using matric multiplication
def mirror(shape, axis):
    """Given a list of points and an axis this method will return the mirrored points"""
    if(axis == X):
        deltaX = 1
        deltaY = -1
    else:
        deltaX = -1
        deltaY = 1
    temp = [[c[X]*deltaX, c[Y]*deltaY] for c in shape]
    temp.reverse()
    return temp
    
def translate(shape, xShift, yShift):
    temp = [[c[X]+xShift, c[Y]+yShift] for c in shape]
    return temp

def arcToLineList(arc):
    """Converts an arc to a set of line segments"""
    radius = distance(arc[START], arc[CENTER])
    startAngle = math.atan2(arc[START] [Y]- arc[CENTER][Y],
                        arc[START] [X]- arc[CENTER][X])
    startAngle = startAngle if startAngle >= 0 else 2*math.pi+startAngle
    endAngle = math.atan2(arc[END] [Y]- arc[CENTER][Y],
                        arc[END] [X]- arc[CENTER][X])
    endAngle = endAngle if endAngle >= 0 else 2*math.pi+endAngle

    includedAngle = calcIncludedAngle(startAngle, endAngle, arc[DIR][0])
    currentAngle = startAngle
    tempList = [arc[START]]
    for i in range(numPoints-2):
        currentAngle += includedAngle/(numPoints-1)
        x = arc[CENTER][X]+radius*math.cos(currentAngle)
        y = arc[CENTER][Y]+radius*math.sin(currentAngle)
        tempList.append([x, y])
    tempList.append(arc[END])
#    print tempList
    return tempList
    
def areColinear(p1, p2, p3):
    """
    This method tests if three points all lie on the same line, it is used
    by the removeDuplicates() method and should be removed after the program
    is concerted over to have a lines class.
    """
    if(p1[X] == p2[X] == p3[X]):#vertical line
        return True
    elif(p1[X] == p2[X] or p2[X] == p3[X]): #only one line is vertical       
        return False
    elif(abs((p2[Y]-p1[Y])/(p2[X]-p1[X]) - (p3[Y]-p2[Y])/(p3[X]-p2[X])) < 0.001): #the slope difference between P1P2 and P2P3 is less than an eror amount            
        return True
    return False
    
def removeDuplicates(lines):
    """
    If a shape contains two identical points, not counting the first and last,
    or three points that are colinear, the redundant points are removed.
    This method should be removed after the line class is created.
    """
    i = 0
    while i < (len(lines)-2):
        if(lines[i] == lines[i+1] or lines[i+1] == lines[i+2]):
            del lines[i+1]
        elif(areColinear(lines[i], lines[i+1], lines[i+2])):
            del lines[i+1]
        else:
            i += 1
    if(areColinear(lines[len(lines)-2], lines[len(lines)-1], lines[0])):
#        print 'here line 92'
        del lines[len(lines) - 1]
        del lines[0]
        lines.append(lines[0])
    return lines
    
def getLineAngle(p1, p2):
    angle = math.atan2((p2[Y]-p1[Y]), (p2[X] - p1[X]))
    return angle if angle >= 0 else angle + 2*math.pi
    
def isInside(point, shape):
    """
    Given an input point and a shape this method determines if the shape is inside
    or outside the shape and returns 1 if inside and 0 if outside.
    
    If a line is drawn from the point down to the outside of the part, the number
    of times that line intersects with the shape determines if the point was inside
    or outside. If the number of intersections is even then the point was outside
    of the shape. If the number of intersections is odd then the point is inside.
    """
    lowerPoint = [point[X], shape[0][Y]-10]
    intersections = 0
    for i in range(len(shape)-1):
        if(shape[i+1][Y] < lowerPoint[Y]): lowerPoint[Y] -= 10 
        result, intersectPoint =  segmentsIntersect(point, lowerPoint, shape[i], shape[i+1])
        if(result == 1):
            intersections += 1
    return (intersections % 2) #if intersections is odd then the point was insdie, else it was outside

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

def orderTwoNumbers(n1, n2):
    """Given an input of two numbers reutrn them lowest to highest"""
    return ((n1, n2) if n1 < n2 else (n2, n1))

# a bounding box for a line segment is the upper left and lower right corners
# of the smallest box that encloses the line segment
def getBoundingBox(p1, p2):
    """
    Given two points marking the ends of a line, return the upper left
    and lower right coordinates of the smallest box which containts the line.
    """
    if(p1[Y] == p2[Y]):
        return ((p1, p2) if p1[X] < p2[X] else (p2, p1))
    if(p1[X] == p2[X]):
        return ((p1, p2) if p1[Y] > p2[Y] else (p2, p1))
    upperLeft = [None]*2
    lowerRight = [None]*2
    upperLeft[X], lowerRight[X] = orderTwoNumbers(p1[X], p2[X])
    lowerRight[Y], upperLeft[Y] = orderTwoNumbers(p1[Y], p2[Y])
    return (upperLeft, lowerRight)
    
    
def boundingBoxesIntersect(p1, p2, q1, q2):
    """
    Given the coordinates for two bouding boxes return whether or not the two
    bouding boxes overlap.
    """
    bb1 = getBoundingBox(p1, p2)
    bb2 = getBoundingBox(q1, q2)
#    print 'bb1: ', bb1
#    print 'bb2: ', bb2
    if(bb1[0][X] <= bb2[1][X] and
            bb1[1][X] >= bb2[0][X] and
            bb1[0][Y] >= bb2[1][Y] and
            bb1[1][Y] <= bb2[0][Y]):
                return True
    return False

def getOrientation(p1, p2, p3):
    """
    getOrientation takes in three points,
    returns 0 if they are colinear
    returns 1 if the turn is clockwise
    returns 2 if the turn is CCW
    """
    val = ((p2[Y] - p1[Y])*(p3[X] - p2[X]) - 
            (p2[X] - p1[X])*(p3[Y] - p2[Y]))
    if(val == 0): return 0 #colinear
    return (1 if val > 0 else 2)

def pointToNormalVector(point):
    return [[point[X]], [point[Y]], [1.0]]
    
def normalVectorToPoint(nv):
    return [nv[X][0], nv[Y][0]]

def segmentsIntersect(p1, p2, q1, q2):
    if(not boundingBoxesIntersect(p1, p2, q1, q2)): return -1, None #return if bounding boxes do not intersetc
    o1 = getOrientation(p1, p2, q1)
    o2 = getOrientation(p1, p2, q2)
    o3 = getOrientation(q1, q2, p1)
    o4 = getOrientation(q1, q2, p2)
    
    if((o1+o2+o3+o4) == 0): return 0, None #return if all 4 points are colinear
    
    if(o1 != o2 and o3 != o4):
        r = numpy.subtract(p2, p1)
        s = numpy.subtract(q2, q1)
        Q_Less_P = numpy.subtract(q1, p1)
        denom = numpy.cross(r, s)
        t = numpy.cross(Q_Less_P, s)/denom
        u = numpy.cross(Q_Less_P, r)/denom
        if(abs(t) > 1 or abs(u) > 1):
            print 'Should we be here? segmentsIntersect math problem, I think'
        return 1, [p1[X]+r[X]*t, p1[Y]+r[Y]*t] #lines intersect at given point
    return -2, None #bounding boxes intersected but lines did not

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
    
def getshapeMinMax(shape):
    """Given an input shape reutrns the min and max for each axis plus 5"""
    minX = shape[0][X]-5
    maxX = minX+10
    minY = shape[0][Y]-5
    maxY = minY+10
    
    for point in shape:
        if(point[X] < minX): minX = point[X]-5
        elif(point[X] > maxX): maxX = point[X]+5
        if(point[Y] < minY): minY = point[Y]-5
        elif(point[Y] > maxY): maxY = point[Y]+5
    return minX, maxX, minY, maxY

def setOfLines(lineSpace, lineAngle, insideShape):
    lineSet = [[[]]]
    minX, maxX, minY, maxY = getshapeMinMax(insideShape)
    maxDiagonal = distance([minX, minY], [maxX, maxY])+4*lineSpace
    centerX = (maxX-minX)/2.0 + minX
    centerY = (maxY-minY)/2.0 + minY
    leftX = centerX-maxDiagonal/2.0
    rightX = centerX+maxDiagonal/2.0
    lineSet[0] = [[leftX, centerY, 1], [rightX, centerY, 1]]
    numSteps = int(maxDiagonal/2.0/lineSpace)
    for i in range(1, numSteps):
        lineSet.append([[leftX, centerY+i*lineSpace], [rightX, centerY+i*lineSpace]])
        lineSet.append([[leftX, centerY-i*lineSpace], [rightX, centerY-i*lineSpace]])
    lineSet = sorted(lineSet, key = lambda line : line[0][1])
    R = [[math.cos(lineAngle), -math.sin(lineAngle)], [math.sin(lineAngle), math.cos(lineAngle)]]
    p = [[centerX], [centerY]]
#    print "p: ", p
    p_lessRp = numpy.subtract(p, numpy.dot(R, p))
#    print 'p_lessRp: ', p_lessRp
    T = [[0 for x in range(3)] for x in range(3)]
    
    for i in range(2):
        for j in range(2):
            T[i][j] = R[i][j]
    T[0][2] = p_lessRp[0][0]
    T[1][2] = p_lessRp[1][0]
    T[2][2] = 1.0

    for i in range(len(lineSet)):
        normalVector1 = numpy.dot(T, pointToNormalVector(lineSet[i][0]))
        normalVector2 = numpy.dot(T, pointToNormalVector(lineSet[i][1]))
        lineSet[i][0] = normalVectorToPoint(normalVector1)
        lineSet[i][1] = normalVectorToPoint(normalVector2)

    return lineSet   

def getMidPoint(line):
    x = (line[0][X] - line[1][X])/2.0 + line[1][X]
    y = (line[0][Y] - line[1][Y])/2.0 + line[1][Y]
    return ([x, y])
    
def closeShape(shape):
    if(shape[0][X] != shape[-1][X] or shape[0][Y] != shape[-1][Y]):
        shape.append(shape[0])
        return shape
    return shape

#create a multi point line, start, end, intersect point
#then sort by XY, then create seperate line segments, then check if in middle
#maybe make newLines[[]] the list of line segments and then put the lines in finalLines[[]]
def trimBackground(background, outline):
    newLines = [[]]
    offset = 1
    for line in background:
        newLines.append([line[0]]) #add first point of line to last line in newLines
        for i in range(len(outline)-1):
            value, point = segmentsIntersect(line[0], line[1], outline[i], outline[i+1])
            if(value == 1):
                newLines[offset].append(point)
#                offset += 1
#                newLines.append([point])
        newLines[offset].append(line[1])
        offset += 1
    newLines.pop(0)
#    for line in newLines:
#        print line
        
    finalLines = [[]]
  
    for lineSet in newLines:
        lineSet = sorted(lineSet, key = operator.itemgetter(0,1))        
        for i in range(len(lineSet)-1):
            line = [lineSet[i], lineSet[i+1]]
            if(isInside(getMidPoint(line), outline)):
                finalLines.append(line)
    finalLines.pop(0)    
    return finalLines

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

    

dogBone = [[82.5, 0], [82.5, 9.5], [49.642, 9.5]]
dogBone.extend(arcToLineList(arc1))
dogBone.append([0,6.5])
dogBone.extend(mirror(dogBone, Y))
dogBone.extend(mirror(dogBone, X))

dogBone = removeDuplicates(dogBone)
dogBone = translate(dogBone, 120, 40)
finalShape = dogBone

point1 = p.Point(1,2)
point2 = p.Point(3,2)

line1 = l.Line(point1, point2)

print line1

line1.translate(4,4)
print line1


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
