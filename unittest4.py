# -*- coding: utf-8 -*-
"""
Created on Tue Jul 11 14:20:51 2017

@author: siddhant
"""

import unittest
from point import Point
from line import Line
from linegroup import LineGroup
#import constants as c
#import numpy as np
#import matrixTrans as mt
from outline import Outline

p1 = Point(1.0, 2.0, 3.0)
p2 = Point(2.0, 4.0, 6.0)
p3 = Point(6.0, 12.0, 18.0)
p4 = Point(8.0, 12.0, 14.0)

l1 = Line(p1, p2)
l2 = Line(p1, p3)
l4 = Line(Point(0,0), Point(0, 8, 0))
l5 = Line(Point(4, 0, 0), Point(0, 6, 0))

l = LineGroup()
l.append(l1)
l.append(l2)

o = Outline()
o.addLineGroup(l)

class OutlineTestCase(unittest.TestCase):
    
    def test_outline_add_linegroup(self):
        """ checks if linegroup correctly added to outline """
#        o = Outline()
##        l = LineGroup()
##        l.append(l1)
##        l.append(l2)
#        o.addLineGroup(l)
        self.assertTrue(o[1] == l2)
        
    def test_outline_is_inside(self):
        """ checks if the given point is contained within the outline """
#        o = Outline()
#        o.addLineGroup(l)
        p = Point(2,2)
        self.assertTrue(o.isInside(p) == 0)
        
    def test_outline_offset(self):
        """ checks if outline is offset correctly in given direction """
        
        
        
        
        
def main():
    unittest.main()
      
if __name__ == '__main__':
    main()
        