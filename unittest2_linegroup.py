# -*- coding: utf-8 -*-
"""
Created on Wed Jul  5 15:50:23 2017

@author: siddhant
"""

import unittest
from point import Point
from line import Line
from linegroup import LineGroup
import constants as c
import numpy as np

p1 = Point(1.0, 2.0, 3.0)
p2 = Point(2.0, 4.0, 6.0)
p3 = Point(6.0, 12.0, 18.0)
p4 = Point(8.0, 12.0, 14.0)

l1 = Line(p1, p2)
l2 = Line(p1, p3)
l4 = Line(Point(0,0), Point(0, 8, 0))
l5 = Line(Point(4, 0, 0), Point(0, 6, 0))

#lg1 = LineGroup()
#lg2 = LineGroup()
#lg2.append(l1)


class LineGroupTestCase(unittest.TestCase):
    
    def test_linegroup_getitem(self):
        """ checks if correct line in linegroup is returned (__getitem__) """
        ltest = LineGroup()
        ltest.append(l1)
        self.assertTrue(ltest[0] == l1)
        
    def test_linegroup_append(self):
        """ checks if correct line is appended to linegroup (append) """
        ltest = LineGroup()
        ltest.append(l1)
        ltest.append(l2)
        self.assertTrue(ltest[1] == l2)
    
    def test_linegroup_remove(self):
        """ checks if line is correctly removed from group (remove) """
        ltest = LineGroup()
        ltest.append(l1)
        ltest.append(l2)
        ltest.remove(l1)
        self.assertTrue(ltest[0] == l2)
        
    def test_linegroup_length(self):
        """ checks if linegroup contains expected number of lines (__len__) """
        ltest = LineGroup()
        ltest.append(l1)
        ltest.append(l2)
        ltest.append(l4)
        count = 0
        for l in ltest:
            count = count + 1
        self.assertEqual(count, 3)
        
    def test_linegroup_pop(self):
        """ checks if correct line returned when linegroup popped (pop) """
        ltest = LineGroup()
        ltest.append(l1)
        ltest.append(l2)
        self.assertTrue(ltest.pop() == l2)
        
    def test_linegroup_midpoint(self):
        """ checks if correct midpoint of linegroup returned (getMidPoint) """
        #print(lg2)
        ltest = LineGroup()
        ltest.append(l1)
        self.assertTrue(ltest.getMidPoint() == Point(1.5, 3.0, 0.0))
             
    def test_linegroup_add_linegroup(self):
        """ checks if linegroup is correctly added (addLineGroup) """
        ltest = LineGroup()
        ltest.append(l1)
        
        ltest1 = LineGroup()
        ltest1.append(l2)
        ltest.addLineGroup(ltest1)
        self.assertTrue(ltest[1] == l2)
        
    def test_linegroup_mirror(self):
        """ checks if linegroup is correctly mirrored (mirror) """
        ltest = LineGroup()
        ltest.append(l1)
        
        #ltest1 = LineGroup()
        #ltest1.append(Line(Point(1,-2,3), Point(2,-4,6)))
        
        self.assertTrue(ltest.mirror(c.X)[0] == 
                        Line(Point(1,-2,3), Point(2,-4,6)))
        
    def test_linegroup_sort(self):
        """ checks if linegroup is sorted correctly (sort) """
        ltest = LineGroup()
        ltest.append(l1)
        ltest.append(l4)
        ltest.sort()
        self.assertTrue(ltest[0] == l4)
        
    def test_linegroup_fourcorners(self):
        """ checks if the four corners correspond to the correct points """
        ltest = LineGroup()
        ltest.append(l4)
        ltest.append(l5)
        self.assertTrue(ltest.fourCorners()[0] == Point(0,0,0))
        self.assertTrue(ltest.fourCorners()[1] == Point(4,0,0))
        self.assertTrue(ltest.fourCorners()[2] == Point(4,8,0))
        self.assertTrue(ltest.fourCorners()[3] == Point(0,8,0))
        
    def test_linegroup_scale(self):
        """ checks if start and end points of lines are scaled correctly """
        ltest = LineGroup()
        ltest.append(l1)
        ltest.append(l2)

        self.assertTrue(ltest.scale(2,3)[0] ==
                        Line(Point(2,6,3), Point(4,12,6)))
        self.assertTrue(ltest.scale(2,3)[1] == 
                        Line(Point(2,6,3), Point(12,36,18)))
        
    def test_linegroup_rotate(self):
        """ checks if linegroup is rotated correctly """
        ltest = LineGroup()
        ltest.append(l1)
        ltest.append(l2)
        self.assertTrue(ltest.rotate(np.pi/2)[0] == 
                        Line(Point(-2,1,3), Point(-4,2,6)))
        self.assertTrue(ltest.rotate(np.pi/2)[1] == 
                        Line(Point(-2,1,3), Point(-12,6,18)))
        
    def test_linegroup_translate(self):
        """ checks if linegroup is translated correctly """
        ltest = LineGroup()
        ltest.append(l1)
        ltest.append(l2)
        self.assertTrue(ltest.translate(2,4)[0] == 
                        Line(Point(3,6,3), Point(4,8,6)))
        self.assertTrue(ltest.translate(2,4)[1] == 
                        Line(Point(3,6,3), Point(8,16,18)))
        
    def test_linegroup_line_outside_boundingbox(self):
        """ checks if the given line is outside the bounding box """
        ltest = LineGroup()
        ltest.append(l1)
        ltest.append(l2)
        self.assertTrue(ltest.lineOutsideBoundingBox(l4) == True)
        self.assertTrue(ltest.lineOutsideBoundingBox(l5) == False)
        
        
    def test_linegroup_line_add_points(self):
        """ checks if line from given points is added to linegroup """
        ltest = LineGroup()
        ltest.append(l1)
        ltest.append(l2)
        p = [Point(1,1,0), Point(4,5,0)]
        ltest.addLinesFromPoints(p)
        self.assertTrue(ltest[2] == Line(Point(1,1,0), Point(4,5,0)))
        
    def test_linegroup_update_min_max(self):
        """ checks if the max & min x and y values are updated correctly """
        ltest = LineGroup()
        ltest.append(l1)
        ltest.append(l2)
        l = Line(Point(10,20,0), Point(14,-16,0))
        ltest.append(l)
        self.assertTrue(ltest.maxY == 20)
        self.assertTrue(ltest.maxX == 14)
        self.assertTrue(ltest.minY == -16)
        self.assertTrue(ltest.minX == 1)
        
    def test_linegroup_line_add_coordlist(self):
        """ checks if points from coordinate list added to linegroup """
        ltest = LineGroup()
        ltest.append(l1)
        k = [[3,4], [-6,7]]
        ltest.addLinesFromCoordinateList(k)
        self.assertTrue(ltest[1] == Line(Point(3,4,0), Point(-6,7,0)))
        
    def test_linegroup_transform(self):
        """ checks if lines within group are transfromed correctly """
        ltest = LineGroup()
        ltest.append(l1)
        ltest.append(l2)
        matr = [[0,0,0,1], [1,4,6,8], [0,6,7,9], [3,4,5,6]]
        ltest = ltest.transform(matr)
        self.assertTrue(ltest[0] == Line(Point(1,35,42),Point(1,62,75)))
        self.assertTrue(ltest[1] == Line(Point(1,35,42), Point(1,170,207)))

def main():
    unittest.main()
      
if __name__ == '__main__':
    main()
