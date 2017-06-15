# -*- coding: utf-8 -*-
"""
Created on Thu Dec 03 16:30:08 2015

Functions used to more quickly create commonly used shapes or infills. Some of the functions
contain fully defined shapes while others allow parameter inputs to create a
custom outline.

Type hints have been used to determine whether a function returns an Outline or
anything else.  Inside RUN_ME.py the doneshapes module is inspected. During the
inspection the return type annotations for each function are read to determine
which is the appropriate dropdown for the function. Any function with otu a
return type annotation will not be added to the dropdown menu.

Typehints must also be used for input parameters so that they can be displayed
in the pop-up window which is created.

@author: lvanhulle
"""

import math
from typing import Callable, List

import arc as a
import constants as c
from line import Line
from linegroup import LineGroup
from point import Point
import outline as outline_module
from outline import Outline
import trimesh
from collections import namedtuple
from functools import wraps
import json
from parameters import zipVariables_gen
import os
import numpy as np

outlines = []
infills = []

OutlineAngle = namedtuple('SecAng', 'outline angle')

def outline(func):
    outlines.append(func.__name__)
    return func  
    
def make_coro(func):
    @wraps(func)
    def inner(*args, **kwargs):
        result = func(*args, **kwargs)
        def doubleInner():
            global_params = yield
            while True:
               global_params = yield (result,),(global_params,)
        return doubleInner
    return inner
    
def infill(func):
    infills.append(func.__name__)
    return func
    
def _getMesh(fname, change_units_from='mm'):
    change_units_from = change_units_from.lower()
    mesh = trimesh.load_mesh(fname)
    if change_units_from is not 'mm':
        mesh.units = change_units_from
        mesh.convert_units('mm')
    return mesh
    
def readMultiPartFile(fname):
    with open(fname, 'r') as file:
        bigList = json.load(file)
    fileNames = []
    paramNames = []
    paramLists = []
    for region in bigList:
        fileNames.append(region[c.FILENAME])
        del region[c.FILENAME]
        paramNames.append(list(region.keys()))
        paramLists.append(list(region.values()))
    return fileNames, paramNames, paramLists

def _getSectionFromMesh(mesh, height):
    return mesh.section(plane_origin=[0,0,height],plane_normal=[0,0,1])          

def _getOutlineFromSTL(fname: str, height: float, change_units_from: str='mm') ->Outline:
    mesh = _getMesh(fname, change_units_from)
    section = _getSectionFromMesh(mesh, height)
    outline = outline_module.outlineFromMeshSection(section)
    outline._name = os.path.basename(fname)
    return outline

def _multiRegionHandler(fname, change_units_from, sliceHeight=None):
    stl_names, eachPart_paramNames, eachPart_paramLists = readMultiPartFile(fname)
    path = os.path.dirname(fname) + '/'
    meshes = [_getMesh(path+stl_name, change_units_from) for stl_name in stl_names]
    bounds = np.array([mesh.bounding_box.bounds[0] for mesh in meshes])
    global_minXYZ = np.amin(bounds, axis=0)
    def multiRegion_coro():
        global_params = yield
        regions = [Region(name, mesh, paramNames, paramLists, global_minXYZ, sliceHeight) 
                    for name, mesh, paramNames, paramLists in
                    zip(stl_names, meshes, eachPart_paramNames, eachPart_paramLists)]
        for region in regions:
            region.sendGlobal(global_params)

        while any(region.outline for region in regions):
            regions.sort(key = lambda x: x.currHeight)
            used = [region for region in regions if region.currHeight == regions[0].currHeight]
#            print('curr Height:', regions[0].currHeight)
            outlines = tuple(region.outline for region in used if region.outline is not None)
            localParamNamedTuples = tuple(region.localParams for region in used if region.outline is not None)

            if outlines:
                global_params = yield outlines, localParamNamedTuples, used[0].currHeight
            for region in used:
                region.sendGlobal(global_params)

    return multiRegion_coro

