# -*- coding: utf-8 -*-
"""
Created on Thu Jun 16 17:57:12 2016

@author: adiebold
"""

from tkinter import *

from mpl_toolkits.mplot3d import axes3d
import matplotlib.pyplot as plt

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
    
class Three_D:
    
    def __init__(self, start, end, x, y, z):
        fig = plt.figure()
        ax = fig.add_subplot(111, projection='3d')
        
        
        colors = []
        color_num = ['0','2','4','6','8','A','C','E']
        for one in color_num:
            for two in color_num:
                for three in color_num:
                    for four in color_num:
                        for five in color_num:
                            for six in color_num:
                                curr_color = '#' + one + two + three + four + five + six
                                colors.append(curr_color)
            
        for num in range(start, end):
            num_color = num%len(colors)
            ax.plot_wireframe(x[num], y[num], z[num], color=colors[num_color])
            
        plt.show()
        
def error_box():
        
    popup = Tk()
    popup.title("Error")
    
    msg = Label(popup, text="Error: End value cannot be less than Start value")
    msg.pack(side="top", fill="x", pady=10)
    
    buttonDismiss = Button(popup, text="Dismiss", command = popup.destroy)
    buttonDismiss.pack()
    
    popup.mainloop()
        
def create_plot(start, end, x, y, z):
    if(end >= start):
        model = Three_D(start, end, x, y, z)
    else:
        error_box()
        
    
root = Tk()

root.title("3D Model")

labelPoints = Label(root, text="Choose the start and end numbers of the graph")
labelPoints.pack()

labelStart = Label(root, text="Start")
labelStart.pack(side=LEFT)

scaleStart = Scale(root, from_=0, to=len(x))
scaleStart.pack(side=LEFT)

labelEnd = Label(root, text="End")
labelEnd.pack(side=LEFT)

scaleEnd = Scale(root, from_=0, to=len(x))
scaleEnd.pack(side=LEFT)

buttonSubmit = Button(text="Create Graph", command=lambda: create_plot(scaleStart.get(), scaleEnd.get(), x, y, z))
buttonSubmit.pack()













root.mainloop()