# -*- coding: utf-8 -*-
"""
Created on Mon Aug 22 13:56:44 2016

@author: adiebold
"""

import math

class Node:
    def __init__(self, coordinates):
        self.x = coordinates[0]
        self.y = coordinates[1]
        self.z = coordinates[2]
        
class Edge:
    def __init__(self, start, stop):
        self.start = start
        self.stop  = stop

class Wireframe:
    def __init__(self):
        self.nodes = []
        self.edges = []

    def addNodes(self, nodeList):
        for node in nodeList:
            self.nodes.append(Node(node))

    def addEdges(self, edgeList):
        for (start, stop) in edgeList:
            self.edges.append(Edge(self.nodes[start], self.nodes[stop]))

    def outputNodes(self):
        print("\n --- Nodes --- ")
        for i, node in enumerate(self.nodes):
            print(" %d: (%.2f, %.2f, %.2f)" % (i, node.x, node.y, node.z))
            
    def outputEdges(self):
        print("\n --- Edges --- ")
        for i, edge in enumerate(self.edges):
            print(" %d: (%.2f, %.2f, %.2f)" % (i, edge.start.x, edge.start.y, edge.start.z),)
            print("to (%.2f, %.2f, %.2f)" % (edge.stop.x,  edge.stop.y,  edge.stop.z))

    def translate(self, axis, d):
        """ Add constant 'd' to the coordinate 'axis' of each node of a wireframe """
        
        if axis in ['x', 'y', 'z']:
            for node in self.nodes:
                setattr(node, axis, getattr(node, axis) + d)

    def scale(self, center_x, center_y, scale):
        """ Scale the wireframe from the center of the screen """

        for node in self.nodes:
            node.x = center_x + scale * (node.x - center_x)
            node.y = center_y + scale * (node.y - center_y)
            node.z *= scale
            
    def findcenter(self):
        """ Find the center of the wireframe. """

        num_nodes = len(self.nodes)
        meanX = sum([node.x for node in self.nodes]) / num_nodes
        meanY = sum([node.y for node in self.nodes]) / num_nodes
        meanZ = sum([node.z for node in self.nodes]) / num_nodes

        return (meanX, meanY, meanZ)

    def rotateX(self, cx,cy,cz, radians):
        for node in self.nodes:
            y      = node.y - cy
            z      = node.z - cz
            d      = math.hypot(y, z)
            theta  = math.atan2(y, z) + radians
            node.z = cz + d * math.cos(theta)
            node.y = cy + d * math.sin(theta)

    def rotateY(self, cx,cy,cz, radians):
        for node in self.nodes:
            x      = node.x - cx
            z      = node.z - cz
            d      = math.hypot(x, z)
            theta  = math.atan2(x, z) + radians
            node.z = cz + d * math.cos(theta)
            node.x = cx + d * math.sin(theta)

    def rotateZ(self, cx,cy,cz, radians):        
        for node in self.nodes:
            x      = node.x - cx
            y      = node.y - cy
            d      = math.hypot(y, x)
            theta  = math.atan2(y, x) + radians
            node.x = cx + d * math.cos(theta)
            node.y = cy + d * math.sin(theta)