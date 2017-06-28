# -*- coding: utf-8 -*-
"""
Created on Mon Jun 26 13:53:41 2017

@author: siddhant
"""

import unittest
from point import Point
import constants as c
from line import Line


p1 = Point(1.0, 2.0, 3.0)
p2 = Point(2.0, 4.0, 6.0)
l1 = Line(p1, p2)
p3 = Point(1.0, 2.0, 3.0)
p4 = Point(6.0, 12.0, 18.0)
l2 = Line(p3, p4)

class PointTestCase (unittest.TestCase):
   
   
    
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
        self.assertTrue(p1[1:2] == [2.0])
      
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
        self.assertAlmostEqual(p2 - p1, 3.74, places = 2)
        
    def test_fliped(self):
        """ check if line flips direction as expected """
        self.assertEqual(l1.fliped(), Line(p2, p1))
        
    def test_on_line(self):
        """ checks if given point is on line (isOnLine) """
        self.assertTrue(l1.isOnLine(p2) == True)

    def test_mirror_line(self):
        """ check if line mirrored correctly about given axis """
        self.assertTrue(l1.mirror(c.X) == Line(Point(1.0, -2.0, 3.0), Point(2.0, -4.0, 6.0)))
    
    def test_lines_parallel(self):
        """ checks if the lines are parallel (areParallel) """
        self.assertTrue(l1.areParallel(l2) == True)

def main():
    unittest.main()
      
if __name__ == '__main__':
    main()