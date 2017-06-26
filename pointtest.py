# -*- coding: utf-8 -*-
"""
Created on Mon Jun 26 13:53:41 2017

@author: siddhant
"""

import unittest
from point import Point
#from point import __lt__
#from point import __gt__
#from point import __neg__
from point import __eq__

p1 = Point(1.0, 2.0, 3.0)

class PointTestCase (unittest.TestCase):
   # p1 = Point(1.0, 2.0, 0.0)
    
    def test_point_negative(self):
        self.assertTrue(__neg__(p1) == Point(-1.0, -2.0, 3.0))
        #self.assertTrue(p1.__neg__ == Point(-1.0, -2.0, 3.0))
        
    #def test_point_greater(self):
     #   self.assertFalse(__gt__((7, 8, 9)) == False)
        
    def test_point_equal(self):
       self.assertEqual(__eq__(p1, (1.0, 2.0, 3.0)))

def main():
    unittest.main()
      
if __name__ == '__main__':
    main()