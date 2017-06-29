# -*- coding: utf-8 -*-
"""
Created on Mon Jun 26 13:53:41 2017

@author: siddhant
"""

import unittest
from point import Point
import constants as c
from line import Line
import numpy as np


p1 = Point(1.0, 2.0, 3.0)
p2 = Point(2.0, 4.0, 6.0)
p3 = Point(6.0, 12.0, 18.0)
p4 = Point(8.0, 12.0, 14.0)

l1 = Line(p1, p2)
l2 = Line(p1, p3)
l3 = Line(p1, p2)
l4 = Line(Point(0,0), Point(0, 8, 0))
l5 = Line(Point(4, 0, 0), Point(0, 6, 0))

class PointTestCase (unittest.TestCase):
   
   #def test_point_valid(self):
    
    def test_point_equal(self):
        """ check if point is equal to given point (__eq__) """ 
        self.assertTrue(p1 == Point(1.0, 2.0, 3.0))
        self.assertFalse(p1 == Point(1.0, 3.0, 4.0))
      
    def test_point_notequal(self):
        """ check points are not equal (__ne__) """ 
        self.assertTrue(p1 != Point(1.0, 2.0, 8.0))
        self.assertFalse(p1 != Point(1.0, 2.0, 3.0))
    
    def test_point_negative(self):
        """ check if point negative is correct (__neg_) """
        self.assertTrue(-p1 == Point(-1.0, -2.0, 3.0))
        
    def test_point_lesser(self):
        """ compare two points to check lesser (__lt__) """
        self.assertTrue(p1 < Point(2.0, 4.0, 6.0))
        self.assertFalse(p1 < Point(1.0, 2.0, 2.0))
        
    def test_point_greater(self):
        """ compare two points to check greater (__gt__) """
        self.assertTrue(p1 > Point(1.0, 2.0, 2.0))
        self.assertFalse(p1 > Point(1.0, 2.0, 6.0))
          
    def test_point_sub(self):
        """ check distance between two points (__sub__) """
        self.assertAlmostEqual(p2-p1, 3.7417, places = 4)
            
    def test_initial_x_property(self):
        """ check if x-coordinate matches """
        self.assertTrue(p1.x == 1.0)
           
    def test_initial_y_propert(self):
        """ check if y-coordinate matches """
        self.assertTrue(p1.y == 2.0)
            
    def test_initial_z_property(self):
        """ check if z-coordinate matches """
        self.assertTrue(p1.z == 3.0)
       
    def test_get_item(self):
        """ check if correct coordinate is returned and slice correctly""" 
        self.assertTrue(p1[0] == 1.0)
        
    def test_get_point2D(self):
        """ check if x and y coordinates of point are correct """
        self.assertTrue(tuple(p1[0:2]) == (1.0, 2.0))
      
    def test_squaredistance(self):
        """ check squared distance between two points (squaredDistance) """
        self.assertTrue(((p1[0] - p2[0])**2 + (p1[1] - p2[1])**2) == 5.0)
      
    def test_point_mirror(self):
        """ check if point correctly mirrored about axis (mirror) """
        self.assertTrue(p1.mirror(c.X) == Point(1.0, -2.0, 3.0))
    
    def test_point_translate(self):
        """ check if point translates correctly  (translate) """
        self.assertTrue(p1.translate(1.0, 2.0) == Point(2.0, 4.0, 3.0))
     
    def test_point_rotate(self):
        """ check if point rotates as expected    (rotate) """
        self.assertTrue(p1.rotate(0) == Point(1.0, 2.0, 3.0))
        
