# -*- coding: utf-8 -*-
'''
Created on Sat May 28 16:39:58 2016
@author: Alex Diebold
'''

import sys
import os

pathway = os.path.dirname(os.path.realpath(__file__)).split(sep='\\')
pathway[-1] = 'DogBone'
pathway = '\\'.join(pathway)

sys.path.append(pathway)
import constants as c
import matplotlib                   #for 3D model
from collections import namedtuple

#if using the Spyder console, matplotlib is already imported and the backend cannot be changed with .use() as is needed
#to change the backend to TkAgg, go to Tools > Preferences > Console > External modules > Matplotlib GUI backend
#be sure to mind the caps in TkAgg
'''
backend = matplotlib.get_backend()
if backend != 'TkAgg' and backend != 'module://ipykernel.pylab.backend_inline':
    matplotlib.use('TkAgg')             #backend of matplotlib, used for putting in GUI
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2TkAgg
from matplotlib.figure import Figure
'''
from mpl_toolkits.mplot3d import axes3d
import matplotlib.pyplot as plt
import matplotlib.animation as animation

from tkinter import *               #GUI module
from tkinter import ttk             #for styling purposing
from tkinter import filedialog      #window for saving and uploading files
import json                         #for saving and uploading files
from main import Main        #for converting to Gcode
from parameters import __version__ as version
import doneShapes as ds
import inspect

import pygame
from pygame.locals import *

from OpenGL.GL import *
from OpenGL.GLU import *

class GUI(Tk):

    def __init__(self, *args, **kwargs):
        Tk.__init__(self, *args, **kwargs)
        
        Tk.iconbitmap(self, 'UW_Madison_icon.ico')
        Tk.title(self, '3D Printer Parameter Setter')
        #format window size -- width=450, height=475, 100px from left of screen, 100px from top of screen
        #Tk.geometry(self, '450x475+100+100')
        
        #set up frame
        self.container = Frame(self)
        self.container.pack(side='top', fill='both', expand=True)
        self.container.grid(row=0,column=0)
        
        #create menubar
#        menubar = Menu(container)
#        filemenu = Menu(menubar, tearoff=0)
#        filemenu.add_command(label='Save', command=lambda: Page_Variables.save(Page_Variables))
#        filemenu.add_command(label='Upload', command=lambda: Page_Variables.upload(Page_Variables))
#        menubar.add_cascade(label='File', menu=filemenu)
#        
#        Tk.config(self, menu=menubar)
        
        #dictionary of Frames
        self.frames = {}
        
        self.shapes = {Page_Variables : '425x750+150+100',       
                       Page_Model : '600x500+150+100'}
        
        #add Frames to dictionary
        for F in (Page_Variables,):
        
            frame = F(self.container, self)
            
            self.frames[F] = frame
            
            frame.grid(row=0, column=0, sticky='nsew')
            
#        frame = Page_Variables(self.container, self)
#        self.frames[Page_Variables] = frame
#        frame.grid(row=0, column=0, sticky='nsew')
            
        
        #show initial Frame
        Tk.geometry(self, self.shapes[Page_Variables])
        self.show_frame(Page_Variables)
       
    #show frame
    def show_frame(self, cont, delete=False, cont_to_del = None):
        
        if cont not in self.frames:
            frame = cont(self.container, self)
            self.frames[cont] = frame
            frame.grid(row=0, column=0, sticky='nsew')
            
        Tk.geometry(self, self.shapes[cont])        
        frame = self.frames[cont]
        frame.tkraise() 
        
        if delete:
            del self.frames[cont_to_del]
        
