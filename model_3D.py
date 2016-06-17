# -*- coding: utf-8 -*-
"""
Created on Thu Jun 16 17:57:12 2016

@author: adiebold
"""

from mpl_toolkits.mplot3d import axes3d
import matplotlib.pyplot as plt

fig = plt.figure()
ax = fig.add_subplot(111, projection='3d'
)
data = []
with open("data_points.txt", 'r') as f:
    for line in f:
        data.append(line)   
    
for x in range(0,len(data)):   
    data[x] = data[x].replace("[", "")
    data[x] = data[x].replace("]", "")
    data[x] = data[x].replace("'", "")
    data[x] = data[x].replace(" ", "")
    data[x] = data[x].replace("\n", "")
    data[x] = data[x].split(",")
    for y in range(0,len(data[x])):
        data[x][y] = float(data[x][y])

for entry in data:
    x = []
    y = []
    z = []
    print(entry)
    #for coord in entry:
        #print(coord)
        #x.append(float(coord[0].replace("[","")))
        #y.append(float(coord[1].replace("[","")))
        #z.append(float(coord[2].replace("[","")))
    #for thing in x: 
        #print(thing)
    #print(type(entry))
    
    #ax.plot_wireframe(x,y,z)
    
#plt.show()

    
#plt.plot([1,2,3],[5,7,4])

#plt.show()