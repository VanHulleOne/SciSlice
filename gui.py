# -*- coding: utf-8 -*-
"""
Created on Sat May 28 16:39:58 2016
@author: Alex Diebold
"""

from tkinter import *               #GUI module
from tkinter import ttk             #for styling purposing
from tkinter import filedialog      #window for saving and uploading files
import json                         #for saving and uploading files
from main import Main        #for converting to Gcode

class GUI(Tk):

    def __init__(self, *args, **kwargs):
        Tk.__init__(self, *args, **kwargs)
        
        
        container = Frame(self)
        container.pack(side="top", fill="both", expand=True)
        container.grid(row=0,column=0)
        
        #set window title
        self.title("3D Printer Parameter Setter")
        #format window size -- width=500, height=475, 100px from left of screen, 100px from top of screen
        #self.geometry("500x475+100+100")
        
        #dictionary of Frames
        self.frames = {}
        
        #add Frames to dictionary
        for F in (Page_Variables, Page_Model):
        
            frame = F(container, self)
            
            self.frames[F] = frame
            
            frame.grid(row=0, column=0, sticky="nsew")
        
        #show initial Frame
        self.show_frame(Page_Variables)
       
    #show frame
    def show_frame(self, cont):
        
        frame = self.frames[cont]
        frame.tkraise() 
        
