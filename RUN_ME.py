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
    Drop = namedtuple('Dropdown', Par._fields + ('ds_return',))
    
    dropdowns = [
                Drop('outline', STR, (COMMON, PART), 'outline'),
                Drop('pattern', STR, (COMMON, PART,), 'linegroup'),
                Drop('test', STR, (COMMON,), 'test'),
                ]
          
    parameters = [
                Par(c.STL_FLAG, STR, (COMMON, PART)),
                Par('solidityRatio', FLOAT_LIST, (COMMON, PART)),
                Par('printSpeed', INT_LIST, (COMMON, PART)),
                Par('shiftX', FLOAT_LIST, (COMMON, PART)),
                Par('shiftY', FLOAT_LIST, (COMMON, PART)),
                Par('firstLayerShiftZ', FLOAT, (PART,)),
                Par('numLayers', INT_LIST, (COMMON, PART)),
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
                
    Elem = namedtuple('Element', 'label entry text_variable')
                
    OUTPUTFILENAME = 'outputFileName'
    CURRPATH = os.path.dirname(os.path.realpath(__file__))
    GCODEPATH = CURRPATH + '\\Gcode\\'
    JSONPATH = CURRPATH + '\\JSON\\'
    OUTPUTSUBDIRECTORY = 'outputSubDirectory'
    
    def __init__(self, parent, controller):
        Frame.__init__(self, parent)
        self.controller = controller
        
        self.filename = ''
        self.elements = {}  
        self.numRows = len(self.parameters)
               
        self.fields = []
        for menu in self.menus:
            field = []
            for dropdown in self.dropdowns:
                if menu.group in dropdown.groups:
                    field.append(dropdown)
            for param in self.parameters:
                if menu.group in param.groups:
                    field.append(param)
            self.fields.append(field)
           
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
            full_defaults = [{}, []]
            for x in range(len(self.dropdowns)):
                full_defaults.append({})
        
        self.defaults = full_defaults[0]
        dropdown_defaults = full_defaults[1]
        
        for x in range(len(self.dropdowns)):
            if x < len(dropdown_defaults):
                if len(dropdown_defaults[x]) > 0:
                    self.all_vars[x][self.SAVED] = dropdown_defaults[x]
                    for key, value in dropdown_defaults[x].items():
                        self.all_vars[x][self.KEYS].append(key)
                        self.all_vars[x][self.TYPES][key] = type(value)
            
        for param in self.dropdowns + self.parameters:
            if param.label not in self.defaults:
                self.defaults[param.label] = ''
                if param.label == c.STL_FLAG:
                    self.stl_path = ''
            elif param.label == c.STL_FLAG:
                self.stl_path = self.defaults[param.label]
                if self.stl_path:
                    self.defaults[param.label] = os.path.basename(os.path.normpath(self.stl_path))
                    
        for x, dropdown in enumerate(self.dropdowns):
            if dropdown.label in self.defaults:
                self.all_vars[x][self.VAR] = self.defaults[dropdown.label]
        
        if self.SHIFT in self.defaults:            
            self.shift = self.defaults[self.SHIFT]
        else:
            self.shift = 0
                
        
    def set_elements(self):
    
        self.doneshapes_menu()
        
        dd = len(self.dropdowns)
        for x, param in enumerate(self.parameters):
            x += 1+len(self.dropdowns)
            curr_label = ttk.Label(self, text= param.label + ' - ' + param.data_type)
            curr_text_variable = StringVar(self, value=self.defaults[param.label])
            curr_entry = ttk.Entry(self, textvariable=curr_text_variable)
            self.elements[param.label] = self.Elem(curr_label, curr_entry, curr_text_variable)
            self.elements[param.label].label.grid(row=x+dd,column=0)
            self.elements[param.label].entry.grid(row=x+dd,column=1,sticky='ew')
            
        #labels for displaying outline or pattern values
        self.var_text = {}
        self.var_labels = {}
        self.var_overall_label = {}
        for x, dropdown in enumerate(self.dropdowns):
            self.var_text[x] = {}
            self.var_labels[x] = {}
            self.var_overall_label[x] = Label(self, text=dropdown.label)
            for key_or_value in (self.KEYS, self.VALUES):
                self.var_text[x][key_or_value] = StringVar(self)
                self.var_labels[x][key_or_value] = Label(self, 
                                textvariable=self.var_text[x][key_or_value])
        
        self.elements[c.STL_FLAG].entry.config(state=DISABLED)
    
    #creates menu of the different possible shapes from the doneshapes class        
    def doneshapes_menu(self):
        
        for x, dropdown in enumerate(self.dropdowns):
            doneshape = []
            if dropdown.label == 'outline':
                doneshape.append(c.STL_FLAG)
            for member in inspect.getmembers(ds, inspect.isfunction):
                if dropdown.ds_return in str(inspect.getfullargspec(getattr(ds, member[0])).annotations['return']):
                    doneshape.append(member[0])
        
            curr_label = ttk.Label(self, text= dropdown.label + ' - ' + dropdown.data_type)
            curr_text_variable = StringVar(self, value=self.defaults[dropdown.label])
            curr_entry = ttk.OptionMenu(self,
                                        curr_text_variable,
                                        self.defaults[dropdown.label],
                                        *doneshape,
                                        command=self.set_var)
            self.elements[dropdown.label] = self.Elem(curr_label, curr_entry, curr_text_variable)
            self.elements[dropdown.label].label.grid(row=x+1,column=0)
            self.elements[dropdown.label].entry.grid(row=x+1,column=1,sticky='ew')
        
    def save_option(self): 
        
        buttonSave = ttk.Button(self,text='Save',command=lambda: self.save()).grid(row=0,column=1)
      
    def upload_option(self):   
        
        buttonUpload = ttk.Button(self,text='Upload',command=lambda: self.upload()).grid(row=0,column=0)
        
    #create menu of label and buttons to switch between tabs
    def tab_buttons(self):
        
        labelParameters = ttk.Label(self,text='Parameters',font='-weight bold')
        labelParameters.grid(row=0,column=2)

        buttonAll = ttk.Button(self,text='All',command=self.command(self.dropdowns + self.parameters))
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
        self.buttonModel = ttk.Button(self, text='3D Model', command=lambda: self.to_model())
        self.buttonModel.grid(row=self.numRows+1, column=0)
        
    #create radiobutton to switch between gcode and robotcode
    def g_robot(self):
        
        self.g_robot_var = IntVar()
        if self.G_ROBOT_VAR in self.defaults:
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
        
        for param in self.dropdowns + self.parameters:
            self.elements[param.label].label.grid_forget()      
            self.elements[param.label].entry.grid_forget()

        for x, param in enumerate(self.current_menu):
            self.elements[param.label].label.grid(row=x+1+self.shift, column=0)
            self.elements[param.label].entry.grid(row=x+1+self.shift, column=1)
    
        self.values_bar()
        self.buttonGcode.grid(row=self.numRows+1+self.shift,column=1)
        self.buttonModel.grid(row=self.numRows+1+self.shift,column=0)
        self.buttonChooseGcode.grid(row=self.numRows+2+self.shift,column=0)
        self.buttonChooseRobot.grid(row=self.numRows+2+self.shift,column=1)
        self.labelVersion.grid(row=self.numRows+3+self.shift,column=0)
        
    #shows the values entered into the popup doneshapes menu
    def values_bar(self):
        
        extra_shift = 0
        for x in range(len(self.dropdowns)):
            text_keys = ''        
            text_values = ''
            if len(self.all_vars[x][self.SAVED]) > 0:
                self.var_overall_label[x].grid(row=1+extra_shift, column=0)
                for key, value in self.all_vars[x][self.SAVED].items():
                    text_keys += '%10s ' % (key)
                    text_values += '%10s ' %(value)
                self.var_text[x][self.KEYS].set(text_keys)
                self.var_text[x][self.VALUES].set(text_values)
                self.var_labels[x][self.KEYS].grid(row=1+extra_shift,column=1)
                self.var_labels[x][self.VALUES].grid(row=2+extra_shift,column=1)
                extra_shift += 2
            else:
                self.var_overall_label[x].grid_forget()
                self.var_labels[x][self.KEYS].grid_forget()
                self.var_labels[x][self.VALUES].grid_forget()
            
    def set_all_vars(self):
        
        self.all_vars = []
        
        for x in range(len(self.dropdowns)):
            self.all_vars.append({})
            for added_key, added_value in ((self.VAR, ''), (self.KEYS, []), (self.TYPES, {}), (self.VALUES, {}), 
                                           (self.STRINGVARS, {}), (self.LABELS, {}), (self.ENTRIES, {}), (self.SAVED, {})):
                self.all_vars[x][added_key] = added_value
    
    #resets doneshape menu variables (either outline or pattern)                    
    def reset_certain_vars(self, vars_to_reset):

        for key, value in self.all_vars[vars_to_reset].items():
            if type(value) == str:
                value = ''
            elif type(value) == dict:
                self.all_vars[vars_to_reset][key].clear()
            elif type(value) == list:
                value[:] = []
    
    #creates popup menu to set values for a doneshape function
    def set_var(self, var):

        for x, dropdown in enumerate(self.dropdowns):
            if dropdown.ds_return in str(inspect.getfullargspec(getattr(ds, var)).annotations['return']):
                dropdown_index = x
                label = dropdown.label
            
        if var == c.STL_FLAG:
            self.stl_path = filedialog.askopenfilename()
            if self.stl_path == '':
                self.elements['outline'].text_variable.set(c.OUTLINE_NONE_CHOICE)
            else:
                self.elements[c.STL_FLAG].text_variable.set(os.path.basename(os.path.normpath(self.stl_path)))
            self.annot = {}
            
        else:
            self.annot = inspect.getfullargspec(getattr(ds, var)).annotations
            if label == 'outline':
                self.stl_path = ''
                self.elements[c.STL_FLAG].text_variable.set(self.stl_path)
            
         #TODO change this to for self.doneshapes   
        self.shift = 0
        for x, dropdown in enumerate(self.dropdowns):
            if len(self.all_vars[x][self.SAVED]) > 0 and label != dropdown.label:
                self.shift += 2

        if len(self.annot) > 1: 
            self.shift += 2
            
            self.regrid()            
            
            var_window = Tk()
            var_window.title(var)
            var_window.geometry('+650+100')  
            
            if self.all_vars[dropdown_index][self.VAR] != var:
                self.reset_certain_vars(dropdown_index)
                self.all_vars[dropdown_index][self.VAR] = var
                      
            for x, (key, value) in enumerate(self.annot.items()):
                if key != 'return':
                    self.all_vars[dropdown_index][self.KEYS].append(key)
                    self.all_vars[dropdown_index][self.TYPES][key] = value
                    new_value = str(value).split('\'')[1]
                    self.all_vars[dropdown_index][self.STRINGVARS][key] = StringVar(var_window)
                    if len(self.all_vars[dropdown_index][self.SAVED]) > 0:
                        self.all_vars[dropdown_index][self.STRINGVARS][key].set(self.all_vars[dropdown_index][self.SAVED][key])
                    else:
                        self.all_vars[dropdown_index][self.STRINGVARS][key].set(new_value)
                    self.all_vars[dropdown_index][self.LABELS][key] = ttk.Label(var_window, text=key)
                    self.all_vars[dropdown_index][self.LABELS][key].grid(row=x, column=0, padx=5)
                    self.all_vars[dropdown_index][self.ENTRIES][key] = ttk.Entry(var_window, 
                                                                            textvariable=self.all_vars[dropdown_index][self.STRINGVARS][key])
                    self.all_vars[dropdown_index][self.ENTRIES][key].grid(row=x, column=1, padx=1, pady=1)
                    self.all_vars[dropdown_index][self.VALUES][self.all_vars[dropdown_index][self.ENTRIES][key]] = new_value  
                    
            def default(event):
                current = event.widget
                if current.get() == self.all_vars[dropdown_index][self.VALUES][current]:
                    current.delete(0, END)
                elif current.get() == '':
                    current.insert(0, self.all_vars[dropdown_index][self.VALUES][current]) 
                quicksave(False)
                    
            def quicksave(destroy = True):
                for key in self.all_vars[dropdown_index][self.KEYS]:
                    self.all_vars[dropdown_index][self.SAVED][key] = self.all_vars[dropdown_index][self.STRINGVARS][key].get()
                self.values_bar()
                if destroy:
                    var_window.destroy()
                   
            for key in self.all_vars[dropdown_index][self.KEYS]:
                self.all_vars[dropdown_index][self.ENTRIES][key].bind('<FocusIn>', default)
                self.all_vars[dropdown_index][self.ENTRIES][key].bind('<FocusOut>', default)

            buttonDestroy = ttk.Button(var_window, text='OK', command=quicksave)
            buttonDestroy.grid(row=len(self.annot.items())+1, column=1)

            var_window.protocol("WM_DELETE_WINDOW", quicksave)
            var_window.mainloop()
            
        else:
            self.reset_certain_vars(dropdown_index)
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
        
        self.set_elements()
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
        
    def _save(self, dic, key, save_type, value, is_list = False):
        if value == '':
            dic[key] = value
        elif is_list:
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
        dropdown_data = []
            
        if self.savePath:                                                       
            data[self.OUTPUTFILENAME] = gcodeName
            data[self.OUTPUTSUBDIRECTORY] = self.savePath
            data[self.G_ROBOT_VAR] = self.g_robot_var.get()
            data[self.SHIFT] = self.shift
            
            for x in range(len(self.dropdowns)):
                dropdown_data.append({})
                if len(self.all_vars[x][self.KEYS]) > 0:
                    for key in self.all_vars[x][self.KEYS]:
                        if self.all_vars[x][self.TYPES][key] in (float, int, str):
                            self._save(dropdown_data[x], key, self.all_vars[x][self.TYPES][key], 
                                 self.all_vars[x][self.SAVED][key])
            
            for param in self.dropdowns + self.parameters:                   
                if param.label == c.STL_FLAG:
                    data[param.label] = self.stl_path
                    
                elif param.data_type == self.INT_LIST or param.data_type == self.FLOAT_LIST:
                    if param.data_type == self.INT_LIST:
                        save_type = int
                    else:
                        save_type = float
                    if self.elements[param.label].text_variable.get() == '':
                        self._save(data, param.label, save_type, '')
                    else:
                        self._save(data, param.label, save_type, 
    self.elements[param.label].text_variable.get().replace(' ', ',').replace(',,', ',').replace('(', '').replace(')', ''), True)
                        
                elif param.data_type in (self.STR, self.INT, self.FLOAT):
                    self._save(data, param.label, param.data_type, self.elements[param.label].text_variable.get())
                    
                elif param.data_type == self.NONE:
                    data[param.label] = None
            
            if not os.path.isdir(self.JSONPATH):
                os.makedirs(self.JSONPATH)
            with open(self.filename, 'w') as fp:
                json.dump([data, dropdown_data], fp)   
    
    #accounts for file extensions
    def check_end(self, pathName):
        
        return os.path.splitext(pathName)[0]
        
    def upload(self):
        uploadname = filedialog.askopenfilename()  
        
        if uploadname != '':
            with open(uploadname, 'r') as fp:
                data, dropdown_data = json.load(fp)
                
            for x in range(len(self.dropdowns)):
                self.reset_certain_vars(x)
               
            for key, value in data.items():    
                if data[key] == None:
                    self.elements[key].text_variable.set('None') 
                elif key == self.SHIFT:
                    self.shift = value
                elif key == self.G_ROBOT_VAR:
                    self.g_robot_var.set(value)
                elif key == c.STL_FLAG:
                    self.stl_path = value
                    if self.stl_path:
                        self.elements[key].text_variable.set(os.path.basename(os.path.normpath(self.stl_path)))
                    else:
                        self.elements[key].text_variable.set(self.stl_path)
                elif key in self.elements.keys():
                    value = str(value)
                    value = value.replace('[','').replace(']','')
                    self.elements[key].text_variable.set(value)  
            
            for x, dropdown in enumerate(self.dropdowns):
                if len(dropdown_data[x]) > 0:
                    for key, value in dropdown_data[x].items():
                        self.all_vars[x][self.KEYS].append(key)
                        self.all_vars[x][self.SAVED][key] = value
                        self.all_vars[x][self.TYPES][key] = type(value)
                        self.all_vars[x][self.VAR] = self.elements[dropdown.label].text_variable.get()
            
            self.values_bar()
            self.regrid()
            
    #swtiches between tabs        
    def command(self, params):
        def inner_command():
            self.current_menu = params
            for param in self.parameters:
                self.elements[param.label].label.grid_forget()      
                self.elements[param.label].entry.grid_forget()
            for x, param in enumerate(params):
                self.elements[param.label].label.grid(row=x+1+self.shift, column=0)
                self.elements[param.label].entry.grid(row=x+1+self.shift, column=1, sticky='ew')
        return inner_command
                    
    
    #create Gcode file                    
    def convert(self, name = None):
        global data_points
        
        if name == None:
            self.save('gcode')
        else:
            self.save(name)
        
        if self.savePath:
            conversion = Runner(self.filename, self.g_robot_var.get())
            data_points = conversion.run()
            os.remove(self.filename)        
    
    #convert to gcode, switch to Page_Model        
    def to_model(self):
        
        try:
            self.convert('temp')
            
        except Exception as e:
            print('Error during Gcode conversion')
            print(e)
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