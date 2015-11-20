# -*- coding: utf-8 -*-
"""
Created on Thu Nov 19 16:45:00 2015

@author: lvanhulle
"""

class Figura():
    
    def __init__(self, layer, zStep, numLayers):
        self.layers = [layer.translate(0, 0, zStep*currentLayer) for currentLayer in range(numLayers)]
    
    