class Page_Variables(Frame):
    
    COMMON = 0
    PART = 1
    LAYER = 2
    FILE = 3
    PRINT = 4
    PRINTER = 5
    
    INT_LIST = 0
    FLOAT_LIST = 1
    
    Menu = namedtuple('Menu', 'name group')
    menus = [
            Menu('Common', COMMON),
            Menu('Part', PART),
            Menu('Layer', LAYER),
            Menu('File', FILE),
            Menu('Print', PRINT),
            Menu('Printer', PRINTER)
            ]

    menus.sort(key=lambda x : x.group)             

             
    Par = namedtuple('Parameter', 'label data_type groups')
    parameters = [
                Par('outline', str, (COMMON, PART)),
                Par('stl_file', str, (COMMON, PART)),
                Par('solidityRatio', FLOAT_LIST, (COMMON, PART)),
                Par('printSpeed', INT_LIST, (COMMON, PART)),
                Par('shiftX', FLOAT_LIST, (COMMON, PART)),
                Par('shiftY', FLOAT_LIST, (COMMON, PART)),
                Par('firstLayerShiftZ', float, (PART,)),
                Par('numLayers', INT_LIST, (COMMON, PART)),
                Par('pattern', None, (PART,)),
                Par('designType', int, (PART,)),
                Par('infillAngleDegrees', FLOAT_LIST, (COMMON, LAYER)),
                Par('pathWidth', FLOAT_LIST, (LAYER,)),
                Par('layerHeight', FLOAT_LIST, (LAYER,)),
                Par('infillShiftX', FLOAT_LIST, (LAYER,)),
                Par('infillShiftY', FLOAT_LIST, (LAYER,)),
                Par('numShells', INT_LIST, (COMMON, LAYER)),
                Par('trimAdjust', FLOAT_LIST, (LAYER,)),
                Par('start_Gcode_FileName', str, (FILE,)),
                Par('end_Gcode_FileName', str, (FILE,)),
                Par('bed_temp', int, (COMMON, PRINT)),
                Par('extruder_temp', int, (COMMON, PRINT)),
                Par('nozzleDiameter', float, (PRINTER,)),
                Par('filamentDiameter', float, (PRINTER,)),
                Par('RAPID', int, (PRINTER,)),
                Par('TRAVERSE_RETRACT', float, (PRINTER,)),
                Par('MAX_FEED_TRAVERSE', float, (PRINTER,)),
                Par('MAX_EXTRUDE_SPEED', int, (PRINTER,)),
                Par('Z_CLEARANCE', float, (PRINTER,)),
                Par('APPROACH_FR', int, (PRINTER,)),
                Par('comment', str, (PRINTER,)),
                ]
                
    OUTPUTFILENAME = 'outputFileName'
    CURRPATH = os.path.dirname(os.path.realpath(__file__))
    GCODEPATH = CURRPATH + '\\Gcode\\'
    JSONPATH = CURRPATH + '\\JSON\\'
    OUTPUTSUBDIRECTORY = 'outputSubDirectory'
    
    def __init__(self, parent, controller):
        Frame.__init__(self, parent)
        self.controller = controller
        
        ########################
        #   class variables    #
        ########################
        
        #string that is the filename of the current file
        self.filename = ''
        
        #dictionary with variable name as key and StringVar as value
        self.text_variable = {} 
        
        #dictionary with variable name as key and Label as value        
        self.labels = {}
                   
        #dictionary with variable name as key and Entry as value
        self.entries = {}
        
        #array of Strings of the variables
        self.texts = [i.label for i in self.parameters]
               
        self.fields = []
        for menu in self.menus:
            self.fields.append([par for par in self.parameters if menu.group in par.groups])
           
        self.set_defaults()
        
        self.shift = 0
        self.current_menu = self.fields[self.COMMON]
            
        self.create_var_page()
              
    ##########################################################
    #   methods that create labels, entries, and/or buttons  #
    ##########################################################
    
    def set_defaults(self):
        
        defaults_path = self.JSONPATH + 'DEFAULT.json'   
        if os.path.isfile(defaults_path):
            with open(defaults_path, 'r') as fp:
                full_defaults = json.load(fp)
        else:
            self.defaults = {}
            
        self.defaults = full_defaults[0]
        var_defaults = full_defaults[1]
        if var_defaults:
            for key, value in var_defaults.items():
                self.var_saved[key] = value
            
        for key in self.texts:
            if key not in self.defaults:
                self.defaults[key] = ''
          
    #initial creation of labels
    def set_labels(self):        
        
        #create all labels
        for x in range(len(self.texts)):
            #create label
            self.labels[self.texts[x]] = ttk.Label(self, text=self.texts[x])
        
        for x, par in enumerate(self.fields[self.COMMON]):
            self.labels[par.label].grid(row=x+1,column=0)
        
        self.var_text_keys = StringVar(self)
        self.labelKeys = Label(self, textvariable=self.var_text_keys)
        self.var_text_values = StringVar(self)
        self.labelValues = Label(self, textvariable=self.var_text_values)

            
    #initial creation of entries
    def set_entries(self):

        for x, label in enumerate(self.texts):
            #create all StringVars
            self.text_variable[label] = StringVar(self, value=self.defaults[label])
            
            #create entry 
            self.entries[label] = ttk.Entry(self, textvariable=self.text_variable[label])  
        
        self.doneshapes_menu()
        
        #show commonly used variables
        for x, par in enumerate(self.fields[self.COMMON]):
            #use grid() after creating entry or dictionary value will be 'NoneType'
            self.entries[par.label].grid(row=x+1,column=1, sticky='ew')
            
        self.entries['stl_file'].config(state=DISABLED)
            
    def doneshapes_menu(self):
        
        doneshape_funcs = ['choose a shape']
        doneshape_funcs.append(c.STL_FLAG)
        for member in inspect.getmembers(ds, inspect.isfunction):
            doneshape_funcs.append(member[0])
        
        self.entries['outline'] = ttk.OptionMenu(self, self.text_variable['outline'], self.defaults['outline'], *doneshape_funcs, command=self.set_var)
        
    #creates button for saving all values
    def save_option(self): 
        
        #create button
        buttonSave = ttk.Button(self,text='Save',command=lambda: self.save()).grid(row=0,column=1)
    
    #creates label, entry, and button for uploading all values    
    def upload_option(self):   
        
        #create button
        buttonUpload = ttk.Button(self,text='Upload',command=lambda: self.upload()).grid(row=0,column=0)
        
    #create menu of label and buttons to switch between tabs
    def tab_buttons(self):
        
        #label for parameters
        labelParameters = ttk.Label(self,text='Parameters',font='-weight bold')
        labelParameters.grid(row=0,column=2)

        #button to display all variables
        buttonAll = ttk.Button(self,text='All',command=self.command(self.parameters))
        buttonAll.grid(row=1,column=2)
        
        for x, menu in enumerate(self.menus):
            button = ttk.Button(self, text=menu.name, command=self.command(self.fields[menu.group]))
            button.grid(row=2+x, column=2)
            
    def command(self, params):
        def inner_command():
            self.current_menu = params
            for text in self.texts:
                self.labels[text].grid_forget()      
                self.entries[text].grid_forget()
            for x, param in enumerate(params):
                self.labels[param.label].grid(row=x+1+self.shift, column=0)
                self.entries[param.label].grid(row=x+1+self.shift, column=1, sticky='ew')
        return inner_command
        
    #create button to convert to Gcode
    def gcode(self):
        
        self.buttonGcode = ttk.Button(self,text='Generate Code',command=lambda: self.convert())
        self.buttonGcode.grid(row=len(self.texts)+1,column=1)
        
    #all set up functions together
    def create_var_page(self):
        
        self.set_labels()
        self.set_entries()
        self.save_option()
        self.upload_option()
        self.tab_buttons()
        self.gcode()
        self.model_page()
        self.g_robot()
        self.version_num()      
        self.reset_vars()
        
    #create button to switch to 3D model page
    def model_page(self):  
        
        #button to switch to 3D model page
        self.buttonModel = ttk.Button(self, text='3D Model', 
                             command=lambda: self.to_model())
        self.buttonModel.grid(row=len(self.texts)+1,column=0)
        
    #create radiobutton to switch between gcode and robotcode
    def g_robot(self):
        
        self.g_robot_var = IntVar()
        if self.defaults['g_robot_var']:
            self.g_robot_var.set(self.defaults['g_robot_var'])
        else:
            self.g_robot_var.set(c.GCODE)
        
        self.buttonChooseGcode = ttk.Radiobutton(self, text='Gcode', variable=self.g_robot_var, value=c.GCODE)
        self.buttonChooseGcode.grid(row=len(self.texts)+2,column=0)
        self.buttonChooseRobot = ttk.Radiobutton(self, text='RobotCode', variable=self.g_robot_var, value=c.ROBOTCODE)
        self.buttonChooseRobot.grid(row=len(self.texts)+2,column=1)
        
    def version_num(self):
        
        self.labelVersion = ttk.Label(self, text='Version ' + version)
        self.labelVersion.grid(row=len(self.texts)+3,column=0)
        
    def regrid(self):
        
        for text in self.texts:
            self.labels[text].grid_forget()      
            self.entries[text].grid_forget()

        for x, param in enumerate(self.current_menu):
            self.labels[param.label].grid(row=x+1+self.shift, column=0)
            self.entries[param.label].grid(row=x+1+self.shift, column=1)
        
        self.values_bar()
        
        self.buttonGcode.grid(row=len(self.texts)+1+self.shift,column=1)
        self.buttonModel.grid(row=len(self.texts)+1+self.shift,column=0)
        self.buttonChooseGcode.grid(row=len(self.texts)+2+self.shift,column=0)
        self.buttonChooseRobot.grid(row=len(self.texts)+2+self.shift,column=1)
        self.labelVersion.grid(row=len(self.texts)+3+self.shift,column=0)
        
    def values_bar(self):
        
        text_keys = ''        
        text_values = ''
        for key, value in self.var_saved.items():
            text_keys += '%10s ' % (key)
            text_values += '%10s ' %(value)
        self.var_text_keys.set(text_keys)
        self.var_text_values.set(text_values)
        if self.shift:
            self.labelKeys.grid(row=1,column=1)
            self.labelValues.grid(row=2,column=1)
    
    def reset_vars(self):
        
        self.old_var = ''
        self.var_keys = []
        self.var_types = {}
        self.var_values = {}
        self.var_stringvars = {}
        self.var_labels = {}
        self.var_entries = {}
        self.var_saved = {}
    
    def set_var(self, var):
        
        self.shift = 0
        self.regrid()        
        
        if var == 'choose a shape':
            self.annot = False
        elif var == c.STL_FLAG:
            self.stl_path = filedialog.askopenfilename()
            if self.stl_path == '':
                self.text_variable['outline'].set('choose a shape')
            else:
                self.text_variable['stl_file'].set(os.path.basename(os.path.normpath(self.stl_path)))
            self.annot = False
        else:
            self.stl_path = ''
            self.annot = inspect.getfullargspec(getattr(ds, var)).annotations
        
        if self.annot: 
            self.shift = 2
            self.regrid()            
            
            var_window = Tk()
            
            var_window.title(var)
            var_window.geometry('+650+100')         
            
            if self.old_var != var:
                self.reset_vars()
                self.old_var = var
            
            for x, (key, value) in enumerate(self.annot.items()):
                if key != 'return':
                    self.var_keys.append(key)
                    self.var_types[key] = value
                    new_value = str(value).split('\'')[1]
                    self.var_stringvars[key] = StringVar(var_window)
                    if self.var_saved:
                        self.var_stringvars[key].set(self.var_saved[key])
                    else:
                        self.var_stringvars[key].set(new_value)
                    self.var_labels[key] = ttk.Label(var_window, text=key)
                    self.var_labels[key].grid(row=x, column=0, padx=5)
                    self.var_entries[key] = ttk.Entry(var_window, textvariable=self.var_stringvars[key])
                    self.var_entries[key].grid(row=x, column=1)
                    self.var_values[self.var_entries[key]] = new_value
            
            def default(event):
                current = event.widget
                if current.get() == self.var_values[current]:
                    current.delete(0, END)
                elif current.get() == '':
                    current.insert(0, self.var_values[current])   
                    
            def quicksave():
                for key in self.var_keys:
                    self.var_saved[key] = self.var_stringvars[key].get()
                self.values_bar()
                var_window.destroy()
                   
            for key in self.var_keys:
                self.var_entries[key].bind('<FocusIn>', default)
                self.var_entries[key].bind('<FocusOut>', default)

            buttonDestroy = ttk.Button(var_window, text='OK', command=quicksave)
            buttonDestroy.grid(row=len(self.annot.items())+1, column=1)

            var_window.protocol("WM_DELETE_WINDOW", quicksave)
            var_window.mainloop()
            
        else:
            self.reset_vars()
        
    #############################################
    #   methods that are called from buttons    #
    #############################################
                
    def save(self, name = None):

        #only saving JSON
        if name == None:
            self.savePath = filedialog.asksaveasfilename()
            self.savePath = self.check_end(self.savePath)
            if self.g_robot_var.get() == c.GCODE:
                gcodeName = self.savePath.split('/')[len(self.savePath.split('/'))-1] + '.gcode'
            elif self.g_robot_var.get() == c.ROBOTCODE:
                gcodeName = self.savePath.split('/')[len(self.savePath.split('/'))-1] + '.mod'
            self.filename = self.savePath + '.json'  
        
        #converting to gcode -- create temp json file with same name as gcode file
        elif name == 'gcode':
            self.savePath = filedialog.asksaveasfilename()
            self.savePath = self.check_end(self.savePath)
            self.filename = self.JSONPATH + self.savePath.split('/')[len(self.savePath.split('/'))-1] + '.json'
            if self.g_robot_var.get() == c.GCODE:
                gcodeName = self.savePath + '.gcode'
            elif self.g_robot_var.get() == c.ROBOTCODE:
                gcodeName = self.savePath + '.mod'
            
        #switching to 3D model page -- create temp json file
        else:
            self.savePath = 'blank'
            if self.g_robot_var.get() == c.GCODE:
                gcodeName = self.GCODEPATH + name + '.gcode'
            elif self.g_robot_var.get() == c.ROBOTCODE:
                gcodeName = self.GCODEPATH = anem + '.mod'
            self.filename = self.JSONPATH + name + '.json'          
        
        data = {}               #dictionary to put String value of StringVar values in
        var_data = {}
        #check if the user cancelled saving the file
        if self.savePath:
                                                       #variables with type None
            data[self.OUTPUTFILENAME] = gcodeName
            data[self.OUTPUTSUBDIRECTORY] = self.savePath
            data['g_robot_var'] = self.g_robot_var.get()
            
            if self.var_keys:
                for key in self.var_keys:
                    if self.var_types[key] == float:
                        var_data[key] = float(self.var_stringvars[key].get())
                    elif self.var_types[key] == int:
                        var_data[key] = int(self.var_stringvars[key].get())
                    elif self.var_types[key] == str:
                        var_data[key] = str(self.var_stringvars[key].get())
            
            for label, data_type, _ in self.parameters:
                if label == 'stl_file':
                    data[label] = self.stl_path
                elif data_type is str:
                    data[label] = self.text_variable[label].get()
                elif data_type is None:
                    data[label] = None
                elif data_type is int or data_type is float:
                    data[label] = data_type(self.text_variable[label].get())
                else:
                    value = self.text_variable[label].get()    
                    if ' ' in value:
                        value = value.replace(' ', ',')                
                    if ',,' in value:
                        value = value.replace(',,', ',')     
                    if '(' in value:
                        value = value.replace('(', '')
                    if ')' in value:
                        value = value.replace(')', '')
                    if data_type == self.INT_LIST:
                        data[label] = [int(i) for i in value.split(',') if i  != '']     
                    elif data_type == self.FLOAT_LIST:
                        data[label] = [float(i) for i in value.split(',') if i  != '']    

            full_data = []
            full_data.append(data)
            full_data.append(var_data)            
            
            if not os.path.isdir(self.JSONPATH):
                os.makedirs(self.JSONPATH)
            with open(self.filename, 'w') as fp:
                json.dump(full_data, fp)    #save JSON file
    
    def check_end(self, pathName):
        
        pathName = os.path.splitext(pathName)[0]
    
        return pathName
        
    #uploads dictionary from JSON file to replace current StringVar values, opens window to find file       
    def upload(self):

        full_data = []
        var_data = {}
        data = {}               #new dictionary that will be replaced with dictionary from JSON file
        uploadname = filedialog.askopenfilename()     #creates window to find file
        
        if uploadname != '':
            with open(uploadname, 'r') as fp:
                full_data = json.load(fp)    #upload JSON file
            
            data = full_data[0]
            var_data = full_data[1]
                
            for key, value in data.items():    
                if data[key] == None:
                    self.text_variable[key].set('None') #replace current StringVar with String 'None'
                elif key == 'g_robot_var':
                    self.g_robot_var.set(value)
