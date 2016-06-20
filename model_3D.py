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

x = []
y = []
z = []
for entry in data:
    tempx = []
    tempy = []
    tempz = []
    tempx.append(entry[0])
    tempx.append(entry[3])
    tempy.append(entry[1])
    tempy.append(entry[4])
    tempz.append(entry[2])
    tempz.append(entry[5])
    x.append(tempx)
    x.append(tempx)
    y.append(tempy)
    y.append(tempy)
    z.append(tempz)
    z.append(tempz)
    
for num in range(0,len(x)):
    ax.plot_wireframe(x[num], y[num], z[num])
    
plt.show()
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