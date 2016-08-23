# -*- coding: utf-8 -*-
"""
Created on Mon Aug 22 16:11:01 2016

@author: adiebold
"""

import pygame
import pickle

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

    def scale(self, centre_x, centre_y, scale):
        """ Scale the wireframe from the centre of the screen """

        for node in self.nodes:
            node.x = centre_x + scale * (node.x - centre_x)
            node.y = centre_y + scale * (node.y - centre_y)
            node.z *= scale

key_to_function = {
    pygame.K_LEFT:   (lambda x: x.translateAll('x', -10)),
    pygame.K_RIGHT:  (lambda x: x.translateAll('x',  10)),
    pygame.K_DOWN:   (lambda x: x.translateAll('y',  10)),
    pygame.K_UP:     (lambda x: x.translateAll('y', -10)),
    pygame.K_EQUALS: (lambda x: x.scaleAll(1.25)),
    pygame.K_MINUS:  (lambda x: x.scaleAll( 0.8))}
            
class ProjectionViewer:
    """ Displays 3D objects on a Pygame screen """

    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.screen = pygame.display.set_mode((width, height))
        pygame.display.set_caption('Wireframe Display')
        self.background = (10,10,50)

        self.wireframes = {}
        self.displayNodes = True
        self.displayEdges = True
        self.nodeColour = (255,255,255)
        self.edgeColour = (200,200,200)
        self.nodeRadius = 1

    def addWireframe(self, name, wireframe):
        """ Add a named wireframe object. """

        self.wireframes[name] = wireframe

    def run(self):
        """ Create a pygame screen until it is closed. """

        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
#                    pygame.display.quit()
                    pygame.quit()
                    
                elif event.type == pygame.KEYDOWN:
                    if event.key in key_to_function:
                        key_to_function[event.key](self)
                    
            self.display()  
            pygame.display.flip()
        
    def display(self):
        """ Draw the wireframes on the screen. """

        self.screen.fill(self.background)

        for wireframe in self.wireframes.values():
            if self.displayEdges:
                for edge in wireframe.edges:
                    pygame.draw.aaline(self.screen, self.edgeColour, (edge.start.x, edge.start.y), (edge.stop.x, edge.stop.y), 1)

            if self.displayNodes:
                for node in wireframe.nodes:
                    pygame.draw.circle(self.screen, self.nodeColour, (int(node.x), int(node.y)), self.nodeRadius, 0)
                    
    def translateAll(self, axis, d):
        """ Translate all wireframes along a given axis by d units. """

        for wireframe in self.wireframes.values():
            wireframe.translate(axis, d)

    def scaleAll(self, scale):
        """ Scale all wireframes by a given scale, centred on the centre of the screen. """

        centre_x = self.width/2
        centre_y = self.height/2

        for wireframe in self.wireframes.values():
            wireframe.scale(centre_x, centre_y, scale)
    
if __name__ == '__main__':
    
    data = pickle.load(open('data_points', 'rb'))
    xar = []
    yar = []
    zar = []
    for line in data:
        for point in line:
            xar.append(point[0])
            yar.append(point[1])
            zar.append(point[2])
            
#    print([(xar[c],yar[c],zar[c]) for c in range(len(xar))])
#    print([(n,n+1) for n in range(0,len(xar),2)])    
#    print('len nodes: ', len([(xar[c],yar[c],zar[c]) for c in range(len(xar))]))
#    print('len endges: ', len([(n,n+1) for n in range(0,len(xar),2)]))
#    print('len data: ', len(data))
#    print('len xar: ', len(xar))
            
#    print(data)
            
    real = True
    
#    real = False
    
    pv = ProjectionViewer(400, 300)
    cube = Wireframe()
    
    if real:
        cube.addNodes([(xar[c],yar[c],zar[c]) for c in range(len(xar))])
        cube.addEdges([(n,n+1) for n in range(0,len(xar),2)])
    else:
        cube.addNodes([(x,y,z) for x in (50,250) for y in (50,250) for z in (50,250)])
        cube.addEdges([(n,n+4) for n in range(0,4)]+[(n,n+1) for n in range(0,8,2)]+[(n,n+2) for n in (0,1,4,5)])
    
    pv.addWireframe('cube', cube)
    pv.run()

    cube.addNodes([(x,y,z) for x in (50,250) for y in (50,250) for z in (50,250)])
    cube.addEdges([(n,n+4) for n in range(0,4)]+[(n,n+1) for n in range(0,8,2)]+[(n,n+2) for n in (0,1,4,5)])
    
#    print(len(data))
#    print(len([(xar[c],yar[c],zar[c]) for c in range(len(xar))]))
#    print(len([(n,n+1) for n in range(0,len(data),2)]))
    
    
    
#    