#                elif key == 'outline':
#                    self.entries[key].set(value)
                elif key in self.text_variable.keys():
                    value = str(value)
                    value = value.replace('[','')
                    value = value.replace(']','')
                    self.text_variable[key].set(value)   #replace current StringVar values with data from JSON file
                    
            if var_data:
                for key, value in var_data.items():
                    self.var_saved[key] = value
                    
    
    #create Gcode file                    
    def convert(self, name = None):
        
        if self.text_variable['outline'].get() == 'choose a shape':
            text = 'Error: no shape is selected.\n   Please choose a shape.'
            self.popup(text, 'Error', '+300+300')
        else:
            if name == None:
                self.save('gcode')
            else:
                self.save(name)
            
            #check if the user cancelled converting to Gcode
            if self.savePath and self.text_variable['outline'].get() != 'choose a shape':
                #convert to Gcode
                conversion = Main(self.filename, self.g_robot_var.get())
                conversion.run()
                os.remove(self.filename)
            
    def popup(self, msg, title, size):
        
        popup = Tk()
        
        popup.title(title)
        popup.geometry(size)
        labelPopup = ttk.Label(popup, text=msg)
        labelPopup.pack(padx=70, pady=50, anchor='center')
        buttonExit = ttk.Button(popup, text='OK', command=popup.destroy)
        buttonExit.pack(pady=10)
        
        popup.mainloop()
            
    
    #convert to gcode, switch to Page_Model        
    def to_model(self):
      
        self.convert('temp')
        
        self.controller.show_frame(Page_Model)
        
        os.remove(self.GCODEPATH + 'temp.gcode')


