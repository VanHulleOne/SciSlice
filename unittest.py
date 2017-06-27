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
   
   
    #check if point is equal to given point (__eq__)
    def test_point_equal(self):
        self.assertEqual(p1, Point(1.0, 2.0, 3.0))
     
    #check points are not equal (__ne__)   
    def test_point_notequal(self):
        self.assertFalse(p1 == Point(1.0, 2.0, 8.0))
    
    #check if point negative is correct (__neg_)
    def test_point_negative(self):
        self.assertTrue(-p1 == Point(-1.0, -2.0, 3.0))
        
    #compare two points to check lesser (__lt__)
    def test_point_lesser(self):
        self.assertTrue(p1 < Point(2.0, 4.0, 6.0))
     
    #compare two points to check greater (__gt__)   
    def test_point_greater(self):
        self.assertFalse(p1 > Point(1.0, 2.0, 6.0))
        
    #check distance between two points (__sub__)  
    def test_point_sub(self):
        self.assertAlmostEqual(p2-p1, 3.74, places = 2)
        
    #check if x-coordinate matches    
    def test_initial_x_property(self):
        self.assertTrue(p1.x == 1.0)
        
    #check if y-coordinate matches    
    def test_initial_y_propert(self):
        self.assertTrue(p2.y == 4.0)
        
    #check if z-coordinate matches    
    def test_initial_z_property(self):
        self.assertTrue(p1.z == 3.0)
    
    #check if correct coordinate is returned    
    def test_get_item(self):
        self.assertTrue(p1[0] == 1.0)
      
    #check squared distance between two points (squaredDistance)
    def test_squaredistance(self):
        self.assertTrue(((p1[0] - p2[0])**2 + (p1[1] - p2[1])**2) == 5.0)
      
    #check if point correctly mirrored about axis (mirror)
    def test_point_mirror(self):
        self.assertTrue(p1.mirror(c.X) == Point(1.0, -2.0, 3.0))
    
    #check if point translates correctly  (translate)
    def test_point_translate(self):
        self.assertTrue(p1.translate(1.0, 2.0) == Point(2.0, 4.0, 3.0))
     
    #check if point rotates as expected    (rotate)
    def test_point_rotate(self):
        self.assertTrue(p1.rotate(0) == Point(1.0, 2.0, 3.0))
        
class LineTestCase(unittest.TestCase):
    
    #checks length of the line (length)
    def test_length(self):
        self.assertAlmostEqual(p2 - p1, 3.74, places = 2)
        
   # def test_fliped(self):
     #   self.assertEqual(l1.fliped, Line(p2, p1))
        
    #checks if given point is on line (isOnLine)
    def test_on_line(self):
        self.assertTrue(l1.isOnLine(p2) == True)

   # def test_mirror_line(self):
    #    self.assertTrue(l1.mirror(c.X) == Line((1.0, -2.0, 3.0), (2.0, -4.0, 6.0)))
    
    #checks if the lines are parallel (areParallel)
    def test_lines_parallel(self):
        self.assertTrue(l1.areParallel(l2) == True)

def main():
    unittest.main()
      
if __name__ == '__main__':
    main()