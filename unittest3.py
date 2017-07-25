# -*- coding: utf-8 -*-
"""
Created on Fri Jul  7 14:33:12 2017

@author: siddhant
"""

import unittest
from point import Point
#from line import Line
#from linegroup import LineGroup
from arc import Arc
import matrixTrans as mt
import constants as c

class ArcTestCase(unittest.TestCase):
    
    def test_arc_calc_inner_angle(self):
        """ checks if inner angle between given points is correct """
        a = Arc(Point(1,1,0), Point(4,4,0), c.X, Point(1,3,0))
        ang = a.calcIncludedAngle(Point(1,1,0), Point(4,4,0))
        self.assertAlmostEqual(ang, 4.2426, 4)
        
    def test_arc_to_lines(self):
        """ checks if line segments double when function called (arcToLines) """
        a = Arc(Point(1,1,0), Point(4,4,0), c.X, Point(1,3,0))
        len1 = len(a)
        
        a.arcToLines()
        len2 = len(a)
        
        self.assertTrue(len2 == 2*len1)
        
class MatrixTestCase(unittest.TestCase):
        
    def test_matrix_mirror(self):
        """ checks if the matrix is mirrored correctly about given axis """
        self.assertTrue(tuple(mt.mirrorMatrix(c.X)[0]) == (1,0,0,0))
        self.assertTrue(tuple(mt.mirrorMatrix(c.X)[1]) == (0,-1,0,0))
        self.assertTrue(tuple(mt.mirrorMatrix(c.X)[2]) == (0,0,1,0))
        self.assertTrue(tuple(mt.mirrorMatrix(c.X)[3]) == (0,0,0,1))
        
    def test_matrix_translate(self):
        """ checks if the matrix is translated correctly """
        self.assertTrue(tuple(mt.translateMatrix(2,3)[0]) == (1,0,0,2))
        self.assertTrue(tuple(mt.translateMatrix(2,3)[1]) == (0,1,0,3))
        self.assertTrue(tuple(mt.translateMatrix(2,3)[2]) == (0,0,1,0))
        self.assertTrue(tuple(mt.translateMatrix(2,3)[3]) == (0,0,0,1))
        
    def test_matrix_rotate(self):
        """ checks if the matrix is rotated correctly """
        self.assertTrue(tuple(mt.rotateMatrix(0)[0]) == (1,0,0,0))
        self.assertTrue(tuple(mt.rotateMatrix(0)[1]) == (0,1,0,0))
        self.assertTrue(tuple(mt.rotateMatrix(0)[2]) == (0,0,1,0))
        self.assertTrue(tuple(mt.rotateMatrix(0)[3]) == (0,0,0,1))
 
    def test_matrix_scale(self):
        """ checks if the matrix is scaled accordingly """
        self.assertTrue(tuple(mt.scale(5,4)[0]) == (5,0,0,0))
        self.assertTrue(tuple(mt.scale(5,4)[1]) == (0,4,0,0))
        self.assertTrue(tuple(mt.scale(5,4)[2]) == (0,0,1,0))
        self.assertTrue(tuple(mt.scale(5,4)[3]) == (0,0,0,1))
        
    def test_matrix_combine_transformations(self):
        """ checks if dot product with matrix list is correct """
        ml = [[1,2,3,4],[5,6,7,8]]
        self.assertTrue(mt.combineTransformations(ml) == 70)
        
def main():
    unittest.main()
      
if __name__ == '__main__':
    main()
    
        

