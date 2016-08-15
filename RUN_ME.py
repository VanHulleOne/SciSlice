# -*- coding: utf-8 -*-
'''
Created on Sat May 28 16:39:58 2016
@author: Alex Diebold
'''

import os

import constants as c
import matplotlib                  
from collections import namedtuple

#when using Spyder, to make a pop-up interactive plot, go to 
#tools > preferences > IPython console > Graphics > change "Backend" to "Automatic" > restart Spyder
from mpl_toolkits.mplot3d import axes3d
import matplotlib.pyplot as plt

from tkinter import *               #GUI module
from tkinter import ttk             #for styling purposing
from tkinter import filedialog      #window for saving and uploading files
import json                         #for saving and uploading files
from runner import Runner           #for converting to Gcode
import parameters
import doneshapes as ds
import inspect
data_points = []

class GUI(Tk):

    def __init__(self, *args, **kwargs):
        Tk.__init__(self, *args, **kwargs)
        
        Tk.iconbitmap(self, 'UW_Madison_icon.ico')
        Tk.title(self, '3D Printer Parameter Setter')
        #format window size -- width=450, height=475, 100px from left of screen, 100px from top of screen
        #Tk.geometry(self, '450x475+100+100')
        
        self.container = Frame(self)
        self.container.pack(side='top', fill='both', expand=True)
        self.container.grid(row=0,column=0)
        
        self.frames = {}
        
        self.shapes = {Page_Variables : '475x750+150+100',       
                       Page_Model : '600x500+150+100'}
        
        for F in (Page_Variables,):        
            frame = F(self.container, self)            
            self.frames[F] = frame            
            frame.grid(row=0, column=0, sticky='nsew')            
        
        #show initial Frame
        Tk.geometry(self, self.shapes[Page_Variables])
        self.show_frame(Page_Variables)
       
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
    
    INT_LIST = '[int]'
    FLOAT_LIST = '[float]'
    STR = 'str'
    INT = 'int'
    FLOAT = 'float'
    NONE = 'None'
    
    SHIFT = 'shift'
    G_ROBOT_VAR =  'g_robot_var'   
    
    VAR = 'var'
    KEYS = 'keys'
    TYPES = 'types'
    VALUES = 'values'
    STRINGVARS = 'stringvars'
    LABELS = 'labels'
    ENTRIES = 'entries'
    SAVED = 'saved'
    OUTLINE = 'outline'
    PATTERN = 'pattern'
    
    
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
                Par('outline', STR, (COMMON, PART)),
                Par(c.STL_FLAG, STR, (COMMON, PART)),
                Par('solidityRatio', FLOAT_LIST, (COMMON, PART)),
                Par('printSpeed', INT_LIST, (COMMON, PART)),
                Par('shiftX', FLOAT_LIST, (COMMON, PART)),
                Par('shiftY', FLOAT_LIST, (COMMON, PART)),
                Par('firstLayerShiftZ', FLOAT, (PART,)),
                Par('numLayers', INT_LIST, (COMMON, PART)),
                Par('pattern', STR, (COMMON, PART,)),
                Par('designType', INT, (PART,)),
                Par('infillAngleDegrees', FLOAT_LIST, (COMMON, LAYER)),
                Par('pathWidth', FLOAT_LIST, (LAYER,)),
                Par('layerHeight', FLOAT_LIST, (LAYER,)),
                Par('infillShiftX', FLOAT_LIST, (LAYER,)),
                Par('infillShiftY', FLOAT_LIST, (LAYER,)),
                Par('numShells', INT_LIST, (COMMON, LAYER)),
                Par('trimAdjust', FLOAT_LIST, (LAYER,)),
                Par('start_Gcode_FileName', STR, (FILE,)),
                Par('end_Gcode_FileName', STR, (FILE,)),
                Par('bed_temp', INT, (COMMON, PRINT)),
                Par('extruder_temp', INT, (COMMON, PRINT)),
                Par('nozzleDiameter', FLOAT, (PRINTER,)),
                Par('filamentDiameter', FLOAT, (PRINTER,)),
                Par('RAPID', INT, (PRINTER,)),
                Par('TRAVERSE_RETRACT', FLOAT, (PRINTER,)),
                Par('MAX_FEED_TRAVERSE', FLOAT, (PRINTER,)),
                Par('MAX_EXTRUDE_SPEED', INT, (PRINTER,)),
                Par('Z_CLEARANCE', FLOAT, (PRINTER,)),
                Par('APPROACH_FR', INT, (PRINTER,)),
                Par('comment', STR, (PRINTER,)),
                ]
                
    OUTPUTFILENAME = 'outputFileName'
    CURRPATH = os.path.dirname(os.path.realpath(__file__))
    GCODEPATH = CURRPATH + '\\Gcode\\'
    JSONPATH = CURRPATH + '\\JSON\\'
    OUTPUTSUBDIRECTORY = 'outputSubDirectory'
    
    def __init__(self, parent, controller):
        Frame.__init__(self, parent)
        self.controller = controller
        
        self.filename = ''
        self.text_variable = {}       
        self.labels = {}
        self.entries = {}        
        self.numRows = len(self.parameters)
               
        self.fields = []
        for menu in self.menus:
            self.fields.append([par for par in self.parameters if menu.group in par.groups])
           
        self.set_all_vars()
        self.set_defaults()
        
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
        
        for var_dict, outline_or_pattern in ((full_defaults[1], self.OUTLINE), (full_defaults[2], self.PATTERN)):
                if len(var_dict) > 0:
                    for key, value in var_dict.items():
                        self.all_vars[outline_or_pattern][self.SAVED][key] = value
            
        for param in self.parameters:
            if param.label not in self.defaults:
                self.defaults[param.label] = ''
            elif param.label == c.STL_FLAG:
                self.stl_path = self.defaults[param.label]
                if self.stl_path:
                    self.defaults[param.label] = os.path.basename(os.path.normpath(self.stl_path))
                    
        self.shift = self.defaults[self.SHIFT]
          
    def set_labels(self):        
        
        for param in self.parameters:
            self.labels[param.label] = ttk.Label(self, text= param.label + ' - ' + param.data_type)
        
        for x, par in enumerate(self.fields[self.COMMON]):
            self.labels[par.label].grid(row=x+1,column=0)
        
        #labels for displaying outline or pattern values
        self.var_text = {}
        self.var_labels = {}
        self.var_overall_label = {}
        for outline_or_pattern in (self.OUTLINE, self.PATTERN):
            self.var_text[outline_or_pattern] = {}
            self.var_labels[outline_or_pattern] = {}
            self.var_overall_label[outline_or_pattern] = Label(self, text=outline_or_pattern)
            for key_or_value in (self.KEYS, self.VALUES):
                self.var_text[outline_or_pattern][key_or_value] = StringVar(self)
                self.var_labels[outline_or_pattern][key_or_value] = Label(self, textvariable=self.var_text[outline_or_pattern][key_or_value])
            
    def set_entries(self):

        for param in self.parameters:
            self.text_variable[param.label] = StringVar(self, value=self.defaults[param.label])
            self.entries[param.label] = ttk.Entry(self, textvariable=self.text_variable[param.label])  
        
        self.doneshapes_menu()
        
        for x, par in enumerate(self.fields[self.COMMON]):
            self.entries[par.label].grid(row=x+1,column=1, sticky='ew')
            
        self.entries[c.STL_FLAG].config(state=DISABLED)
    
    #creates menu of the different possible shapes from the doneshapes class        
    def doneshapes_menu(self):
        
        doneshape_outline = [c.OUTLINE_NONE_CHOICE]
        doneshape_pattern = [c.PATTERN_NONE_CHOICE]
        doneshape_outline.append(c.STL_FLAG)
        for member in inspect.getmembers(ds, inspect.isfunction):
            if 'outline' in str(inspect.getfullargspec(getattr(ds, member[0])).annotations['return']):
                doneshape_outline.append(member[0])
            else:
                doneshape_pattern.append(member[0])
        
        self.entries['outline'] = ttk.OptionMenu(self,
                                                self.text_variable['outline'],
                                                self.defaults['outline'],
                                                *doneshape_outline,
                                                command=self.set_var)
        self.entries['pattern'] = ttk.OptionMenu(self,
                                                self.text_variable['pattern'],
                                                self.defaults['pattern'],
                                                *doneshape_pattern,
                                                command=self.set_var)
        
    def save_option(self): 
        
        buttonSave = ttk.Button(self,text='Save',command=lambda: self.save()).grid(row=0,column=1)
      
    def upload_option(self):   
        
        buttonUpload = ttk.Button(self,text='Upload',command=lambda: self.upload()).grid(row=0,column=0)
        
    #create menu of label and buttons to switch between tabs
    def tab_buttons(self):
        
        labelParameters = ttk.Label(self,text='Parameters',font='-weight bold')
        labelParameters.grid(row=0,column=2)

        buttonAll = ttk.Button(self,text='All',command=self.command(self.parameters))
        buttonAll.grid(row=1,column=2)
        
        for x, menu in enumerate(self.menus):
            button = ttk.Button(self, text=menu.name, command=self.command(self.fields[menu.group]))
            button.grid(row=2+x, column=2)
        
    #create Gcode conversion button
    def gcode(self):
        
        self.buttonGcode = ttk.Button(self,text='Generate Code',command=lambda: self.convert())
        self.buttonGcode.grid(row=len(self.parameters)+1,column=1)
        
    #create button to switch to 3D model page
    def model_page(self):  
        
        #button to switch to 3D model page
        self.buttonModel = ttk.Button(self, text='3D Model', 
                             command=lambda: self.to_model())
        self.buttonModel.grid(row=self.numRows+1, column=0)
        
    #create radiobutton to switch between gcode and robotcode
    def g_robot(self):
        
        self.g_robot_var = IntVar()
        if self.defaults[self.G_ROBOT_VAR]:
            self.g_robot_var.set(self.defaults[self.G_ROBOT_VAR])
        else:
            self.g_robot_var.set(c.GCODE)
        
        self.buttonChooseGcode = ttk.Radiobutton(self, text='Gcode', variable=self.g_robot_var, value=c.GCODE)
        self.buttonChooseGcode.grid(row=self.numRows+2,column=0)
        self.buttonChooseRobot = ttk.Radiobutton(self, text='RobotCode', variable=self.g_robot_var, value=c.ROBOTCODE)
        self.buttonChooseRobot.grid(row=self.numRows+2,column=1)
       
    def version_num(self):
        
        self.labelVersion = ttk.Label(self, text='Version ' + parameters.__version__)
        self.labelVersion.grid(row=self.numRows+3,column=0)
    
    #moves labels and entries up or down depending on the self.shift value    
    def regrid(self):
        
        for param in self.parameters:
            self.labels[param.label].grid_forget()      
            self.entries[param.label].grid_forget()

        for x, param in enumerate(self.current_menu):
            self.labels[param.label].grid(row=x+1+self.shift, column=0)
            self.entries[param.label].grid(row=x+1+self.shift, column=1)
    
        self.values_bar()
        print(self.shift)
        self.buttonGcode.grid(row=self.numRows+1+self.shift,column=1)
        self.buttonModel.grid(row=self.numRows+1+self.shift,column=0)
        self.buttonChooseGcode.grid(row=self.numRows+2+self.shift,column=0)
        self.buttonChooseRobot.grid(row=self.numRows+2+self.shift,column=1)
        self.labelVersion.grid(row=self.numRows+3+self.shift,column=0)
        
    #shows the values entered into the popup doneshapes menu
    def values_bar(self):
        
        extra_shift = 0
        for outline_or_pattern in (self.OUTLINE, self.PATTERN):
            text_keys = ''        
            text_values = ''
            if len(self.all_vars[outline_or_pattern][self.SAVED]) > 0:
                self.var_overall_label[outline_or_pattern].grid(row=1+extra_shift, column=0)
                for key, value in self.all_vars[outline_or_pattern][self.SAVED].items():
                    text_keys += '%10s ' % (key)
                    text_values += '%10s ' %(value)
                self.var_text[outline_or_pattern][self.KEYS].set(text_keys)
                self.var_text[outline_or_pattern][self.VALUES].set(text_values)
                self.var_labels[outline_or_pattern][self.KEYS].grid(row=1+extra_shift,column=1)
                self.var_labels[outline_or_pattern][self.VALUES].grid(row=2+extra_shift,column=1)
                extra_shift += 2
            else:
                self.var_overall_label[outline_or_pattern].grid_forget()
                self.var_labels[outline_or_pattern][self.KEYS].grid_forget()
                self.var_labels[outline_or_pattern][self.VALUES].grid_forget()
            
    def set_all_vars(self):
        
        self.all_vars = {self.OUTLINE : {self.VAR : '', self.KEYS : [], 
                             self.TYPES : {}, self.VALUES : {},
                             self.STRINGVARS : {}, self.LABELS : {}, 
                             self.ENTRIES : {}, self.SAVED : {}},
                        self.PATTERN : {self.VAR : '', self.KEYS : [], 
                             self.TYPES : {}, self.VALUES : {},
                             self.STRINGVARS : {}, self.LABELS : {}, 
                             self.ENTRIES : {}, self.SAVED : {}}}
    
    #resets doneshape menu variables (either outline or pattern)                    
    def reset_certain_vars(self, vars_to_reset):
        
        for key, value in self.all_vars[vars_to_reset].items():
            if type(value) == str:
                value = ''
            elif type(value) == dict:
                value.clear()
            elif type(value) == list:
                value[:] = []
    
    #creates popup menu to set values for a doneshape function
    def set_var(self, var):

        self.shift = 0    
        
        is_outline = False
        
        if var != c.STL_FLAG:
            try:
                self.annot = inspect.getfullargspec(getattr(ds, var)).annotations
            except:
                self.annot = {}
                if var == c.OUTLINE_NONE_CHOICE:
                    is_outline = True
                    self.stl_path = ''
                    self.text_variable[c.STL_FLAG].set(self.stl_path)
            else:
                if 'outline' in str(self.annot['return']):
                    is_outline = True
                    self.stl_path = ''
                    self.text_variable[c.STL_FLAG].set(self.stl_path)
        else:
            is_outline = True
            self.stl_path = filedialog.askopenfilename()
            if self.stl_path == '':
                self.text_variable['outline'].set(c.OUTLINE_NONE_CHOICE)
            else:
                self.text_variable[c.STL_FLAG].set(os.path.basename(os.path.normpath(self.stl_path)))
            self.annot = {}
            
        if is_outline:
            outline_or_pattern = self.OUTLINE
            if len(self.all_vars[self.PATTERN][self.SAVED]) > 0:
                self.shift += 2
        else:
            outline_or_pattern = self.PATTERN
            if len(self.all_vars[self.OUTLINE][self.SAVED]) > 0:
                self.shift += 2

        if len(self.annot) > 1: 
            self.shift += 2
            
            self.regrid()            
            
            var_window = Tk()
            
            var_window.title(var)
            var_window.geometry('+650+100')         
            
            if self.all_vars[outline_or_pattern][self.VAR] != var:
                self.reset_certain_vars(outline_or_pattern)
                self.all_vars[outline_or_pattern][self.VAR] = var
                      
            for x, (key, value) in enumerate(self.annot.items()):
                if key != 'return':
                    self.all_vars[outline_or_pattern][self.KEYS].append(key)
                    self.all_vars[outline_or_pattern][self.TYPES][key] = value
                    new_value = str(value).split('\'')[1]
                    self.all_vars[outline_or_pattern][self.STRINGVARS][key] = StringVar(var_window)
                    if len(self.all_vars[outline_or_pattern][self.SAVED]) > 0:
                        self.all_vars[outline_or_pattern][self.STRINGVARS][key].set
                        (self.all_vars[outline_or_pattern][self.SAVED][key])
                    else:
                        self.all_vars[outline_or_pattern][self.STRINGVARS][key].set(new_value)
                    self.all_vars[outline_or_pattern][self.LABELS][key] = ttk.Label(var_window, text=key)
                    self.all_vars[outline_or_pattern][self.LABELS][key].grid(row=x, column=0, padx=5)
                    self.all_vars[outline_or_pattern][self.ENTRIES][key] = ttk.Entry(var_window, 
                                                                            textvariable=self.all_vars[outline_or_pattern][self.STRINGVARS][key])
                    self.all_vars[outline_or_pattern][self.ENTRIES][key].grid(row=x, column=1, padx=1, pady=1)
                    self.all_vars[outline_or_pattern][self.VALUES][self.all_vars[outline_or_pattern][self.ENTRIES][key]] = new_value                    
            
            def default(event):
                current = event.widget
                if current.get() == self.all_vars[outline_or_pattern][self.VALUES][current]:
                    current.delete(0, END)
                elif current.get() == '':
                    current.insert(0, self.all_vars[outline_or_pattern][self.VALUES][current])   
                    
            def quicksave():
                for key in self.all_vars[outline_or_pattern][self.KEYS]:
                    self.all_vars[outline_or_pattern][self.SAVED][key] = self.all_vars[outline_or_pattern][self.STRINGVARS][key].get()
                self.values_bar()
                var_window.destroy()
                   
            for key in self.all_vars[outline_or_pattern][self.KEYS]:
                self.all_vars[outline_or_pattern][self.ENTRIES][key].bind('<FocusIn>', default)
                self.all_vars[outline_or_pattern][self.ENTRIES][key].bind('<FocusOut>', default)

            buttonDestroy = ttk.Button(var_window, text='OK', command=quicksave)
            buttonDestroy.grid(row=len(self.annot.items())+1, column=1)

            var_window.protocol("WM_DELETE_WINDOW", quicksave)
            var_window.mainloop()
            
        else:
            self.reset_certain_vars(outline_or_pattern)
            self.values_bar()
            self.regrid()
            
    #creates error popup message        
    def popup(self, msg, title, size):
        
        popup = Tk()
        
        popup.title(title)
        popup.geometry(size)
        labelPopup = ttk.Label(popup, text=msg)
        labelPopup.pack(padx=70, pady=50, anchor='center')
        buttonExit = ttk.Button(popup, text='OK', command=popup.destroy)
        buttonExit.pack(pady=10)
        
        popup.mainloop()
            
    #all set up functions
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
        self.regrid()
        
    #############################################
    #   methods that are called from buttons    #
    #############################################
               
    def save(self, name = None):

        #only saving JSON
        if name is None:
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
                gcodeName = self.GCODEPATH = name + '.mod'
            self.filename = self.JSONPATH + name + '.json'          
        
        data = {}              
        all_var_data = {self.OUTLINE : {}, self.PATTERN : {}}
        
        def save(dic, key, save_type, value, is_list = False):
            if is_list:
                dic[key] = [save_type(i) for i in value.split(',') if i != '']
            else:
                if save_type == self.INT:
                    dic[key] = int(value) 
                elif save_type == self.FLOAT:
                    dic[key] = float(value)
                elif save_type == self.STR:
                    dic[key] = str(value)
                else:
                    dic[key] = save_type(value)
            
        if self.savePath:                                                       
            data[self.OUTPUTFILENAME] = gcodeName
            data[self.OUTPUTSUBDIRECTORY] = self.savePath
            data[self.G_ROBOT_VAR] = self.g_robot_var.get()
            print(self.shift)
            data[self.SHIFT] = self.shift
            
            for outline_or_pattern in (self.OUTLINE, self.PATTERN):
                if len(self.all_vars[outline_or_pattern][self.KEYS]) > 0:
                    for key in self.all_vars[outline_or_pattern][self.KEYS]:
                        if self.all_vars[outline_or_pattern][self.TYPES][key] in (float, int, str):
                            save(all_var_data[outline_or_pattern], key, self.all_vars[outline_or_pattern][self.TYPES][key], 
                                 self.all_vars[outline_or_pattern][self.SAVED][key])
            
            for param in self.parameters:                   
                if param.label == c.STL_FLAG:
                    data[param.label] = self.stl_path
                    
                elif param.data_type == self.INT_LIST or param.data_type == self.FLOAT_LIST:
                    if param.data_type == self.INT_LIST:
                        save_type = int
                    else:
                        save_type = float
                    save(data, param.label, save_type, 
    self.text_variable[param.label].get().replace(' ', ',').replace(',,', ',').replace('(', '').replace(')', ''), True)
                        
                elif param.data_type in (self.STR, self.INT, self.FLOAT):
                    save(data, param.label, param.data_type, self.text_variable[param.label].get())
                    
                elif param.data_type == self.NONE:
                    data[param.label] = None
            
            if not os.path.isdir(self.JSONPATH):
                os.makedirs(self.JSONPATH)
            with open(self.filename, 'w') as fp:
                json.dump([data, all_var_data[self.OUTLINE], all_var_data[self.PATTERN]], fp)   
    
    #accounts for file extensions
    def check_end(self, pathName):
        
        return os.path.splitext(pathName)[0]
        
    def upload(self):
        uploadname = filedialog.askopenfilename()  
        
        if uploadname != '':
            with open(uploadname, 'r') as fp:
                data, outline_var_data, pattern_var_data = json.load(fp)
                
            for outline_or_pattern in (self.OUTLINE, self.PATTERN):
                self.reset_certain_vars(outline_or_pattern)
               
            for key, value in data.items():    
                if data[key] == None:
                    self.text_variable[key].set('None') 
                elif key == self.SHIFT:
                    self.shift = value
                elif key == self.G_ROBOT_VAR:
                    self.g_robot_var.set(value)
                elif key == c.STL_FLAG:
                    self.stl_path = value
                    if self.stl_path:
                        self.text_variable[key].set(os.path.basename(os.path.normpath(self.stl_path)))
                    else:
                        self.text_variable[key].set(self.stl_path)
                elif key in self.text_variable.keys():
                    value = str(value)
                    value = value.replace('[','').replace(']','')
                    self.text_variable[key].set(value)  
            
            for var_dict, outline_or_pattern in ((outline_var_data, self.OUTLINE), (pattern_var_data, self.PATTERN)):
                if len(var_dict) > 0:
                    for key, value in var_dict.items():
                        self.all_vars[outline_or_pattern][self.KEYS].append(key)
                        self.all_vars[outline_or_pattern][self.SAVED][key] = value
                        self.all_vars[outline_or_pattern][self.TYPES][key] = type(value)
                    
            self.regrid()
            
    #swtiches between tabs        
    def command(self, params):
        def inner_command():
            self.current_menu = params
            for param in self.parameters:
                self.labels[param.label].grid_forget()      
                self.entries[param.label].grid_forget()
            for x, param in enumerate(params):
                self.labels[param.label].grid(row=x+1+self.shift, column=0)
                self.entries[param.label].grid(row=x+1+self.shift, column=1, sticky='ew')
        return inner_command
                    
    
    #create Gcode file                    
    def convert(self, name = None):
        global data_points
        
        if self.text_variable['outline'].get() == c.OUTLINE_NONE_CHOICE:
            text = 'Error: no shape is selected.\n   Please choose a shape.'
            self.popup(text, 'Error', '+300+300')
        else:
            if name == None:
                self.save('gcode')
            else:
                self.save(name)
            
            if self.savePath and self.text_variable['outline'].get() != c.OUTLINE_NONE_CHOICE:
                conversion = Runner(self.filename, self.g_robot_var.get())
                data_points = conversion.run()
                os.remove(self.filename)        
    
    #convert to gcode, switch to Page_Model        
    def to_model(self):
        
        try:
            self.convert('temp')
            
        except:
            print('Error during Gcode conversion')
            self.controller.show_frame(Page_Variables)
            
        else:
            self.controller.show_frame(Page_Model)
            os.remove(self.GCODEPATH + 'temp.gcode')