class Page_Model(Frame):    
    
    def __init__ (self, parent, controller):
        Frame.__init__(self, parent)
        self.controller = controller
        
    def model(self):
        
        data = []
        counter = 0
        layer_part = []
        
        datapath = pathway + '\\data_points.txt'
        with open(datapath, 'r') as f:
            for line in f:
                if 'start' in line:
                    print('start ', counter)
                    start = counter
                elif 'layer_number' in line:
                    print(line)
                    print(counter)
                    layer_part.append([line.split(':')[1], line.split(':')[3], start, counter])
                else:
                    data.append(line)      
                    data[counter] = data[counter].split(',')
                    for y in range(0,len(data[counter])):
                        data[counter][y] = float(data[counter][y])
                    data[counter] = [tuple(data[counter][0:3]), tuple(data[counter][3:])]
                    counter += 1
                    
        buttonMakeModel = ttk.Button(self, text='Make Model', command=make_model)
        buttonMakeModel.pack(padx=10, pady=10)
        
    def make_model(self):
        
        def Cube():
        #    x=0
        #    glBegin(GL_QUADS)
        #    for line in data:
        #        
        #        for point in line:
        #            glColor3fv((x,x,0))
        #            glVertex3fv(point)
        #            num = 1.0/len(data)
        #            x += num
        #            
        #    glEnd()
        #    
            glBegin(GL_LINES)
        #    for edge in edges:
        #        print('line')
        #        for vertex in edge:
        #            glVertex3fv(vertices[vertex])
        #            print(vertices[vertex])
            for line in data:
        #        print('line')
                for point in line:
                    
                    glVertex3fv(point)
        #            print(point)
            glEnd()
            
        def main():
            pygame.init()
            display = (800,600)
            pygame.display.set_mode(display, DOUBLEBUF|OPENGL)
            
            gluPerspective(45, (display[0]/display[1]), 0.1, 1000.0) #187
            
            glTranslatef(-112.0,-40.0, -500)
            
            glRotatef(0, 0, 0, 0)
            
            while True:
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        pygame.quit()
                        quit()
                        
                    if event.type == pygame.KEYDOWN:
                        if event.key == pygame.K_LEFT:
                            glTranslatef(-10,0,0)
                        if event.key == pygame.K_RIGHT:
                            glTranslatef(10,0,0)
                        if event.key == pygame.K_UP:
                            glTranslatef(0,10,0)
                        if event.key == pygame.K_DOWN:
                            glTranslatef(0,-10,0)
                        if event.key == pygame.K_a:
                            glRotatef(10,0,1,0)
                        if event.key == pygame.K_d:
                            glRotatef(-10,0,1,0)
                        if event.key == pygame.K_w:
                            glRotatef(10,1,0,0)
                        if event.key == pygame.K_s:
                            glRotatef(-10,1,0,0)
                        if event.key == pygame.K_q:
                            glRotatef(10,0,0,1)
                        if event.key == pygame.K_e:
                            glRotatef(-10,0,0,1)
                            
                    if event.type == pygame.MOUSEBUTTONDOWN:
                        if event.button == 4:
                            glTranslatef(0,0,10.0)
                        if event.button == 5:
                            glTranslatef(0,0,-10.0)
                
                glRotatef(0,0,0,0)        
                glClear(GL_COLOR_BUFFER_BIT|GL_DEPTH_BUFFER_BIT)
                Cube()
                pygame.display.flip()
                pygame.time.wait(10)
                
        main()
    
