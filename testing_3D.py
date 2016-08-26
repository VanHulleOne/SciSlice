# -*- coding: utf-8 -*-
"""
Created on Mon Aug 22 16:11:01 2016

@author: adiebold
"""

import math
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
            
    def findCentre(self):
        """ Find the centre of the wireframe. """

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


key_to_function = {
    pygame.K_LEFT:   (lambda x: x.translateAll('x',  20)),
    pygame.K_RIGHT:  (lambda x: x.translateAll('x', -20)),
    pygame.K_DOWN:   (lambda x: x.translateAll('y', -20)),
    pygame.K_UP:     (lambda x: x.translateAll('y',  20)),
    pygame.K_2:      (lambda x: x.scaleAll(1.25)),
    pygame.K_1:      (lambda x: x.scaleAll( 0.8)),
    pygame.K_q:      (lambda x: x.rotateAll('X',  0.1)),
    pygame.K_w:      (lambda x: x.rotateAll('X', -0.1)),
    pygame.K_a:      (lambda x: x.rotateAll('Y',  0.1)),
    pygame.K_s:      (lambda x: x.rotateAll('Y', -0.1)),
    pygame.K_z:      (lambda x: x.rotateAll('Z',  0.1)),
    pygame.K_x:      (lambda x: x.rotateAll('Z', -0.1)),
    pygame.K_3:      (lambda x: x.shift_up()),
    pygame.K_e:      (lambda x: x.add()),
    pygame.K_d:      (lambda x: x.subtract()),
    pygame.K_c:      (lambda x: x.shift_down()),}
    
            
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
        
        self.layer_part = pickle.load(open('layer_part', 'rb'))
        print(self.layer_part[0])
        print(self.layer_part[len(self.layer_part)-1])
        
        self.MODEL = 'model'
        self.start = 0
        self.end = 0
        self.first = True

    def addWireframe(self, name, wireframe):
        """ Add a named wireframe object. """

        self.wireframes[name] = wireframe

    def run(self):
        """ Create a pygame screen until it is closed. """
        pygame.init()
        self.myfont = pygame.font.SysFont("monospace", 15)
        
        self.translateAll('x', (400-self.wireframes['model'].findCentre()[0]))
        self.translateAll('y', (300-self.wireframes['model'].findCentre()[1]))
        self.scaleAll(2.5)
        
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
#                    pygame.display.quit()
                    pygame.quit()
                    
                elif event.type == pygame.KEYDOWN:
                    if event.key in key_to_function:
                        key_to_function[event.key](self)
                        
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    if event.button == 4:
                        self.scaleAll(1.25)
                    if event.button == 5:
                        self.scaleAll(0.8)
                    
            self.display()  
            pygame.display.flip()        
        
    def display(self):
        """ Draw the wireframes on the screen. """

        self.screen.fill(self.background)

        text = "Showing Part " + self.layer_part[self.start][1] + " Layer " + self.layer_part[self.start][0]
        text += " through Part " + self.layer_part[self.end][1] + " Layer " + self.layer_part[self.end][0]
        text += "  (" + str(self.end - self.start + 1) + " layers total)"
        label = self.myfont.render(text, 1, (255,255,0))
        self.screen.blit(label, (0, 0))
        
        instructions = []
        instruct_label = []
        
        instructions.append("1/2 = zoom in/out | q/w = rotate X-axis | a/s = rotate Y-axis | z/x = rotate Z-axis")
        instruct_label.append(self.myfont.render(instructions[0], 1, (255,255,0)))
        self.screen.blit(instruct_label[0], (0, 25))
        
        instructions.append("e/d = add/subtract layers | 3/c = shift layers up/down")
        instruct_label.append(self.myfont.render(instructions[1], 1, (255,255,0)))
        self.screen.blit(instruct_label[1], (0,50))
        
        wireframe = self.wireframes[self.MODEL]
        if self.displayEdges:
            if self.first:
                self.end = len(self.layer_part)-1
                self.first = False
                print(len(self.wireframes[self.MODEL].edges))
                print(self.layer_part[self.start][2])
                print(self.layer_part[self.end][3])
            for edge in wireframe.edges[self.layer_part[self.start][2]:self.layer_part[self.end][3]]:
                pygame.draw.line(self.screen, self.edgeColour, (edge.start.x, edge.start.y), (edge.stop.x, edge.stop.y), 1)#width
                    
    def translateAll(self, axis, d):
        """ Translate all wireframes along a given axis by d units. """

        wireframe = self.wireframes[self.MODEL]
        wireframe.translate(axis, d)

    def scaleAll(self, scale):
        """ Scale all wireframes by a given scale, centred on the centre of the screen. """

        centre_x = self.width/2
        centre_y = self.height/2

        wireframe = self.wireframes[self.MODEL]
        wireframe.scale(centre_x, centre_y, scale)
            
    def rotateAll(self, axis, theta):
        """ Rotate all wireframe about their centre, along a given axis by a given angle. """

        rotateFunction = 'rotate' + axis

        wireframe = self.wireframes[self.MODEL]
        centre = wireframe.findCentre()
        getattr(wireframe, rotateFunction)(centre[0], centre[1], centre[2], theta)
            
    def add(self):
        """ Increases the amount of layers shown. """
        
        if self.end < (len(self.layer_part)-1):
            self.end += 1
        elif self.start > 0:
            self.start -= 1  
        else:
            print('Showing all parts and layers.')
            
    def subtract(self):
        """ Decreases the amount of layers shown. """
        
        if self.end > (self.start):
            self.end -= 1
            
        else:
            print('Showing one layer of one part already.')
            print(self.start)
            print(self.end)
            
    def shift_up(self):
        """ Shifts the layers being viewed up by one. """
        
        if self.end < (len(self.layer_part)-1):
            self.start += 1
            self.end += 1
        else:
            print('Showing the topmost layers already.')
            
    def shift_down(self):
        """ Shifts the layers being viewed down by one. """
        
        if self.start > 0:
            self.start -= 1
            self.end -= 1
        else:
            print('Showing the lowest layers already.')
        
    
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
    
    pv = ProjectionViewer(800, 600)
    model = Wireframe()
    
    model.addNodes([(xar[c],yar[c],zar[c]) for c in range(len(xar))])
    model.addEdges([(n,n+1) for n in range(0,len(xar),2)])
    
    pv.addWireframe('model', model)
    pv.run()
    