class LineTestCase(unittest.TestCase):
    
    def test_length(self):
        """ checks length of the line (length) """
        self.assertAlmostEqual(p2 - p1, 3.7417, places = 4)
        
    def test_fliped(self):
        """ check if line flips direction as expected (fliped) """
        self.assertEqual(l1.fliped(), Line(p2, p1))
        
    def test_on_line(self):
        """ checks if given point is on line (isOnLine) """
        self.assertTrue(l1.isOnLine(p2) == True)

    def test_mirror_line(self):
        """ check if line mirrored correctly about given axis (mirror) """
        self.assertTrue(l1.mirror(c.X) == 
                        Line(Point(1.0, -2.0, 3.0), Point(2.0, -4.0, 6.0)))
    
    def test_lines_parallel(self):
        """ checks if the lines are parallel (areParallel) """
        self.assertTrue(l1.areParallel(l2) == True)
        
    def test_line_start(self):
        """ checks if starting point of line is correct """
        self.assertTrue(l1.start == p1)
        
    def test_line_end(self):
        """ checks if end point of line is correct """
        self.assertTrue(l1.end == p2)
        
    def test_line_angle(self):
        """ checks if line is oriented correctly by way of angle """
        self.assertAlmostEqual(l1.angle, 1.1071, places = 4)
        
    def test_line_midpoint(self):
        """ checks if midpoint of line is correct (getMidPoint) """
        self.assertTrue(l1.getMidPoint() == Point(1.5, 3.0, 4.5))
        
    def test_line_equal(self):
        ' checks if lines with same start and end points are equal (__eq__) '
        self.assertTrue(l1 == l3)
        self.assertFalse(l1 != l3)
        
    def test_line_lesser(self):
        """ checks if line is less than other (__lt__) """
        self.assertTrue(l1 < l2)
        self.assertFalse(l2 < l1)
        
    def test_line_calcT(self):
        """ checks if point located at correct distance from start (calcT) """
        self.assertTrue(l1.calcT(p2) == 1.0)
        
    def test_line_translate(self):
        """ checks if line is translated correctly (translate) """
        self.assertTrue(l1.translate(1.0, 2.0, 1.0) ==
                        Line(Point(2.0, 4.0, 4.0), Point(3.0, 6.0, 7.0)))
        
    def test_line_rotate(self):    
        """ checks if line is rotated correctly (rotate) """
        self.assertTrue(l1.rotate(np.pi/2, Point(0,0)) == 
                        Line(Point(-2.0, 1.0, 3.0), Point(-4.0, 2.0, 6.0)))
        
    def test_line_bounding_boxes(self):
        """ checks if bounding boxes of two lines intersect """
        self.assertTrue(l1.doBoundingBoxesIntersect(l2) == True)
        self.assertFalse(l1.doBoundingBoxesIntersect(l2) != True)
        
    def test_line_point_to_line_distance(self):
        """ checks the distance between point and line (pointToLineDist) """
        self.assertAlmostEqual(l1.pointToLineDist(p4), 1.7889, places = 4)
        
    def test_get_offset_line(self):    
        """ checks if correct offset line returned (getOffsetLine) """
        self.assertTrue(l4.getOffsetLine(4) == 
                Line(Point(-4.0, 0.0, 0.0), Point(-4.0, 8.0, 0.0)))
        
    def test_get_area(self):
        """ checks if area of triangle is correct (getArea) """
        self.assertAlmostEqual(l1.getArea(p1, p2, p4), 1.0000, places = 4)
        
    def test_are_colinear(self):
        """ checks if two lines are colinear (areColinear) """
        self.assertTrue(l1.areColinear(l2) == True)
        self.assertFalse(l1.areColinear(l2) != True)
        
    def test__side_of_line(self):
        """ unsure about precise description """
        self.assertTrue(l1.sideOfLine(p4) == 1)
        
    def test_do_lines_intersect(self):
        """ checks if lines intersect and returns nature of intersection """
        self.assertTrue(l4.segmentsIntersect(l5) == 
                        (1, Point(0, 6, 0)))
        
    def test_line_upper_left(self):
        """ checks if upper left point of line is correct """
        self.assertTrue(l4.upperLeft == Point(0.0, 8.0, 0.0))

    def test_line_lower_right(self):
        """ checks if lower right point of line is correct """
        self.assertTrue(l4.lowerRight == Point(0.0, 0.0))
        
    
        
def main():
    unittest.main()
      
if __name__ == '__main__':
    main()