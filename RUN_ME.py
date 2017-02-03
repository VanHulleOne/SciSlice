# -*- coding: utf-8 -*-
'''
Created on Sat May 28 16:39:58 2016
@author: Alex Diebold
'''

import os, shutil

import constants as c               
from collections import namedtuple, OrderedDict

import tkinter as tk                #GUI module
from tkinter import ttk             #for styling purposing
from tkinter import filedialog      #window for saving and uploading files
import json                         #for saving and uploading files
from runner import Runner           #for converting to Gcode
import parameters
import doneshapes as ds
import inspect
data_points = []
import time

import pygame
#from pygame.locals import *

from wireframe import Wireframe

machineCodePath = ''

class GUI(tk.Tk):

    def __init__(self, *args, **kwargs):
        tk.Tk.__init__(self, *args, **kwargs)
        
        tk.Tk.iconbitmap(self, 'UW_Madison_icon.ico')
        tk.Tk.title(self, '3D Printer Parameter Setter')
        #format window size -- width=450, height=475, 100px from left of screen, 100px from top of screen
        #tk.Tk.geometry(self, '450x475+100+100')
        
        #set where the 3D model page opens
        os.environ['SDL_VIDEO_WINDOW_POS'] = '700,200'
        
        self.container = tk.Frame(self)
        self.container.pack(side='top', fill='both', expand=True)
        self.container.grid(row=0,column=0)
        
        self.frames = {}
        
        self.shapes = {Page_Variables : '475x850+150+100',}
        
        for F in (Page_Variables,):        
            frame = F(self.container, self)            
            self.frames[F] = frame            
            frame.grid(row=0, column=0, sticky='nsew')            
        self.protocol("WM_DELETE_WINDOW", self.on_closing)
        #show initial Frame
        tk.Tk.geometry(self, self.shapes[Page_Variables])
        self.show_frame(Page_Variables)
       
    def show_frame(self, cont, delete=False, cont_to_del = None):
        if cont not in self.frames:
            frame = cont(self.container, self)
            self.frames[cont] = frame
            frame.grid(row=0, column=0, sticky='nsew')
            
        tk.Tk.geometry(self, self.shapes[cont])        
        frame = self.frames[cont]
        frame.tkraise() 
        
        if delete:
            del self.frames[cont_to_del]
            
    def on_closing(self):
        for extension in c.FILE_EXTENSIONS:
            try:
                os.remove(machineCodePath + c.TEMP_FILE + extension)
            except Exception:
                pass
        self.destroy()
        
        
