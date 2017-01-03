# -*- coding: utf-8 -*-
"""
Created on Fri Dec 23 14:11:50 2016

@author: Luke Van Hulle
"""

import trimesh
import matplotlib.pyplot as plt
from parameters import Parameters
import json
from collections import namedtuple
import figura as fg
from gcode import Gcode
import time
from outline import Outline, Section

path = 'C:\\Users\\lvanhulle\\Google Drive\\School\\Research\\Optimize\\volFrac0.5 3Directions\\'
zero = 'C-Bracket_0.50_0.stl'
minus45 = 'C-Bracket_0.50_minus45.stl'
plus45 = 'C-Bracket_0.50_plus45WithPlate.STL'
paramFile = 'Print1.json'

fnames = (zero, minus45, plus45)
colors = 'rgb'
angles = (0, -45, 45)

SecAng = namedtuple('SecAng', 'section angle')

secAngs = []
meshes = []

with open(path + paramFile, 'r') as fp:
    data = json.load(fp)
    
params = Parameters(data[0], data[1])


for fname, color, angle in zip(fnames, colors, angles):
    mesh = trimesh.load_mesh(path+fname)
    meshes.append(mesh)
    section = mesh.section(plane_origin=[0,0,0.01],plane_normal=[0,0,1])
    loops = section.discrete
    for loop in loops:
        outline = Outline()
        outline._name = fname
        outline.addCoordLoop(loop*1000) # 1000 to convert from meters to mm
        outline = outline.translate(-50, -12)
        secAngs.append(SecAng(Section(outline), angle))
        plt.plot(loop[:,0]-0.050, loop[:,1]-0.012, color)

params.outline = [tuple(secAngs)]
gCode = Gcode(params)

plt.show()

def run():
    startTime = time.time()
    print('\nGenerating code, please wait...')
    fig = fg.Figura(params, gCode)

    with open(path + params.outputFileName, 'w') as f:
        for string in fig.masterGcode_gen():
            f.write(string)
    
    endTime = time.time()
    print('\nCode generated.')
    print('Done writting: ' + params.outputFileName + '\n')
    print('{:.2f} total time'.format(endTime - startTime)) 
    
if __name__ == '__main__':
    run()