@outline
def fromSTL(fname: str, change_units_from: str='mm'):
    mesh = _getMesh(fname, change_units_from)
    minX, minY, minZ = mesh.bounding_box.bounds[0]
    def fromSTL_coro():
        currHeight = minZ
        global_params = yield
        currHeight += global_params.layerHeight
        while True:
            try:
                section = mesh.section(plane_origin=[0,0,currHeight],plane_normal=[0,0,1])
            except Exception:
                return
            else:
                global_params = yield (outline_module.outlineFromMeshSection(section).translate(-minX, -minY),), (global_params,)
                currHeight += global_params.layerHeight
    return fromSTL_coro

@make_coro
@outline    
def fromSTL_oneLevel(fname: str, sliceHeight: float, change_units_from: str='mm') ->Outline:
    mesh = _getMesh(fname, change_units_from)
    _, _, minZ = mesh.bounding_box.bounds[0]
    section = _getSectionFromMesh(mesh, sliceHeight+minZ)
    outline = outline_module.outlineFromMeshSection(section)
    outline = outline.translate(-outline.minX, -outline.minY)
    outline._name = os.path.basename(fname)
    return outline

@outline
def multiRegion_oneLevel(fname: str, change_units_from: str, sliceHeight: float):
    return _multiRegionHandler(fname, change_units_from, sliceHeight)                      
    
@outline     
def multiRegion(fname: str, change_units_from: str='mm'):  
    return _multiRegionHandler(fname, change_units_from)

@make_coro        
@outline
def regularDogBone() ->Outline:    
    dogBone = Outline(None)
    dogBone.addLinesFromCoordinateList([[82.5, 0], [82.5, 9.5], [49.642, 9.5]])
    arc = a.Arc(Point(49.642, 9.5), Point(28.5, 6.5), c.CW, Point(28.5, 82.5), 20)
    dogBone.addLineGroup(arc)
    dogBone.addLinesFromCoordinateList([[28.5, 6.5], [0, 6.5]])
    dogBone.addLineGroup(dogBone.mirror(c.Y))
    dogBone.addLineGroup(dogBone.mirror(c.X))
    dogBone = dogBone.translate(82.5, 9.5)
    dogBone.finishOutline()
    dogBone._name = 'regularDogBone'
    return dogBone

@make_coro        
@outline
def regularDogBoneFillet(scale: float) ->Outline:    
    dogBoneF = Outline(None)
    dogBoneF.addLinesFromCoordinateList([[82.5, 0], [82.5, 4.5]])
    arc = a.Arc(Point(82.5, 4.5), Point(77.5, 9.5), c.CCW, Point(77.5, 4.5), 6) #5mm fillet
    dogBoneF.addLineGroup(arc)
    dogBoneF.addLinesFromCoordinateList([[77.5, 9.5], [49.642, 9.5]])
    arc = a.Arc(Point(49.642, 9.5), Point(28.5, 6.5), c.CW, Point(28.5, 82.5), 20)
    dogBoneF.addLineGroup(arc)
    dogBoneF.addLinesFromCoordinateList([[28.5, 6.5], [0, 6.5]])
    dogBoneF.addLineGroup(dogBoneF.mirror(c.Y))
    dogBoneF.addLineGroup(dogBoneF.mirror(c.X))
    dogBoneF = dogBoneF.translate(82.5, 9.5)
    dogBoneF.finishOutline()
    dogBoneF=dogBoneF.scale(scale)
    dogBoneF._name = 'regularDogBoneFillet'
    return dogBoneF
    
@make_coro        
@outline    
def typeVDogBone(scale: float) ->Outline:
    typeV = Outline(None)
    typeV.addLinesFromCoordinateList([[31.75, 0], [31.75, 3.77]])
    arc=a.Arc(Point(31.75,3.77), Point(30.75,4.77), c.CCW, Point(30.75,3.77),5) #1mm fillet
    typeV.addLineGroup(arc)
    typeV.addLinesFromCoordinateList([[30.75,4.77], [13.17, 4.77]])
    arc=a.Arc(Point(13.17, 4.77), Point(4.77, 1.59), c.CW, Point(4.77, 14.29))
    typeV.addLineGroup(arc)
    typeV.addLinesFromCoordinateList([[4.77,1.59], [0,1.59]])
    typeV.addLineGroup(typeV.mirror(c.Y))
    typeV.addLineGroup(typeV.mirror(c.X))
    typeV= typeV.translate(31.75, 4.77)
    typeV.finishOutline()
    typeV=typeV.scale(scale)
    typeV._name= 'typeVDogBone'
    return typeV
    