#    def __init__(self, parent, controller):
#        Frame.__init__(self, parent)
#        self.controller = controller
#        
#        self.get_data()
#        
#    def get_data(self):
#        
#        data = []
#        counter = 0
#        self.xar = []
#        self.yar = []
#        self.zar = []
#        self.layer_part = []
#        
#        with open('data_points.txt', 'r') as f:
#            for line in f:
#                if 'start' in line:
#                    print('start ', counter)
#                    start = counter
#                elif 'layer_number' in line:
#                    print(line)
#                    print(counter)
#                    self.layer_part.append([line.split(':')[1], line.split(':')[3], start, counter])
#                else:
#                    data.append(line)      
#                    data[counter] = data[counter].split(',')
#                    for y in range(0,len(data[counter])):
#                        data[counter][y] = float(data[counter][y])
#                    self.xar.append([data[counter][0], data[counter][3]])
#                    self.yar.append([data[counter][1], data[counter][4]])
#                    self.zar.append([data[counter][2], data[counter][5]])     
#                    counter += 1
#                    
#        self.setup()
#    
#    def show_labels(self):
#        
#        labelIntro = ttk.Label(self, text='Choose the start and end layers of the model:')
#        labelIntro.grid(row=0,column=1)
#        
#        labelStart = ttk.Label(self, text='Start')
#        labelStart.grid(row=1,column=0)
#        
#        labelEnd = ttk.Label(self, text='End')
#        labelEnd.grid(row=2,column=0)
#        
#    def show_scales(self):
#        
#        self.scaleStart = Scale(self, from_=0, to=len(self.xar), length=500, orient=HORIZONTAL)
#        self.scaleStart.grid(row=1,column=1)
#        
#        self.scaleEnd = Scale(self, from_=0, to=len(self.xar), length=500, tickinterval=5000, orient=HORIZONTAL)
#        self.scaleEnd.grid(row=2,column=1)
#        
#    def show_buttons(self):
#        
#        buttonSubmit = ttk.Button(self, text='Create Model', command=lambda: 
#            self.make_graph(self.scaleStart.get(), self.scaleEnd.get()))
#        buttonSubmit.grid(row=3,column=1)
#        
#        buttonVariables = ttk.Button(self, text='Variables', 
#                     command=lambda: self.to_variables())
#        buttonVariables.grid(row=0,column=0)
#    
##        self.buttonUpdate = ttk.Button(self, text='Update from Variables', command=lambda: self.get_data())
##        self.buttonUpdate.grid(row=4,column=1)
#
##        self.radiobuttons = {}
##        x = 0
##        y = 0
##        z = 0
##        selection = IntVar()
##        
##        for id_array in self.layer_part:
##            rb_text = 'Part:' + str(id_array[1] + ' Layer:' + str(id_array[0]))
##            self.radiobuttons[str(id_array)] = ttk.Radiobutton(self, text=rb_text, variable=selection, value=x)
##            self.radiobuttons[str(id_array)].grid(row=z+4,column=y)
##            x+=1
##            y = x//5
##            z = x%5 
#
#        self.intvar_layerparts = {}
#        
#        self.mb = ttk.Menubutton(self, text='testing')
#        self.mb.grid()
#        self.mb.menu = Menu (self.mb, tearoff=1)
#        self.mb['menu'] = self.mb.menu
#        
#        for id_array in self.layer_part:
#            self.intvar_layerparts[str(id_array)] = IntVar()
#            self.rb_text = 'Part:' + str(id_array[1] + ' Layer:' + str(id_array[0]))
#            self.mb.menu.add_checkbutton(label=self.rb_text, onvalue=1, offvalue=0, variable=self.intvar_layerparts[str(id_array)])
#        
#        self.mb.grid(row=5,column=1)
#        
#        buttonModel = ttk.Button(self, text='Create Model', command=lambda:
#            self.make_model())
#        buttonModel.grid(row=6,column=1)
#        
#
#    def setup(self):
#
#        self.show_labels()
#        self.show_scales()
#        self.show_buttons()                
#        
#    def make_graph(self, start, end):
#                
#        self.fig = plt.figure()
#        self.ax = self.fig.add_subplot(111, projection='3d')
#        
#        self.colors = []
#        
#        color_num = ['0','1','2','3','4','5','6','7','8','9','A','B','C','D','E','F']
#        color_num2 = ['0','8']
#        for one in color_num:
#            for two in color_num2:
#                for three in color_num2:
#                    for four in color_num2:
#                        for five in color_num2:
#                            for six in color_num:
#                                curr_color = '#' + one + two + three + four + five + six
#                                self.colors.append(curr_color)
#            
#        for num in range(start, end):
#            num_color = num%len(self.colors)
#            self.ax.plot_wireframe(self.xar[num], self.yar[num], self.zar[num], color=self.colors[num_color])
#            
#        plt.show()
#        
#    def make_model(self):
#        
#        self.fig = plt.figure()
#        self.ax = self.fig.add_subplot(111, projection='3d')
#        
#        self.colors = []
#        
#        color_num = ['0','1','2','3','4','5','6','7','8','9','A','B','C','D','E','F']
#        color_num2 = ['0','8']
#        for one in color_num:
#            for two in color_num2:
#                for three in color_num2:
#                    for four in color_num2:
#                        for five in color_num2:
#                            for six in color_num:
#                                curr_color = '#' + one + two + three + four + five + six
#                                self.colors.append(curr_color)
#         
##        for id_array in self.layer_part:
##            print(self.intvar_layerparts[id_array].get())
#         
#         
#        counting = 0                       
#        for id_array in self.layer_part:
#            if self.intvar_layerparts[str(id_array)].get() == 1:
#                for c in range(int(id_array[2]), int(id_array[3])):
#                    num_color=c%len(self.colors)
#                    self.ax.plot_wireframe(self.xar[c], self.yar[c], self.zar[c], color=self.colors[num_color])
#                    
#        plt.show()
#        
#    def to_variables(self):
#        
#        self.controller.show_frame(Page_Variables, True, Page_Model)
#        
#    
##class Page_Model(Frame):
##    
##    def __init__(self, parent, controller):
##        Frame.__init__(self, parent)
##        self.controller = controller
##        
##        labelExample = ttk.Label(self, text='HELLO')
##        labelExample.pack()
##        
##        self.to_variables()
##        
##        canvasExample = Canvas(self, width=200, height=100)
##        canvasExample.pack()      \
##        
##        canvasExample.create_rectangle(50, 20, 150, 80, fill='#476042')
##        canvasExample.create_line(0, 0, 50, 20, width=3)
##        
##        '''
##        f = Figure(figsize=(5,5), dpi=100)
##        a = f.add_subplot(111)
##        a.plot([1,2,3,4,5,6,7,8],[5,6,1,3,8,9,3,5])
##        
##        canvas = FigureCanvasTkAgg(f, self)
##        canvas.show()
##        canvas.get_tk_widget().pack(side=TOP, fill=BOTH, expand=True)
##        
##        toolbar = NavigationToolbar2TkAgg(canvas, self)
##        toolbar.update()
##        canvas._tkcanvas.pack()
##        '''
##        
##        
##    def to_variables(self):
##        
##        buttonVariable = ttk.Button(self, text='Variables', 
##                                command=lambda: self.controller.show_frame(Page_Variables))
##        buttonVariable.pack()
    
#only works if program is used as the main program, not as a module    
#if __name__ == '__main__':
    

#####################
#   GUI creation    #
#####################

#create GUI
gui = GUI()

#keeps GUI open, always necessary
gui.mainloop() 