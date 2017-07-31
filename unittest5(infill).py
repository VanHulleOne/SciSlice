# -*- coding: utf-8 -*-
"""
Created on Mon Jul 24 15:35:34 2017

@author: siddhant
"""

import unittest
from point import Point
from line import Line
from outline import Outline
from infill import Infill

class InfillTestCase(unittest.TestCase):
    
    def test_infill_extend_design(self):
        
        outline1 = Outline()
        outline1.append(Line(Point(0,0), Point(4,0)))
        outline1.append(Line(Point(4,0), Point(4,4)))
        outline1.append(Line(Point(4,4), Point(0,4)))
        outline1.append(Line(Point(0,4), Point(0,0)))
   
        d = [Line(Point(0,0), Point(2,0))]
        
        i1 = Infill(outline1, 0.5, 0, design = d, testMode = True)
        #print(i1.design)
        i1.extendDesign()
        #print(i1.design[3])
        self.assertTrue(i1.design[1] == Line(Point(2,0), Point(4,0)))
        
    def test_infill_create_design(self):
        """ checks if resulting infill design has expected modified path width """    
        outline1 = Outline()
        outline1.append(Line(Point(0,0), Point(4,0)))
        outline1.append(Line(Point(4,0), Point(4,4)))
        outline1.append(Line(Point(4,4), Point(0,4)))
        outline1.append(Line(Point(0,4), Point(0,0)))
   
        d = [Line(Point(0,0), Point(2,0))]
        
        i1 = Infill(outline1, 0.5, 0, design = d, testMode = True)
        i1.createField()
        self.assertTrue(i1.design[1] == Line(Point(0,0.5), Point(2,0.5)))
        
    def test_infill_centre_and_rotate(self):
       
        outline1 = Outline()
        outline1.append(Line(Point(0,0), Point(4,0)))
        outline1.append(Line(Point(4,0), Point(4,4)))
        outline1.append(Line(Point(4,4), Point(0,4)))
        outline1.append(Line(Point(0,4), Point(0,0)))
   
        d = [Line(Point(0,0), Point(2,0))]
        
        i1 = Infill(outline1, 0.5, 0, design = d, testMode = True)
        i1.centerAndRotateField()
        self.assertTrue(i1.design[0] == Line(Point(1,2), Point(3,2)))
        
    def test_infill_trim(self):
        
        outline1 = Outline()
        outline1.append(Line(Point(0,0), Point(4,0)))
        outline1.append(Line(Point(4,0), Point(4,4)))
        outline1.append(Line(Point(4,4), Point(0,4)))
        outline1.append(Line(Point(0,4), Point(0,0)))
   
        d = [Line(Point(0,0), Point(2,0))]
        
        i1 = Infill(outline1, 0.5, 0, design = d, testMode = True)
        i1.trimField()
        self.assertTrue(i1.design[0] == d[0])
        
def main():
    unittest.main()
      
if __name__ == '__main__':
    main()
    