def testSimpleDogBone() ->Outline:
    temp = Outline(None)
    temp.addLinesFromCoordinateList([[82.5,0],[82.5,9.5],[49.642, 9.5], [28.5,6.5],[0,6.5]])
    temp.addLineGroup(temp.mirror(c.Y))
    temp.addLineGroup(temp.mirror(c.X))
    temp = temp.translate(82.5, 9.5)
    temp.finishOutline()
    return temp

@make_coro 
@outline     
def wideDogBone(gageWidth: float) ->Outline:
    halfWidth = gageWidth / 2.0    
    wideDogBone = Outline(None)
    wideDogBone.addLinesFromCoordinateList([[82.5, 0], [82.5, 9.5 + halfWidth],
                                            [49.642, 9.5 + halfWidth]])
    wideArc = a.Arc(Point(49.642, 9.5 + halfWidth),
                    Point(28.5, 6.5 + halfWidth), c.CW,
                    Point(28.5, 82.5 + halfWidth), 20)
    wideDogBone.addLineGroup(wideArc)
    wideDogBone.addLinesFromCoordinateList([[28.5, 6.5 + halfWidth], [0, 6.5 + halfWidth]])
    wideDogBone.addLineGroup(wideDogBone.mirror(c.Y))
    wideDogBone.addLineGroup(wideDogBone.mirror(c.X))
    return wideDogBone.translate(82.5, 9.5 + halfWidth)
   
def rightGrip() ->Outline:
    outline = Outline(None)
    outline.addLinesFromCoordinateList([[82.5, 0], [82.5, 9.5], [49.642, 9.5]])
    arc = a.Arc(Point(49.642, 9.5), Point(28.5, 6.5), c.CW, Point(28.5, 82.5), 20)
    outline.addLineGroup(arc)
    outline.addLinesFromCoordinateList([[28.5, 6.5], [28.5, 0]])
    outline.addLineGroup(outline.mirror(c.X)) 
    return outline.translate(82.5, 9.5)

def leftGrip() ->Outline:
    outline = rightGrip()
    outline = outline.translate(-82.5, -9.5)
    outline = outline.mirror(c.Y)
    return outline.translate(82.5, 9.5)

def grips() ->Outline:
    outline = leftGrip()
    outline.addLineGroup(rightGrip())
    return outline

def center() ->Outline:
    outline = Outline(None)
    outline.addLinesFromCoordinateList([[28.5, 6.5], [-28.5, 6.5], [-28.5, -6.5],
                                      [28.5, -6.5], [28.5, 6.5]])
    return outline.translate(82.5, 9.5)
    
def squareWithHole() ->Outline:
    outline = Outline(None)
    outline.addLinesFromCoordinateList([[0,0], [50,0], [50,50], [0,50], [0,0]])
    circle = a.Arc(Point(35,25), Point(35,25), c.CW, Point(25,25))
    outline.addLineGroup(circle)
    return outline

@make_coro
@outline    
def circle(centerX: float, centerY: float, radius: float) ->Outline:
    startPoint = Point(centerX+radius, centerY)
    center = Point(centerX, centerY)
    return Outline(a.Arc(startPoint, startPoint, c.CW, center, numPoints=40))

@make_coro     
@outline     
def rectangle(lowerLeftX: float, lowerLeftY: float, X_width: float, Y_height: float) ->Outline:
    rect = [Point(lowerLeftX, lowerLeftY)]
    rect.append(Point(lowerLeftX+X_width, lowerLeftY))
    rect.append(Point(lowerLeftX+X_width, lowerLeftY+Y_height))
    rect.append(Point(lowerLeftX, lowerLeftY+Y_height))
    rectLG = Outline(None)
    rectLG.addLinesFromPoints(rect)
    rectLG.closeShape()
    return rectLG