class Page_Model(Frame):    
    
    def __init__(self, parent, controller):
        Frame.__init__(self, parent)
        self.controller = controller
        
        self.get_data()
       
    def get_data(self):
        global data_points
        
        data = []
        counter = 0
        self.xar = []
        self.yar = []
        self.zar = []
        self.layer_part = []
        curr_layer = None
        curr_part = None
        
        for line in data_points:
            if 'start' in line:
                start = counter
            else:
                if curr_layer != line[1].split(':')[1] and curr_part != line[1].split(':')[3]:
                    self.layer_part.append([line[1].split(':')[1], line[1].split(':')[3], start, counter]) 
                    curr_layer = line[1].split(':')[1]
                    curr_part = line[1].split(':')[3]
                data.append(line[0])      
                data[counter] = data[counter].split(',')
                for y in range(0,len(data[counter])):
                    data[counter][y] = float(data[counter][y])
                self.xar.append([data[counter][0], data[counter][3]])
                self.yar.append([data[counter][1], data[counter][4]])
                self.zar.append([data[counter][2], data[counter][5]])     
                counter += 1
                    
        self.setup()
    
    def show_labels(self):
        
        labelIntro = ttk.Label(self, text='Choose the start and end layers of the model:')
        labelIntro.grid(row=0,column=1)
        
        labelStart = ttk.Label(self, text='Start')
        labelStart.grid(row=1,column=0)
        
        labelEnd = ttk.Label(self, text='End')
        labelEnd.grid(row=2,column=0)
        
    def show_scales(self):
        
        self.scaleStart = Scale(self, from_=0, to=len(self.xar), length=500, orient=HORIZONTAL)
        self.scaleStart.grid(row=1,column=1)
        
        self.scaleEnd = Scale(self, from_=0, to=len(self.xar), length=500, tickinterval=5000, orient=HORIZONTAL)
        self.scaleEnd.grid(row=2,column=1)
        
    def show_buttons(self):
        
        buttonSubmit = ttk.Button(self, text='Create Model', command=lambda: 
            self.make_graph(self.scaleStart.get(), self.scaleEnd.get()))
        buttonSubmit.grid(row=3,column=1)
        
        buttonVariables = ttk.Button(self, text='Variables', 
                                 command=lambda: self.to_variables())
        buttonVariables.grid(row=0,column=0)

        self.intvar_layerparts = {}
        
        self.mb = ttk.Menubutton(self, text='Layers')
        self.mb.grid()
        self.mb.menu = Menu (self.mb, tearoff=1)
        self.mb['menu'] = self.mb.menu
        
        for id_array in self.layer_part:
            self.intvar_layerparts[str(id_array)] = IntVar()
            self.rb_text = 'Part:' + str(id_array[1] + ' Layer:' + str(id_array[0]))
            self.mb.menu.add_checkbutton(label=self.rb_text, onvalue=1, offvalue=0, variable=self.intvar_layerparts[str(id_array)])
        
        self.mb.grid(row=5,column=1)
        
        buttonModel = ttk.Button(self, text='Create Model',
                                 command=lambda: self.make_graph())
        buttonModel.grid(row=6,column=1)
        

    def setup(self):

        self.show_labels()
        self.show_scales()
        self.show_buttons()                
   
    def make_graph(self, start = False, end = False):
                
        self.fig = plt.figure()
        self.ax = self.fig.add_subplot(111, projection='3d')

        self.colors = []
        
        color_num = ['0','1','2','3','4','5','6','7','8','9','A','B','C','D','E','F']
        color_num2 = ['0','8']
        for one in color_num:
            for two in color_num2:
                for three in color_num2:
                    for four in color_num2:
                        for five in color_num2:
                            for six in color_num:
                                curr_color = '#' + one + two + three + four + five + six
                                self.colors.append(curr_color)

        if end:      
            for num in range(start, end):
                num_color = num%len(self.colors)
                self.ax.plot_wireframe(self.xar[num], self.yar[num], self.zar[num], color=self.colors[num_color])
                
        else:
            counting = 0                       
            for id_array in self.layer_part:
                if self.intvar_layerparts[str(id_array)].get() == 1:
                    for c in range(int(id_array[2]), int(id_array[3])):
                        num_color=c%len(self.colors)
                        self.ax.plot_wireframe(self.xar[c], self.yar[c], self.zar[c], color=self.colors[num_color])
            
        plt.show()
        
    def to_variables(self):
        
        self.controller.show_frame(Page_Variables, True, Page_Model)
    
#only works if program is used as the main program, not as a module    
if __name__ == '__main__': 
    
    gui = GUI()
    gui.mainloop() 