class Page_Variables(tk.Frame):
    
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
    Drop = namedtuple('Dropdown', Par._fields + ('list',))
    
    dropdowns = [
                Drop('outline', STR, (COMMON, PART), ds.outlines),
                Drop('pattern', STR, (COMMON, PART,), ds.infills),
                ]
          
    parameters = [
                Par('extrusionFactor', FLOAT_LIST, (COMMON, PART)),
                Par('printSpeed', INT_LIST, (COMMON, PART)),
                Par('shiftX', FLOAT_LIST, (COMMON, PART)),
                Par('shiftY', FLOAT_LIST, (COMMON, PART)),
                Par('shiftZ', FLOAT_LIST, (PART,)),
                Par('numLayers', INT_LIST, (COMMON, PART)),
                Par('designType', INT_LIST, (PART,)),
                Par('infillAngleDegrees', FLOAT_LIST, (COMMON, LAYER)),
                Par('pathWidth', FLOAT_LIST, (LAYER,)),
                Par('layerHeight', FLOAT_LIST, (LAYER,)),
                Par('infillShiftX', FLOAT_LIST, (LAYER,)),
                Par('infillShiftY', FLOAT_LIST, (LAYER,)),
                Par('numShells', INT_LIST, (COMMON, LAYER)),
                Par('brims', INT_LIST, (COMMON, PART)),
                Par('infillOverlap', FLOAT_LIST, (LAYER,)),
                Par('start_Gcode_FileName', STR, (FILE,)),
                Par('end_Gcode_FileName', STR, (FILE,)),
                Par('bed_temp', INT, (COMMON, PRINT)),
                Par('extruder_temp', INT, (COMMON, PRINT)),
                Par('nozzleDiameter', FLOAT, (PRINTER,)),
                Par('horizontalExpansion', FLOAT, (PRINTER,)),
                Par('filamentDiameter', FLOAT, (PRINTER,)),
                Par('RAPID', INT, (PRINTER,)),
                Par('retractDistance', FLOAT, (PRINTER,)),
                Par('retractMinTravel', FLOAT, (PRINTER,)),
                Par('retractSpeed', INT, (PRINTER,)),
                Par('ZHopHeight', FLOAT, (PRINTER,)),
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
        tk.Frame.__init__(self, parent)
        self.controller = controller
        self.lastParameters = {}
        self.elements = {}  
        self.numRows = len(self.dropdowns + self.parameters)
        self.shift = 0
        self.regionParams = None
        self.currJsonPath = self.JSONPATH
        
        global machineCodePath
        
        machineCodePath = self.GCODEPATH
               
        self.fields = []
        for menu in self.menus:
            self.fields.append([par for par in (self.dropdowns + self.parameters) if menu.group in par.groups])

        self.set_all_vars()
        self.set_defaults()
        
        self.current_menu = self.fields[self.COMMON]
            
        self.create_var_page()
        
        self.layerParamsLabels = []
        self.partParamsLabels = []
        for param in self.parameters:
            if self.LAYER in param.groups:
                self.layerParamsLabels.append(param.label)
            elif self.PART in param.groups:
                self.partParamsLabels.append(param.label)
              
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
        
        #this is so if the JSON is saved before a dropdown is edited, it will
        #have all the necessary information (key, value, and type).
        #also makes it so if the same dropdown option as the default is picked
        #before any other option is picked, the program will recognize that
        #and act accordingly     
        for x, dropdown in enumerate(self.dropdowns):
            if x < len(dropdown_defaults):
                del dropdown_defaults[x][c.THE_LABEL]
                if len(dropdown_defaults[x]) > 0:
                    self.shift += 2
                    self.all_vars[x][self.SAVED] = dropdown_defaults[x]
                    if dropdown.label in self.defaults:
                        self.all_vars[x][self.VAR] = self.defaults[dropdown.label]
                    for key, value in dropdown_defaults[x].items():
                        self.all_vars[x][self.KEYS].append(key)
                        self.all_vars[x][self.TYPES][key] = type(value)
        
        #makes the default value of any parameter not found in the JSON be 
        #an empty string
        for param in self.dropdowns + self.parameters:
            if param.label not in self.defaults:
                self.defaults[param.label] = ''           
                
        
    def set_elements(self):
    
        self.doneshapes_menu()
        
        #creates a namedtuple with label, entry, and text_variables parameters; appends namedtuple to a list
        for x, param in enumerate(self.parameters):
            x += 1+len(self.dropdowns)
            curr_label = ttk.Label(self, text= param.label + ' - ' + param.data_type)
            curr_text_variable = tk.StringVar(self, value=self.defaults[param.label])
            curr_entry = ttk.Entry(self, textvariable=curr_text_variable)
            self.elements[param.label] = self.Elem(curr_label, curr_entry, curr_text_variable)
            self.elements[param.label].label.grid(row=x,column=0)
            self.elements[param.label].entry.grid(row=x,column=1,sticky='ew')
            
        #labels for displaying dropdown values in the value bar
        self.var_text = {}
        self.var_labels = {}
        self.var_overall_label = {}
        for x, dropdown in enumerate(self.dropdowns):
            self.var_text[x] = {}
            self.var_labels[x] = {}
            self.var_overall_label[x] = ttk.Label(self, text=dropdown.label)
            for key_or_value in (self.KEYS, self.VALUES):
                self.var_text[x][key_or_value] = tk.StringVar(self)
                self.var_labels[x][key_or_value] = ttk.Label(self, 
                                textvariable=self.var_text[x][key_or_value])
    
    #creates menu of the different possible shapes from the doneshapes class        
    def doneshapes_menu(self):
        
        for x, dropdown in enumerate(self.dropdowns):        
            curr_label = ttk.Label(self, text= dropdown.label + ' - ' + dropdown.data_type)
            curr_text_variable = tk.StringVar(self, value=self.defaults[dropdown.label])
            curr_entry = ttk.OptionMenu(self,
                                        curr_text_variable,
                                        self.defaults[dropdown.label],
                                        *dropdown.list,
                                        command=self.set_var)
            self.elements[dropdown.label] = self.Elem(curr_label, curr_entry, curr_text_variable)
            self.elements[dropdown.label].label.grid(row=x+1,column=0)
            self.elements[dropdown.label].entry.grid(row=x+1,column=1,sticky='ew')
        
    def save_option(self): 
        
        buttonSave = ttk.Button(self,text='Save',command=lambda: self.saveJson())
        buttonSave.grid(row=0,column=1)
      
    def upload_option(self):   
        
        buttonUpload = ttk.Button(self,text='Upload',command=lambda: self.upload())
        buttonUpload.grid(row=0,column=0)
        
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
        self.buttonGcode.grid(row=self.numRows+1+self.shift,column=1)
        
    #create button to switch to 3D model page
    def model_creation(self):  
        
        #button to switch to 3D model page
        self.buttonModel = ttk.Button(self, text='Create 3D Model', command=lambda: self.gen_model())
        self.buttonModel.grid(row=self.numRows+1+self.shift, column=0)
        
    #create radiobutton to switch between gcode and robotcode
    def g_robot(self):
        
        self.g_robot_var = tk.IntVar()
        if self.G_ROBOT_VAR in self.defaults:
            self.g_robot_var.set(self.defaults[self.G_ROBOT_VAR])
        else:
            self.g_robot_var.set(c.GCODE)
        
        self.buttonChooseGcode = ttk.Radiobutton(self, text='Gcode', variable=self.g_robot_var, value=c.GCODE)
        self.buttonChooseGcode.grid(row=self.numRows+2+self.shift,column=0)
        self.buttonChooseRobot = ttk.Radiobutton(self, text='RobotCode', variable=self.g_robot_var, value=c.ROBOTCODE)
        self.buttonChooseRobot.grid(row=self.numRows+2+self.shift,column=1)
       
    def version_num(self):
        
        self.labelVersion = ttk.Label(self, text='Version ' + parameters.__version__)
        self.labelVersion.grid(row=self.numRows+3+self.shift,column=0)
    
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
            #checks if any values are entered
            if len(self.all_vars[x][self.SAVED]) > 0:
                self.var_overall_label[x].grid(row=1+extra_shift, column=0)
                for key, value in self.all_vars[x][self.SAVED].items():
                    text_keys += '%10s ' % (key)
                    if len(str(value)) > 25:
                        value = str(value)
                        value = value[:10] + ' ... ' + value[-10::]
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
        
        #creates data structure-ception to hold the necessary dropdown information
        #essentially is a list of dictionary, each dictionary having a string as the
        #value and a string/list/dict as the value
        #would look like this: [{'' : '', '' : [], '' : {}, '' : {}}, 
        #                       {'' : '', '' : [], '' : {}, '' : {}}]
        for x in range(len(self.dropdowns)):
            self.all_vars.append({})
            for added_key, added_value in ((self.VAR, ''), (self.KEYS, []), (self.TYPES, {}), (self.VALUES, {}), 
                                           (self.STRINGVARS, {}), (self.LABELS, {}), (self.ENTRIES, {}), (self.SAVED, {})):
                self.all_vars[x][added_key] = added_value
    
    #resets a specific doneshape menu's variables              
    def reset_certain_vars(self, vars_to_reset):

        for key, value in self.all_vars[vars_to_reset].items():
            if type(value) == str:
                value = ''
            elif type(value) == dict:
                self.all_vars[vars_to_reset][key].clear()
            elif type(value) == list:
                value[:] = []
                
    def save_fname(self, save_dict, key):
        def command():
            save_dict[key] = filedialog.askopenfilename()
        return command
    
    #creates popup menu to set values for a doneshape function
    def set_var(self, var):
        self.annot = getattr(ds, var).__annotations__ #inspect.getfullargspec(getattr(ds, var)).annotations
        #determines which dropdown menu is currently being used
        for x, dropdown in enumerate(self.dropdowns):
            if var in dropdown.list:
                dropdown_index = x
                label = dropdown.label
               
        self.shift = 0
        for x, dropdown in enumerate(self.dropdowns):
            if len(self.all_vars[x][self.SAVED]) > 0 and label != dropdown.label:
                self.shift += 2

        if len(self.annot) > 1: 
            
            self.shift += 2
            self.regrid()            
            
            var_window = tk.Tk()
            var_window.title(var)
            var_window.geometry('+650+100')  
            
            #checks whether the option is the same as the one chosen last time
            if self.all_vars[dropdown_index][self.VAR] != var:
                self.reset_certain_vars(dropdown_index)
                self.all_vars[dropdown_index][self.VAR] = var
                      
            for x, (key, value) in enumerate(self.annot.items()):
                if key != 'return':
                    self.all_vars[dropdown_index][self.KEYS].append(key)
                    self.all_vars[dropdown_index][self.TYPES][key] = value
                    new_value = str(value).split('\'')[1]
                    self.all_vars[dropdown_index][self.STRINGVARS][key] = tk.StringVar(var_window)
                    if key in self.all_vars[dropdown_index][self.SAVED]:
                        self.all_vars[dropdown_index][self.STRINGVARS][key].set(self.all_vars[dropdown_index][self.SAVED][key])
                    else:
                        self.all_vars[dropdown_index][self.STRINGVARS][key].set(new_value)
                    self.all_vars[dropdown_index][self.LABELS][key] = ttk.Label(var_window, text=key)
                    self.all_vars[dropdown_index][self.LABELS][key].grid(row=x, column=0, padx=5)
                    if key == 'fname':
                        self.all_vars[dropdown_index][self.ENTRIES][key] = ttk.Button(var_window,
                                                                                      text='File',
                                                                                      command=self.save_fname(self.all_vars[dropdown_index][self.SAVED], key))
                    else:
                        self.all_vars[dropdown_index][self.ENTRIES][key] = ttk.Entry(var_window, 
                                                                            textvariable=self.all_vars[dropdown_index][self.STRINGVARS][key])
                    self.all_vars[dropdown_index][self.ENTRIES][key].grid(row=x, column=1, padx=1, pady=1)
                    self.all_vars[dropdown_index][self.VALUES][self.all_vars[dropdown_index][self.ENTRIES][key]] = new_value  
            
            #method that makes it so the entry clears itself upon being clicked when 
            #the data type is the value and fills the entry with the data type if 
            #it's empty
            def default(event):
                current = event.widget
                try:
                    if current.get() == self.all_vars[dropdown_index][self.VALUES][current]:
                        current.delete(0, tk.END)
                    elif current.get() == '':
                        current.insert(0, self.all_vars[dropdown_index][self.VALUES][current]) 
                except Exception:
                    pass
                quicksave(False)
                    
            def quicksave(destroy = True):
                for key in self.all_vars[dropdown_index][self.KEYS]:
                    if key == 'fname':
                        continue
                    self.all_vars[dropdown_index][self.SAVED][key] = self.all_vars[dropdown_index][self.STRINGVARS][key].get()
                self.values_bar()
                if destroy:
                    var_window.destroy()
                   
            for key in self.all_vars[dropdown_index][self.KEYS]:
                self.all_vars[dropdown_index][self.ENTRIES][key].bind('<FocusIn>', default)
                self.all_vars[dropdown_index][self.ENTRIES][key].bind('<FocusOut>', default)

            buttonDestroy = ttk.Button(var_window, text='OK', command=quicksave)
            buttonDestroy.grid(row=len(self.annot.items())+1, column=1)

            #quicksaves if the user closes the window using a method other than the "OK" button
            var_window.protocol('WM_DELETE_WINDOW', quicksave)
            var_window.mainloop()
            
        else:
            self.reset_certain_vars(dropdown_index)
            self.values_bar()
            self.regrid()
            
    #creates error popup message        
    def popup(self, msg, title, size):
        
        popup = tk.Tk()
        
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
        self.model_creation()
        self.g_robot()
        self.version_num()      
        self.regrid()
        
    #############################################
    #   methods that are called from buttons    #
    #############################################
        
    #called from within the "save" method to put a value or list of values into a dictionary
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
                
    def saveJson(self, name = None):
        #Saving JSON
        if name is None:
            jsonFileName = filedialog.asksaveasfilename()
            if not jsonFileName:
                """ The filedialog box was canceled. """
                return None
            jsonFileName = self.removeExtension(jsonFileName)

            jsonFileName += c.FILE_EXTENSIONS[c.JSON] 
            
        #Create a temp json file
        else:
            jsonFileName = self.JSONPATH + name + c.FILE_EXTENSIONS[c.JSON]          
        
        if not os.path.isdir(self.JSONPATH):
            os.makedirs(self.JSONPATH)
        with open(jsonFileName, 'w') as fp:
            json.dump(self.currentParameters(), fp, separators=(',\n',': ')) 
        return jsonFileName
    
    def _writeDict(self, file, _dict, last = False):
        file.write('{')
        for x, (key, value) in enumerate(_dict.items()):
            if x:
                file.write('\t')
            file.write('"'+ key + '"')
            file.write(': ')
            if isinstance(value, str):
                file.write('"'+ value + '"')
            else:
                file.write(str(value))
            if x == len(_dict)-1:
                if last:
                    file.write('}\n')
                else:
                    file.write('},\n')
            else:
                file.write(',\n')
        
    
    def currentParameters(self):
        data = {}              
        dropdown_data = []
        data[self.G_ROBOT_VAR] = self.g_robot_var.get()
        
        #saves the extra dropdown menu data
        for x, dropdown in enumerate(self.dropdowns):
            dropdown_data.append({c.THE_LABEL : dropdown.label})
            if len(self.all_vars[x][self.KEYS]) > 0:
                for key in self.all_vars[x][self.KEYS]:
                    if self.all_vars[x][self.TYPES][key] in (float, int, str):
                        self._save(dropdown_data[x], key, self.all_vars[x][self.TYPES][key], 
                             self.all_vars[x][self.SAVED][key])
        
        #saves the values entered into entry boxes
        for param in self.dropdowns + self.parameters:                   
                
            if param.data_type == self.INT_LIST or param.data_type == self.FLOAT_LIST:
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
                    
        return data, dropdown_data
    
    #accounts for file extensions
    def removeExtension(self, pathName):        
        return os.path.splitext(pathName)[0]
        
    def upload(self):
        uploadname = filedialog.askopenfilename()  
        
        
        if uploadname:
            #gives error messages if user tries to upload a filetype other than .json
            try:
                with open(uploadname, 'r') as fp:
                    data, dropdown_data, *self.regionParams = json.load(fp, object_pairs_hook=OrderedDict)
                    
            except Exception as e:
                if '.json' not in uploadname:
                    print('Error: this is not a JSON file. Please upload a JSON file.')
                else:
                    print('Error uploading file.\n', e)
                    
            else:
                self.currJsonPath = os.path.dirname(uploadname) + '/'                
                for x in range(len(self.dropdowns)):
                    self.reset_certain_vars(x)
                   
                for key, value in data.items():    
                    if data[key] == None:
                        self.elements[key].text_variable.set('None') 
                    elif key == self.G_ROBOT_VAR:
                        self.g_robot_var.set(value)
                    elif key in self.elements.keys():
                        value = str(value)
                        value = value.replace('[','').replace(']','')
                        self.elements[key].text_variable.set(value)  
                
                self.shift = 0
                #deletes the label entry so it doesn't show up in the value bar
                #uploads all necessary dropdown menu data so dropdown menu
                #functions can act appropriately
                for x, dropdown in enumerate(self.dropdowns):
                    del dropdown_data[x][c.THE_LABEL]
                    if len(dropdown_data[x]) > 0:
                        self.shift += 2
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
                    
# TODO: Save gcode during 3D model creation so it doesn't have to be re-run if converted    
    #create Gcode file; creates temp JSON file then deletes it                    
    def convert(self, *, temp = False):
        global data_points  
        
        if temp:
            machCodeName = self.GCODEPATH + c.TEMP_FILE

        else:
            machCodeName = filedialog.asksaveasfilename()
            if not machCodeName:
                """ The dialog box was cancelled. """
                return
            machCodeName = self.removeExtension(machCodeName)
        
        machCodeName += c.FILE_EXTENSIONS[self.g_robot_var.get()]

        tempFileName = (self.GCODEPATH
                        + c.TEMP_FILE
                        + c.FILE_EXTENSIONS[self.g_robot_var.get()])
        if self.lastParameters == self.currentParameters():
            if temp:
                return
            try:
                shutil.copyfile(tempFileName, machCodeName)
            except Exception:
                pass
            else:
                print('\nMachine code written to:', machCodeName)
                return

        jsonFileName = self.saveJson(c.TEMP_FILE) 
                
        conversion = Runner(jsonFileName,
                            tempFileName,
                            self.g_robot_var.get(),
                            self.layerParamsLabels,
                            self.partParamsLabels)
        data_points = conversion.run()
        
        self.lastParameters = self.currentParameters()
        
        os.remove(jsonFileName)
        if not temp:
            try:
                shutil.copyfile(tempFileName, machCodeName)
            except Exception as e:
                print('Error copying temporary machine code file to final file' + 
                      '\n please double check file name:', machCodeName)
                raise e
            else:
                print('Results written to:', machCodeName)
    
    #create popup 3D model viewer; creates temp JSON and temp Gcode files then deletes both       
    def gen_model(self):
        
        try:
            self.convert(temp=True)
            
        except Exception as e:
            print('Error during calculations.')
            raise(e)
            
        else:
            #3D model data setup and creation
            pv = ProjectionViewer(1000, 750)
            model = Wireframe()
            
            data = pv.parse_data()

            model.addNodes([point for point in data])
            model.addEdges([(n,n+1) for n in range(0,len(data),2)])
            
            pv.addWireframe(c.MODEL, model)
            try:
                pv.run()
            #needed become it always gives error message when 3D model page is closed
            except Exception as e:
                if str(e) == 'display Surface quit':
                    print('You have closed the 3D model.')
                else:
                    print('Flag this message in RUN_ME.py\n' + str(e))
                    raise e

#3D model controls            
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
    pygame.K_c:      (lambda x: x.shift_down()),
    pygame.K_r:      (lambda x: x.max_layers()),
    pygame.K_f:      (lambda x: x.one_layer()),}
    
            
