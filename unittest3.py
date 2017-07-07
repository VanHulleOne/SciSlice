# -*- coding: utf-8 -*-
"""
Created on Fri Jul  7 14:33:12 2017

@author: siddhant
"""

import unittest
from point import Point
from line import Line
from linegroup import LineGroup
from arc import Arc
import matrixTrans as mt
import constants as c
import math
import numpy as np
#from shapely.geometry.polygon import Polygon
#from shapely.ops import cascaded_union
#from outline import Outline

class ArcTestCase(unittest.TestCase):
    
    def test_arc_calc_inner_angle(self):
        """ checks if inner angle between given points is correct """
        a = Arc(Point(1,1,0), Point(4,4,0), c.X, Point(1,3,0))
        ang = a.calcIncludedAngle(Point(1,1,0), Point(4,4,0))
        self.assertAlmostEqual(ang, 4.2426, 4)
        
#    def test_ok(self):
#        pass
#class MatrixTestCase(unittest.TestCase):
#    
#    def test_matrix_translate(self):
#        
#        m = np.arange(1,17).reshape(4,4)
#        print(m.t)
        
def main():
    unittest.main()
      
if __name__ == '__main__':
    main()
    
        