class Page_Variables(Frame):
    
    def __init__(self, parent, controller):
        Frame.__init__(self, parent)
        self.controller = controller

        ########################
        #   class variables    #
        ########################
        
        #string that is the filename of the current file
        self.filename = ""
        
        #dictionary with variable name as key and StringVar as value
        self.text_variable = {} 
        
        #dictionary with variable name as key and Label as value        
        self.labels = {}
                   
        #dictionary with variable name as key and Entry as value
        self.entries = {}
        
        #array of Strings of the variables
        self.texts = ["outline", "solidityRatio", "printSpeed", "shiftX",            #part parameters
                 "shiftY", "firstLayerShiftZ", "numLayers",                         #part parameters
                 "pattern", "designType",                                           #part parameters
                 "inFillAngleDegrees", "pathWidth", "layerHeight",                  #layer parameters
                 "inFillShiftX", "inFillShiftY", "numShells", "trimAdjust",         #layer parameters
                 "start_Gcode_FileName", "end_Gcode_FileName"]                      #file parameters
                 
        #array of Strings of the commonly used variables
        self.common_texts = ["outline", "solidityRatio", "printSpeed", 
                        "shiftX", "shiftY", "pattern", "numShells"]
                      
        #array of Strings of the default values
        self.defaults = ["regularDogBone", "1.09", "2000", "10, 50",                #part parameters
                    "10, 35, 60", "0", "8",                                         #part parameters
                    "None", "0",                                                    #part parameters
                    "0, -45, 90, 45, 45, 90, -45", "0.5", "0.4",                    #layer parameters
                    "0", "0", "13,1,1,0,0,1,1", "2*c.EPSILON",                      #layer parameters
                    "Start_Gcode_Taz5.txt", "End_Gcode_Taz5.txt"]                   #file parameters   
                    
        self.create_var_page()
              
    ##########################################################
    #   methods that create labels, entries, and/or buttons  #
    ##########################################################
              
    #initial creation of labels
    def set_labels(self):
        
        #create all labels
        for x in range(0, len(self.texts)):
            #create label
            self.labels[self.texts[x]] = Label(self, text=self.texts[x])
            
        #show commonly used variables
        for x in range(0,len(self.common_texts)):
            #use grid() after creating label or dictionary value will be "NoneType"
            self.labels[self.common_texts[x]].grid(row=x+1,column=0)   
            
    #initial creation of entries
    def set_entries(self):
        
        #create all StringVars
        for x in range(0, len(self.texts)):
            #set textvariable to StringVar with default text as value
            self.text_variable[self.texts[x]] = StringVar(self, value=self.defaults[x])
            
        #create all entries
        for x in range(0, len(self.texts)):
            #create entry 
            self.entries[self.texts[x]] = ttk.Entry(self, textvariable=self.text_variable[self.texts[x]])
            
        #show commonly used variables
        for x in range(0, len(self.common_texts)):
            #use grid() after creating entry or dictionary value will be "NoneType"
            self.entries[self.common_texts[x]].grid(row=x+1,column=1)
        
    #creates button for saving all values
    def save_option(self): 
        
        #create button
        buttonSave = ttk.Button(self,text="Save (exclude .json)",command=lambda: self.save()).grid(row=0,column=1)
    
    #creates label, entry, and button for uploading all values    
    def upload_option(self):   
        
        #create button
        buttonUpload = ttk.Button(self,text="Upload",command=lambda: self.upload()).grid(row=0,column=0)
        
    #create menu of label and buttons to switch between tabs
    def tab_buttons(self):
        
        #label for parameters
        labelParameters = Label(self,text="Parameters")
        labelParameters.grid(row=0,column=2)
        
        #button to display all variables
        buttonAll = ttk.Button(self,text="All",command=lambda: self.use_all())
        buttonAll.grid(row=1,column=2)
        #button to display commonly used variables
        buttonCommon = ttk.Button(self,text="Common",command=lambda: self.use_common())
        buttonCommon.grid(row=2,column=2)
        #button to display part parameters
        buttonParts = ttk.Button(self,text="Parts",command=lambda: self.use_parts())
        buttonParts.grid(row=3,column=2)
        #button to display layer parameters
        buttonLayers = ttk.Button(self,text="Layers",command=lambda: self.use_layers())
        buttonLayers.grid(row=4,column=2)
        #button to display file parameters
        buttonFiles = ttk.Button(self,text="Files",command=lambda: self.use_files()).grid(row=5,column=2)
        
    #create label and buttons for different preset values of parameters
    def presets(self):
        
        #label for presets
        labelPresets = Label(self,text="Presets").grid(row=0,column=3)
        #button for dogbone
        buttonDogbone = ttk.Button(self,text="Dogbone",command=lambda: self.dogbone())
        buttonDogbone.grid(row=1,column=3)
    
    #create button to convert to Gcode
    def gcode(self):
        
        buttonGcode = ttk.Button(self,text="Convert to Gcode",command=lambda: self.convert())
        buttonGcode.grid(row=len(self.texts)+1,column=1)
        
    #all set up functions together
    def create_var_page(self):
        
        self.set_labels()
        self.set_entries()
        self.save_option()
        self.upload_option()
        self.tab_buttons()
        self.presets()
        self.gcode()
        self.to_model()
    
    #create button to switch to 3D model page
    def to_model(self):  
        
        #button to switch to 3D model page
        buttonModel = ttk.Button(self, text="3D Model", 
                             command=lambda: self.controller.show_frame(Page_Model))
        buttonModel.grid(row=len(self.texts)+1,column=0)
        
    #############################################
    #   methods that are called from buttons    #
    #############################################
        
    #saves the dictionary of the StringVars to a JSON file    
    def save(self):

        data = {}               #dictionary to put String value of StringVar values in
        self.filename = filedialog.asksaveasfilename()   #creates window to get filename
        self.filename = self.filename + ".json"               #adds .json to name
        
        #check if the user cancelled saving the file
        if self.filename != "":
            to_string = ["outline", "start_Gcode_FileName", "end_Gcode_FileName"]      #variables with type String                
            to_int = ["designType", "firstLayerShiftZ"]           #variables with type int
            to_string_array = ["trimAdjust"]                      #variables with type String that go in an array
            to_int_array = ["printSpeed", "shiftX", "shiftY",     #variables with type int that go in an array
                            "numLayers", "inFillAngleDegrees"
                            "inFillShiftX", "inFillShiftY", "numShells"]
            to_float_array = ["solidityRatio", "pathWidth",      #variables with type double that go in an array
                               "layerHeight"]
            to_none = ["pattern"]                                 #variables with type None
            for key in self.text_variable:
                if key in to_string:
                    data[key] = self.text_variable[key].get()
                elif key in to_int:
                    data[key] = int(self.text_variable[key].get())   #converts value to int
                elif key in to_none:
                    data[key] = None                            #converts value to None
                elif key in to_string_array:
                    temp = []                                   #creates empty array
                    value = self.text_variable[key].get()            #sets the value to a variable
                    if " " in value:
                        value = value.replace(" ", ",")                 #replaces spaces with commas
                    if ",," in value:
                        value = value.replace(",,", ",")                #replaces double commas with single commas
                    temp = value.split(",")                     #creates list split by commas
                    data[key] = temp                            #saves list
                elif key in to_int_array:
                    temp = []
                    value = self.text_variable[key].get()
                    if " " in value:
                        value = value.replace(" ", ",")
                    if ",," in value:
                        value = value.replace(",,", ",")
                    temp = value.split(",")
                    temp = [int(i) for i in temp]               #converts values in list to int before saving
                    data[key] = temp
                elif key in to_float_array:
                    temp = []
                    value = self.text_variable[key].get()
                    if " " in value:
                        value = value.replace(" ", ",")
                    if ",," in value:
                        value = value.replace(",,", ",")
                    temp = value.split(",")
                    temp = [float(i) for i in temp]             #converts values in list to float before saving
                    data[key] = temp
                    
            with open(self.filename, 'w') as fp:
                json.dump(data, fp)    #save JSON file
        
    #uploads dictionary from JSON file to replace current StringVar values, opens window to find file       
    def upload(self):

        data = {}               #new dictionary that will be replaced with dictionary from JSON file
        uploadname = filedialog.askopenfilename()     #creates window to find file
        
        with open(uploadname, 'r') as fp:
            data = json.load(fp)    #upload JSON file
            
        for key in data:
            if data[key] == None:
                self.text_variable[key].set("None") #replace current StringVar with String "None"
            else:
                value = str(data[key])
                value = value.replace("[","")
                value = value.replace("]","")
                self.text_variable[key].set(value)   #replace current StringVar values with data from JSON file
        
    #switch to tab with all parameters    
    def use_all(self):
        
        for x in range(0, len(self.labels)):
            self.labels[self.texts[x]].grid(row=x+1,column=0)    #show labels
            self.entries[self.texts[x]].grid(row=x+1,column=1)   #show entries
        
    def use_common(self):
        
        for x in range(0,len(self.texts)):
            self.labels[self.texts[x]].grid_forget()      #hide labels
            self.entries[self.texts[x]].grid_forget()     #hide entries
            
        for x in range(0,len(self.common_texts)):
            self.labels[self.common_texts[x]].grid(row=x+1,column=0)      #show labels
            self.entries[self.common_texts[x]].grid(row=x+1,column=1)     #show entries
        
    #switch to tab with only part parameters
    def use_parts(self):
        
        for x in range(0,9):
            self.labels[self.texts[x]].grid(row=x+1,column=0)   #show labels
            self.entries[self.texts[x]].grid(row=x+1,column=1)  #show entries
            
        for x in range(9, len(self.texts)):
            self.labels[self.texts[x]].grid_forget()    #hide labels
            self.entries[self.texts[x]].grid_forget()   #hide entries
      
    #switch to tab with only layer parameters  
    def use_layers(self):
        
        for x in range(9,16):
            self.labels[self.texts[x]].grid(row=x-8,column=0)     #show labels
            self.entries[self.texts[x]].grid(row=x-8,column=1)    #show entries
            
        for x in range(16, len(labels)):
            self.labels[self.texts[x]].grid_forget()      #hide labels
            self.entries[self.texts[x]].grid_forget()     #hide entries
            
        for x in range(0,9):
            self.labels[self.texts[x]].grid_forget()      #hide labels
            self.entries[self.texts[x]].grid_forget()     #hide entries
      
    #switch to tabe with only file parameters  
    def use_files(self):
            
        for x in range(16,len(self.labels)):
            self.labels[self.texts[x]].grid(row=x-15,column=0)     #show labels
            self.entries[self.texts[x]].grid(row=x-15,column=1)    #show entries
            
        for x in range(0,16):
            self.labels[self.texts[x]].grid_forget()      #hide labels
            self.entries[self.texts[x]].grid_forget()     #hide entries
        
    #change values to dogbone preset    
    def dogbone(self):
        
        dogbone_data = ["regularDogBone", "1.09", "2000", "10, 50",                #part parameters
                "10, 35, 60", "0", "8",                                                 #part parameters
                "None", "0",                                                            #part parameters
                "0, -45, 90, 45, 45, 90, -45", "0.5", "0.4",                            #layer parameters
                "0", "0", "13,1,1,0,0,1,1",  "2*c.EPSILON",                             #layer parameters
                "'ZigZag.gcode'", "'Start_Gcodee_Taz5.txt'", "'End_Gcode_Taz5.txt'",    #file parameters
                "currPath + '\\Gcode'", "currPath + '\\Start_End_Gcode'"]               #file parameters
                
        for x in range(0,len(self.texts)):
            self.text_variable[self.texts[x]].set(dogbone_data[x])        #change values to dogbone values
    
    #create Gcode file        
    def convert(self):

        #save file
        self.save()
        
        #check if the user cancelled converting to Gcode
        if self.filename != "":
            #convert to Gcode
            conversion = Main(self.filename)
            conversion.run()
    
class Page_Model(Frame):
    
    def __init__(self, parent, controller):
        Frame.__init__(self, parent)
        self.controller = controller
        
        labelExample = Label(self, text="HELLO")
        labelExample.pack()
        
        self.to_variable()
        
    def to_variable(self):
        
        buttonVariable = ttk.Button(self, text="Variables", 
                                command=lambda: self.controller.show_frame(Page_Variables))
        buttonVariable.pack()
    
#only works if program is used as the main program, not as a module    
#if __name__ == '__main__':
    

#####################
#   GUI creation    #
#####################

#create GUI
gui = GUI()

#keeps GUI open, always necessary
gui.mainloop() 