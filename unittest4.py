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
#from outline import _sidedpolygon
#import numpy as np
#import matrixTrans as mt
from outline import Outline

p1 = Point(0.0, 0.0, 0.0)
p2 = Point(6.0, 0.0, 0.0)
p3 = Point(6.0, 6.0, 0.0)
p4 = Point(0.0, 6.0, 0.0)

l1 = Line(p1, p2)
l2 = Line(p2, p3)
l3 = Line(p3, p4)
l4 = Line(p4, p1)

p5 = Point(2.0, 2.0, 0.0)
p6 = Point(2.0, 4.0, 0.0)
p7 = Point(4.0, 4.0, 0.0)
p8 = Point(2.0, 4.0, 0.0)

l5 = Line(p5, p6)
l6 = Line(p6, p7)
l7 = Line(p7, p8)
l8 = Line(p8, p5)

p9 = Point(8.0, 0.0, 0.0)
p10 = Point(8.0, 6.0, 0.0)

l9 = Line(p1, p9)
l10 = Line(p9, p10)
l11 = Line(p10, p4)
l12 = Line(p10, p1)

class OutlineTestCase(unittest.TestCase):
    
    def test_outline_add_linegroup(self):
        """ checks if linegroup correctly added to outline (addLineGroup) """
        o = Outline()
        lg = LineGroup()
        lg.append(l1)
        o.addLineGroup(lg)
        self.assertTrue(o[0] == l1)
        
    def test_outline_is_inside(self):
        """ checks if the given point is contained within the outline """
        o = Outline()
        o.append(l1)
        o.append(l2)
        o.append(l3)
        o.append(l4)
        p_in = Point(2,2)
        p_out = Point(8,6,0)
        self.assertTrue(o.isInside(p_in) == 1)
        self.assertFalse(o.isInside(p_out) == 1)
        
    def test_outline_offset(self):
        """ checks if outline is offset correctly in given direction """
        o = Outline()
        o.append(l1)
        o.append(l2)
        o.append(l3)
        o.append(l4)
        o1 = o.offset(2, c.OUTSIDE)
        self.assertTrue(o1[0] == 
                        Line(Point(-2.0,0.0,0.0), Point(-2.0, 6.0, 0.0)))
        
    def test_outline_do_intersect(self):
        """ checks if two given outlines intersect (doOutlinesIntersect) """
        o = Outline()
        o.append(l1)
        o.append(l2)
        o.append(l3)
        o.append(l4)
        
        o1 = Outline()
        o1.append(l5)
        o1.append(l6)
        o1.append(l7)
        o1.append(l8)
        
        o2 = Outline()
        o2.append(l9)
        o2.append(l10)
        o2.append(l11)
        o2.append(l12)
        
        self.assertTrue(o.doOutlinesIntersect(o1) == False)
        self.assertTrue(o.doOutlinesIntersect(o2) == True)
        
    def test_outline_add_internal_shape(self):
        """ checks if given shape is added to outline (addInternalShape) """
        o = Outline()
        o.append(l1)
        o.append(l2)
        o.append(l3)
        o.append(l4)
        
        o1 = Outline()
        o1.append(l5)
        o1.append(l6)
        o1.append(l7)
        o1.append(l8)

        o.addInternalShape(o1)
        self.assertTrue(o[4] == l5)
        
    def test_outline_close_shape(self):
        """ checks if the given outline is closed (closeShape) """
        o = Outline()
        o.append(l1)
        o.append(l2)
        o.closeShape()
        self.assertTrue(o[2] == Line(Point(6.0,6.0,0.0), Point(0.0,0.0,0.0)))
        
    def test_outline_finish(self):
        """ checks if the given outline is finished (finishOutline) """
        o = Outline()
        o.append(l1)
        o.append(l2)
        o.append(l3)
        o.append(l4)
        self.assertTrue(o.finishOutline() == None)
        
                                                                                                                                        
def main():
    unittest.main()
      
if __name__ == '__main__':
    main()
        