# -*- coding: utf-8 -*-
"""
Created on Thu Dec 03 16:30:08 2015

@author: lvanhulle
"""

import Shape as s
import arc as a
import Point as p
from parameters import constants as c

class DoneShapes():


    @property
    def regularDogBone(self):    
        dogBone = s.Shape(None)
        dogBone.addLinesFromCoordinateList([[82.5, 0], [82.5, 9.5], [49.642, 9.5]])
        arc = a.Arc(p.Point(49.642, 9.5), p.Point(28.5, 6.5), c.CW, p.Point(28.5, 82.5), 20)
        dogBone.addLineGroup(arc)
        dogBone.addLinesFromCoordinateList([[28.5, 6.5], [0, 6.5]])
        dogBone.addLineGroup(dogBone.mirror(c.Y))
        dogBone.addLineGroup(dogBone.mirror(c.X))
        dogBone.outlineFinished = True
        return dogBone.translate(82.5, 9.5)
    
    @property
    def wideDogBone(self):
        halfWidth = 5.0    
        wideDogBone = s.Shape(None)
        wideDogBone.addLinesFromCoordinateList([[82.5, 0], [82.5, 9.5 + halfWidth], [49.642, 9.5 + halfWidth]])
        wideArc = a.Arc(p.Point(49.642, 9.5 + halfWidth), p.Point(28.5, 6.5 + halfWidth), c.CW, p.Point(28.5, 82.5 + halfWidth), 20)
        wideDogBone.addLineGroup(wideArc)
        wideDogBone.addLinesFromCoordinateList([[28.5, 6.5 + halfWidth], [0, 6.5 + halfWidth]])
        wideDogBone.addLineGroup(wideDogBone.mirror(c.Y))
        wideDogBone.addLineGroup(wideDogBone.mirror(c.X))
        wideDogBone.outlineFinished = True
        return wideDogBone.translate(82.5, 9.5 + halfWidth)
        
    @property
    def rightGrip(self):
        shape = s.Shape(None)
        shape.addLinesFromCoordinateList([[82.5, 0], [82.5, 9.5], [49.642, 9.5]])
        arc = a.Arc(p.Point(49.642, 9.5), p.Point(28.5, 6.5), c.CW, p.Point(28.5, 82.5), 20)
        shape.addLineGroup(arc)
        shape.addLinesFromCoordinateList([[28.5, 6.5], [28.5, 0]])
        shape.addLineGroup(shape.mirror(c.X))
        shape.outlineFinished = True
        return shape.translate(82.5, 9.5)
        
    @property
    def leftGrip(self):
        shape = s.Shape(self.rightGrip)
        shape = shape.translate(-82.5, -9.5)
        shape = shape.mirror(c.Y)
        shape.outlineFinished = True
        return shape.translate(82.5, 9.5)
        
    @property
    def grips(self):
        shape = self.leftGrip
        shape.addLineGroup(self.rightGrip)
        shape.outlineFinished = True
        return shape

    @property
    def center(self):
        shape = s.Shape(None)
        shape.addLinesFromCoordinateList([[28.5, 6.5], [-28.5, 6.5], [-28.5, -6.5],
                                          [28.5, -6.5], [28.5, 6.5]])                                          
        shape.outlineFinished = True
        return shape.translate(82.5, 9.5)
        

