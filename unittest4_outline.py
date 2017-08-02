# -*- coding: utf-8 -*-
"""
Created on Tue Jul 11 14:20:51 2017

@author: siddhant
"""

import unittest
from point import Point
from line import Line
from linegroup import LineGroup
import constants as c
#import numpy as np
#import matrixTrans as mt
from outline import Outline
#from infill import Infill

pt1 = Point(0.0, 0.0, 0.0)
pt2 = Point(6.0, 0.0, 0.0)
pt3 = Point(6.0, 6.0, 0.0)
pt4 = Point(0.0, 6.0, 0.0)

ln1 = Line(pt1, pt2)
ln2 = Line(pt2, pt3)
ln3 = Line(pt3, pt4)
ln4 = Line(pt4, pt1)

pt5 = Point(2.0, 2.0, 0.0)
pt6 = Point(2.0, 4.0, 0.0)
pt7 = Point(4.0, 4.0, 0.0)
pt8 = Point(2.0, 4.0, 0.0)

ln5 = Line(pt5, pt6)
ln6 = Line(pt6, pt7)
ln7 = Line(pt7, pt8)
ln8 = Line(pt8, pt5)

pt9 = Point(8.0, 0.0, 0.0)
pt10 = Point(8.0, 6.0, 0.0)

ln9 = Line(pt1, pt9)
ln10 = Line(pt9, pt10)
ln11 = Line(pt10, pt4)
ln12 = Line(pt10, pt1)

class OutlineTestCase(unittest.TestCase):
    
    def test_outline_add_linegroup(self):
        """ checks if linegroup correctly added to outline (addLineGroup) """
        o = Outline()
        lg = LineGroup()
        lg.append(ln1)
        o.addLineGroup(lg)
        self.assertTrue(o[0] == ln1)
        
    def test_outline_is_inside(self):
        """ checks if the given point is contained within the outline """
        o = Outline()
        o.append(ln1)
        o.append(ln2)
        o.append(ln3)
        o.append(ln4)
        p_in = Point(2,2)
        p_out = Point(8,6,0)
        self.assertTrue(o.isInside(p_in) == 1)
        self.assertFalse(o.isInside(p_out) == 1)
        
    def test_outline_offset(self):
        """ checks if outline is offset correctly in given direction """
        o = Outline()
        o.append(ln1)
        o.append(ln2)
        o.append(ln3)
        o.append(ln4)
        o1 = o.offset(2, c.OUTSIDE)
        self.assertTrue(o1[0] == 
                        Line(Point(-2.0,0.0,0.0), Point(-2.0, 6.0, 0.0)))
        
    def test_outline_do_intersect(self):
        """ checks if two given outlines intersect (doOutlinesIntersect) """
        o = Outline()
        o.append(ln1)
        o.append(ln2)
        o.append(ln3)
        o.append(ln4)
        
        o1 = Outline()
        o1.append(ln5)
        o1.append(ln6)
        o1.append(ln7)
        o1.append(ln8)
        
        o2 = Outline()
        o2.append(ln9)
        o2.append(ln10)
        o2.append(ln11)
        o2.append(ln12)
        
        self.assertTrue(o.doOutlinesIntersect(o1) == False)
        self.assertTrue(o.doOutlinesIntersect(o2) == True)
        
    def test_outline_add_internal_shape(self):
        """ checks if given shape is added to outline (addInternalShape) """
        o = Outline()
        o.append(ln1)
        o.append(ln2)
        o.append(ln3)
        o.append(ln4)
        
        o1 = Outline()
        o1.append(ln5)
        o1.append(ln6)
        o1.append(ln7)
        o1.append(ln8)
        #print(o1)
        
        o.addInternalShape(o1)
        #print(o)
        #print(o1)
        self.assertTrue(o[4] == ln8)
        #adds lines in strange order
        
    def test_outline_close_shape(self):
        """ checks if the given outline is closed (closeShape) """
        o = Outline()
        o.append(ln1)
        o.append(ln2)
        o.closeShape()
        self.assertTrue(o[2] == Line(Point(6.0,6.0,0.0), Point(0.0,0.0,0.0)))
        
    def test_outline_finish(self):
        """ checks if the given outline is finished (finishOutline) """
        o = Outline()
        o.append(ln1)
        o.append(ln2)
        o.append(ln3)
        o.append(ln4)
        self.assertTrue(o.finishOutline() == None)
    
def main():
    unittest.main()
      
if __name__ == '__main__':
    main()
        