@make_coro     
@outline     
def polygon(centerX: float, centerY: float, radius: float, numCorners: int) ->Outline:
    angle = 1.5*math.pi
    points = []
    incAngle = 2*math.pi/numCorners
    for i in range(numCorners):
        x = math.cos(angle+incAngle*i)*radius+centerX
        y = math.sin(angle+incAngle*i)*radius+centerY
        points.append(Point(x,y))
    poly = Outline(None)
    poly.addLinesFromPoints(points)
    poly.closeShape()
    poly = poly.rotate(incAngle/2.0, Point(centerX, centerY))
    return poly

@infill        
def straightLines() -> Callable[[float, float, float], LineGroup]:
    def _straightLines(*, space: float=0, length: float=0, height: float=0) -> LineGroup:
        lines = []
        currHeight = 0
        while currHeight < height:
            lines.append(Line(Point(0,currHeight), Point(length,currHeight)))
            currHeight += space
        group = LineGroup()
        group.lines = lines
        group.minX = 0
        group.minY = 0
        group.maxX = length
        group.maxY = currHeight-space
        return group
    return _straightLines
    
@infill
def hexagons(sideLength: float) -> Callable[[float, float, float], LineGroup]:
    def _hexagons(*, space: float=0, length: float=0, height: float=0) -> LineGroup:
        baseLine = LineGroup(None)
        baseLine.addLinesFromCoordinateList([[0,0], [sideLength, 0],
                 [sideLength+math.cos(math.pi/4)*sideLength, math.cos(math.pi/4)*sideLength],
                  [sideLength*2+math.cos(math.pi/4)*sideLength, math.cos(math.pi/4)*sideLength],
                   [2*(sideLength+math.cos(math.pi/4)*sideLength), 0]])
        fullLine = LineGroup(baseLine)
        
        while fullLine.maxX - fullLine.minX < length:
            baseLine = baseLine.translate(baseLine.maxX - baseLine.minX, 0)
            fullLine.addLineGroup(baseLine)
            
        mirrorLine = LineGroup(fullLine)
        mirrorLine = mirrorLine.mirror(c.X)
        mirrorLine = mirrorLine.translate(0, -space)
        fullLine.addLineGroup(mirrorLine)
        field = LineGroup(fullLine)
        
        while field.maxY - field.minY < height:
            fullLine = fullLine.translate(0, fullLine.maxY-fullLine.minY+space)
            field.addLineGroup(fullLine)
        return field
    return _hexagons

@infill    
def noInfill() -> LineGroup:
    return LineGroup()
    
class Region:
    def __init__(self, name, mesh, paramNames, paramLists, global_minXYZ, height=None):
        self.name = name
        self.mesh = mesh
        self.paramNames = paramNames
        self.paramGen = zipVariables_gen(paramLists, repeat=True)
        self.currHeight = 0
        self.outline = None
        self.localParams = None
        self.global_minXYZ = global_minXYZ
        
        if height is not None:
            try:
                section = _getSectionFromMesh(self.mesh, height + self.global_minXYZ[c.Z])
            except Exception as e:
                raise Exception('Height for .STL slice did not intersect .STL\n' + str(e))
            else:
                self.outline = outline_module.outlineFromMeshSection(section).translate(-self.global_minXYZ[c.X],
                                                                                        -self.global_minXYZ[c.Y])
                self.oneLevel = True
        else:
            self.oneLevel = False

        
    def sendGlobal(self, globalParams):
        localParamDict = {paramName : param for paramName, param in
                          zip(self.paramNames, next(self.paramGen))}
        self.localParams = globalParams._replace(**localParamDict)
        
        self.currHeight += self.localParams.layerHeight
        if not self.oneLevel:
            self.setNextOutline()
            
    def setNextOutline(self):
        try:
            section = _getSectionFromMesh(self.mesh, self.currHeight+self.global_minXYZ[c.Z])
        except Exception:
#            print('Exception. currHeight:', self.currHeight)
            self.outline = None
        else:
            self.outline = outline_module.outlineFromMeshSection(section).translate(-self.global_minXYZ[c.X],
                                                                                    -self.global_minXYZ[c.Y])
    
    
    def __repr__(self):
        return 'Region-> ' + str(self.name)
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
       