class ProjectionViewer:
    ''' Displays 3D objects on a Pygame screen '''

    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.screen = pygame.display.set_mode((width, height), pygame.RESIZABLE)
        pygame.display.set_caption('Wireframe Display')
        self.background = (255,255,255)

        self.wireframes = {}
        self.displayEdges = True
        self.label_color = (0,0,0)
        self.color_increment = 50
        self.color_cap = 220 - self.color_increment
        
        self.start = 0
        self.end = 0
        
        self.error_text = ''
        
    def parse_data(self):
        
        data = []
#        counter = 0
        self.layer_part = []
        LayerIndexes = namedtuple('LayerIndexes', 'layerNum partNum startIndex endIndex')
        
        for partNum, part in enumerate(data_points):
            for layerNum, layer in enumerate(part):
                start = len(data)//2
                data.extend(layer)
                end = len(data)//2
                self.layer_part.append(LayerIndexes(layerNum+1, partNum+1, start, end))
        self.end = len(self.layer_part)-1
        return data

    def addWireframe(self, name, wireframe):
        ''' Add a named wireframe object. '''

        self.wireframes[name] = wireframe

    def run(self):
        ''' Create a pygame screen until it is closed. '''
        pygame.init()
        self.myfont = pygame.font.SysFont('monospace', 15)
        
        #automatically translates image to center of window
        x, y = self.screen.get_size()
        self.translateAll('x', (x/2-self.wireframes[c.MODEL].findcenter()[0]))
        self.translateAll('y', (y/2-self.wireframes[c.MODEL].findcenter()[1]))
        self.scaleAll(4)
        
        while True:
            self.r = 0
            self.b = 0
            self.g = 0
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    
                elif event.type == pygame.KEYDOWN:
                    if event.key in key_to_function:
                        key_to_function[event.key](self)
                        
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    if event.button == 4:
                        self.scaleAll(1.25)
                    elif event.button == 5:
                        self.scaleAll(0.8)
                elif event.type == pygame.MOUSEMOTION:
                    if event.buttons[0]:
                        shiftX, shiftY = event.rel
                        self.translateAll('x', shiftX)
                        self.translateAll('y', -shiftY)
                    elif event.buttons[2]:
                        rotY, rotX = event.rel
                        self.rotateAll('X', rotX/270)
                        self.rotateAll('Y', rotY/270)
                        
                elif event.type == pygame.VIDEORESIZE:
                    os.environ['SDL_VIDEO_WINDOW_POS'] = '' # Clears the default window location
                    self.width, self.height = event.dict['size']
                    self.screen = pygame.display.set_mode(event.dict['size'], pygame.RESIZABLE)
                    
            self.display()  
            pygame.display.flip()

    def display(self):
        ''' Draw the wireframes on the screen. '''

        self.screen.fill(self.background)

        text = []
        #Part and Layer numbers change to accurately reflect the parts/layers being shown
        text.append('Showing Part ' + str(self.layer_part[self.start].partNum)
                + ' Layer ' + str(self.layer_part[self.start].layerNum)
                + ' through Part ' + str(self.layer_part[self.end].partNum)
                + ' Layer ' + str(self.layer_part[self.end].layerNum)
                + '  (' + str(self.end - self.start + 1) + ' layers total)')
        
        text.append('Left click mouse to Pan | Scroll Wheel to Zoom | Right Click for rotate')
        text.append('1/2 = zoom in/out | q/w = rotate X-axis | a/s = rotate Y-axis | z/x = rotate Z-axis')        
        text.append('e/d = add/subtract layers | 3/c = shift layers up/down | r/f = show all/one layer(s)')        
        text.append('Line color gradually changes from BLK > RED > OR > YEL > GRY in the order printed')
        text.append('Line colors will repeat the cycle in the middle of shapes if there are a lot of lines')

        for x, line in enumerate(text):
            label = self.myfont.render(line, 1, self.label_color)
            self.screen.blit(label, (0, x*25))
            
        error_label = self.myfont.render(self.error_text, 1, self.label_color)
        self.screen.blit(error_label, (25,self.screen.get_size()[1]-25))
                
        #creates 3D model
        wireframe = self.wireframes[c.MODEL]
        if self.displayEdges:            
            #adjusts color incrementation to the amount of lines being displayed
            #tries to divide colors up evenly so it goes through one cycle of colors, but if there are
            #so many lines that the incrementation would be 0, it defaults to 1 and just cycles through
            #the colors multiples times
            self.color_increment = int(255 * 3
                                       / len(wireframe.edges[self.layer_part[self.start].startIndex
                                                             : self.layer_part[self.end].endIndex]))
            if self.color_increment > 219:
                self.color_increment = 219
            elif self.color_increment == 0:
                self.color_increment = 1
            self.color_cap = 220 - self.color_increment     #220 is used so lines never get too light of a color            
            
            #prints each edge, adjusts color for each line
            for edge in wireframe.edges[self.layer_part[self.start].startIndex
                                        : self.layer_part[self.end].endIndex]:
                if self.r < self.color_cap:
                    self.r += self.color_increment
                elif self.g < self.color_cap:
                    self.g += self.color_increment
                elif self.b < self.color_cap:
                    self.b += self.color_increment
                else:
                    self.r = 0
                    self.g = 0
                    self.b = 0
                color = (self.r, self.g, self.b)
                pygame.draw.line(self.screen,
                                 color,
                                 (edge.start.x, self.height-edge.start.y),
                                 (edge.stop.x, self.height-edge.stop.y),
                                 4) # Line Width
                    
    def translateAll(self, axis, d):
        ''' Translate all wireframes along a given axis by d units. '''

        wireframe = self.wireframes[c.MODEL]
        wireframe.translate(axis, d)

    def scaleAll(self, scale):
        ''' Scale all wireframes by a given scale, centerd on the center of the screen. '''

        center_x = self.width/2
        center_y = self.height/2

        wireframe = self.wireframes[c.MODEL]
        wireframe.scale(center_x, center_y, scale)
            
    def rotateAll(self, axis, theta):
        ''' Rotate all wireframe about their center, along a given axis by a given angle. '''

        rotateFunction = 'rotate' + axis

        wireframe = self.wireframes[c.MODEL]
        center = wireframe.findcenter()
        getattr(wireframe, rotateFunction)(center[0], center[1], center[2], theta)
            
    def add(self):
        ''' Increases the amount of layers shown. '''
        
        self.error_text = ''
        
        if self.end < (len(self.layer_part)-1):
            self.end += 1
        elif self.start > 0:
            self.start -= 1  
        else:
            self.error_text = 'Showing all parts and layers.'
            
    def subtract(self):
        ''' Decreases the amount of layers shown. '''
        
        self.error_text = ''
        if self.end > (self.start):
            self.end -= 1            
        else:
            self.error_text = 'Showing one layer of one part already.'
            
    def shift_up(self):
        ''' Shifts the layers being viewed up by one. '''
        
        self.error_text = ''
        
        if self.end < (len(self.layer_part)-1):
            self.start += 1
            self.end += 1
        else:
            self.error_text = 'Showing the topmost layers already.'
            
    def shift_down(self):
        ''' Shifts the layers being viewed down by one. '''
        
        self.error_text = ''
        
        if self.start > 0:
            self.start -= 1
            self.end -= 1
        else:
            self.error_text = 'Showing the lowest layers already.'
            
    def one_layer(self):
        ''' Decreases amount of layers shown to one. '''
        
        self.error_text = ''
        
        if self.end != self.start:
            self.end = self.start
        else:
            self.error_text = 'Showing the lowest layers already.'
        
    def max_layers(self):
        ''' Increases the amount of layers shown to the maximum. '''
        
        self.error_text = ''
        
        if self.end == len(self.layer_part) and self.start == 0:
            self.error_text = 'All layers already being shown.'
        else:
            self.end = len(self.layer_part)-1
            self.start = 0
    
#only works if program is used as the main program, not as a module    
if __name__ == '__main__': 
    
    gui = GUI()
    gui.mainloop() 