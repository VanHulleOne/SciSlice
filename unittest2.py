# -*- coding: utf-8 -*-
"""
Created on Wed Jul  5 15:50:23 2017

@author: siddhant
"""

import unittest
from point import Point
from line import Line
from linegroup import LineGroup
#import constants as c
import numpy as np

p1 = Point(1.0, 2.0, 3.0)
p2 = Point(2.0, 4.0, 6.0)
p3 = Point(6.0, 12.0, 18.0)
p4 = Point(8.0, 12.0, 14.0)

l1 = Line(p1, p2)
l2 = Line(p1, p3)
l4 = Line(Point(0,0), Point(0, 8, 0))
l5 = Line(Point(4, 0, 0), Point(0, 6, 0))

lg1 = LineGroup()
lg2 = LineGroup()
lg2.append(l1)


class LineGroupTestCase(unittest.TestCase):
    
    def test_linegroup_getitem(self):
        """ checks if correct line in linegroup is returned """
        self.assertTrue(lg2[0] == l1)
        
    def test_linegroup_append(self):
        """ checks if correct line is appended to linegroup """
        lg2.append(l2)
        self.assertTrue(lg2[1] == l2)
        
    #print(lg2)
    
    def test_linegroup_remove(self):
        lg2.append(l2)
        lg2.remove(l1)
        self.assertTrue(lg2[0] == l2)
        
#    def test_linegroup_length(self):
#        self.assertTrue(lg2.__len__ == 1)

    def test_linegroup_pop(self):
        """ checks if correct line returned when linegroup popped """
        lg2.append(l2)
        self.assertTrue(lg2.pop() == l2)
        
    #print(lg2)
    
    def test_linegroup_midpoint(self):
        """ checks if correct midpoint of linegroup returned """
        self.assertTrue(lg2.getMidPoint() == Point(3.5, 7.0, 0.0))
        
    #print(lg2)
    #print(lg1)
        
    def test_linegroup_add_linegroup(self):
        """ checks if linegroup is correctly added """
        lg1.append(l2)
        lg2.addLineGroup(lg1)
        self.assertTrue(lg2[1] == l2)
        
    #print(lg2)
    print(lg2)
    #vectors
    #starts (numpy.ndarray issue)
    
#    def test_linegroup_add_linesfrompoints(self):
#        """ checks if line is correctly added """
#        lg2.addLinesFromPoints([Point(-4, -6, 8), Point(2, 4, 6)])
#        print(lg2)
#        self.assertTrue(lg2[2] == Line(Point(-4, -6, 8), Point(2, 4, 6)))
    
    #    def test_linegroup_pop(self):
#        """ checks if correct line is returned when popped """
#        self.assertTrue(lg1.pop() == l1)
    
    

def main():
    unittest.main()
      
if __name__ == '__main__':
    main()