# -*- coding: utf-8 -*-
"""
Created on Sat May 28 16:39:58 2016
@author: Alex Diebold
"""

from tkinter import *               #GUI module
from tkinter import filedialog      #window for saving and uploading files
import json                         #for saving and uploading files
from main import Main        #for converting to Gcode

#########################
#   global variables    #
#########################

#string that is the filename of the current file
filename = ""

#dictionary with variable name as key and StringVar as value
text_variable = {} 

#dictionary with variable name as key and Label as value        
labels = {}
           
#dictionary with variable name as key and Entry as value
entries = {}

#part parameters = outline(0) - designType(8)
#layer parameters = inFilleAngleDegrees(9) - trimAdust(15)
#file parameters = outputFileName(16) - startEndSubDirectory(20)

#array of Strings of the variables
texts = ["outline", "solidityRatio", "printSpeed", "shiftX",                #part parameters
         "shiftY", "firstLayerShiftZ", "numLayers",                         #part parameters
         "pattern", "designType",                                           #part parameters
         "inFillAngleDegrees", "pathWidth", "layerHeight",                  #layer parameters
         "inFillShiftX", "inFillShiftY", "numShells", "trimAdjust",         #layer parameters
         "start_Gcode_FileName", "end_Gcode_FileName"]                      #file parameters
         
#array of Strings of the commonly used variables
common_texts = ["outline", "solidityRatio", "printSpeed", 
                "shiftX", "shiftY", "pattern", "numShells"]
              
#array of Strings of the default values
defaults = ["regularDogBone", "1.09", "2000", "10, 50",                #part parameters
            "10, 35, 60", "0", "8",                                         #part parameters
            "None", "0",                                                    #part parameters
            "0, -45, 90, 45, 45, 90, -45", "0.5", "0.4",                    #layer parameters
            "0", "0", "13,1,1,0,0,1,1", "2*c.EPSILON",                      #layer parameters
            "Start_Gcode_Taz5.txt", "End_Gcode_Taz5.txt"]              #file parameters
         
          
##########################################################
#   methods that create labels, entries, and/or buttons  #
##########################################################
          
#initial creation of labels
def set_labels():
    global labels              #dictionary of labels
    global texts               #array of variable names
    global common_texts        #array of commonly used variable names
    
    #create all labels
    for x in range(0, len(texts)):
        #create label
        labels[texts[x]] = Label(root, text=texts[x])
        
    #show commonly used variables
    for x in range(0,len(common_texts)):
        #use grid() after creating label or dictionary value will be "NoneType"
        labels[common_texts[x]].grid(row=x+1,column=0)   
        
    return   
        
#initial creation of entries
def set_entries():
    global text_variable    #dictionary of StringVar() with default text as the value
    global entries          #dictionary of entries
    global texts            #array of variable names
    global common_texts     #array of commonly used variable names
    global defaults         #array of default values
    
    #create all StringVars
    for x in range(0, len(texts)):
        #set textvariable to StringVar with default text as value
        text_variable[texts[x]] = StringVar(root, value=defaults[x])
        
    #create all entries
    for x in range(0, len(texts)):
        #create entry 
        entries[texts[x]] = Entry(root, textvariable=text_variable[texts[x]])
        
    #show commonly used variables
    for x in range(0, len(common_texts)):
        #use grid() after creating entry or dictionary value will be "NoneType"
        entries[common_texts[x]].grid(row=x+1,column=1)
        
    return 
    
#creates button for saving all values
def save_option(): 
    #create button
    buttonSave = Button(root,text="Save (exclude .json)",command=save).grid(row=0,column=1)

#creates label, entry, and button for uploading all values    
def upload_option():   
    #create button
    buttonUpload = Button(root,text="Upload",command=upload).grid(row=0,column=0)
    
#create menu of label and buttons to switch between tabs
def tab_buttons():
    
    #label for parameters
    labelParameters = Label(root,text="Parameters")
    labelParameters.grid(row=0,column=2)
    
    #button to display all variables
    buttonAll = Button(root,text="All",command=use_all)
    buttonAll.grid(row=1,column=2)
    #button to display commonly used variables
    buttonCommon = Button(root,text="Common",command=use_common)
    buttonCommon.grid(row=2,column=2)
    #button to display part parameters
    buttonParts = Button(root,text="Parts",command=use_parts)
    buttonParts.grid(row=3,column=2)
    #button to display layer parameters
    buttonLayers = Button(root,text="Layers",command=use_layers)
    buttonLayers.grid(row=4,column=2)
    #button to display file parameters
    buttonFiles = Button(root,text="Files",command=use_files).grid(row=5,column=2)
    
#create label and buttons for different preset values of parameters
def presets():
    
    #label for presets
    labelPresets = Label(root,text="Presets").grid(row=0,column=3)
    #button for dogbone
    buttonDogbone = Button(root,text="Dogbone",command=dogbone)
    buttonDogbone.grid(row=1,column=3)

#create button to convert to Gcode
def gcode():
    global texts        #array of variable names, only used to reference length
    
    buttonGcode = Button(root,text="Convert to Gcode",command=convert)
    buttonGcode.grid(row=len(texts)+1,column=1)

        
#############################################
#   methods that are called from buttons    #
#############################################
    
#saves the dictionary of the StringVars to a JSON file    
def save():
    global text_variable    #dictionary of StringVar with current values from user
    global filename         #string of the name to save the file as
    data = {}               #dictionary to put String value of StringVar values in
    filename = filedialog.asksaveasfilename()   #creates window to get filename
    filename = filename + ".json"               #adds .json to name
    to_string = ["outline", "start_Gcode_FileName", "end_Gcode_FileName"]      #variables with type String                
    to_int = ["designType", "firstLayerShiftZ"]           #variables with type int
    to_string_array = ["trimAdjust"]                      #variables with type String that go in an array
    to_int_array = ["printSpeed", "shiftX", "shiftY",     #variables with type int that go in an array
                    "numLayers", "inFillAngleDegrees"
                    "inFillShiftX", "inFillShiftY", "numShells"]
    to_float_array = ["solidityRatio", "pathWidth",      #variables with type double that go in an array
                       "layerHeight"]
    to_none = ["pattern"]                                 #variables with type None
    for key in text_variable:
        if key in to_string:
            data[key] = text_variable[key].get()
        elif key in to_int:
            data[key] = int(text_variable[key].get())   #converts value to int
        elif key in to_none:
            data[key] = None                            #converts value to None
        elif key in to_string_array:
            temp = []                                   #creates empty array
            value = text_variable[key].get()            #sets the value to a variable
            if " " in value:
                value = value.replace(" ", ",")                 #replaces spaces with commas
            if ",," in value:
                value = value.replace(",,", ",")                #replaces double commas with single commas
            temp = value.split(",")                     #creates list split by commas
            data[key] = temp                            #saves list
        elif key in to_int_array:
            temp = []
            value = text_variable[key].get()
            if " " in value:
                value = value.replace(" ", ",")
            if ",," in value:
                value = value.replace(",,", ",")
            temp = value.split(",")
            temp = [int(i) for i in temp]               #converts values in list to int before saving
            data[key] = temp
        elif key in to_float_array:
            temp = []
            value = text_variable[key].get()
            if " " in value:
                value = value.replace(" ", ",")
            if ",," in value:
                value = value.replace(",,", ",")
            temp = value.split(",")
            temp = [float(i) for i in temp]             #converts values in list to float before saving
            data[key] = temp
            
    with open(filename, 'w') as fp:
        json.dump(data, fp)    #save JSON file
        
    return
    
#uploads dictionary from JSON file to replace current StringVar values, opens window to find file       
def upload():
    global text_variable    #dictionary of StringVar of the entry values
    data = {}               #new dictionary that will be replaced with dictionary from JSON file
    uploadname = filedialog.askopenfilename()     #creates window to find file
    
    with open(uploadname, 'r') as fp:
        data = json.load(fp)    #upload JSON file
        
    for key in data:
        if data[key] == None:
            text_variable[key].set("None") #replace current StringVar with String "None"
        else:
            value = str(data[key])
            value = value.replace("[","")
            value = value.replace("]","")
            text_variable[key].set(value)   #replace current StringVar values with data from JSON file
        
    return
    
#switch to tab with all parameters    
def use_all():
    global labels       #dictionary with labels as values
    global entries      #dictionary with entries as values
    global texts        #array of variable names
    
    for x in range(0, len(labels)):
        labels[texts[x]].grid(row=x+1,column=0)    #show labels
        entries[texts[x]].grid(row=x+1,column=1)   #show entries
        
    return
    
def use_common():
    global labels               #dictionary with labels as values
    global entries              #dictionary with entries as values
    global texts                #dictionary of variable names
    global common_texts         #array of commonly used variable names 
    
    for x in range(0,len(texts)):
        labels[texts[x]].grid_forget()      #hide labels
        entries[texts[x]].grid_forget()     #hide entries
        
    for x in range(0,len(common_texts)):
        labels[common_texts[x]].grid(row=x+1,column=0)      #show labels
        entries[common_texts[x]].grid(row=x+1,column=1)     #show entries
    
#switch to tab with only part parameters
def use_parts():
    global labels       #dictionary with labels as values
    global entries      #dictionary with entries as values
    global texts        #array of variable names
    
    for x in range(0,9):
        labels[texts[x]].grid(row=x+1,column=0)   #show labels
        entries[texts[x]].grid(row=x+1,column=1)  #show entries
        
    for x in range(9, len(texts)):
        labels[texts[x]].grid_forget()    #hide labels
        entries[texts[x]].grid_forget()   #hide entries
        
    return
  
#switch to tab with only layer parameters  
def use_layers():
    global labels       #dictionary with labels as values
    global entries      #dictionary with entries as values
    global texts        #array of variable names
    
    for x in range(9,16):
        labels[texts[x]].grid(row=x-8,column=0)     #show labels
        entries[texts[x]].grid(row=x-8,column=1)    #show entries
        
    for x in range(16, len(labels)):
        labels[texts[x]].grid_forget()      #hide labels
        entries[texts[x]].grid_forget()     #hide entries
        
    for x in range(0,9):
        labels[texts[x]].grid_forget()      #hide labels
        entries[texts[x]].grid_forget()     #hide entries
        
    return
  
#switch to tabe with only file parameters  
def use_files():
    global labels       #dictionary with labels as values
    global entries      #dictionary with entries as values
    global texts        #array of variable names
        
    for x in range(16,len(labels)):
        labels[texts[x]].grid(row=x-15,column=0)     #show labels
        entries[texts[x]].grid(row=x-15,column=1)    #show entries
        
    for x in range(0,16):
        labels[texts[x]].grid_forget()      #hide labels
        entries[texts[x]].grid_forget()     #hide entries
    
    return
    
#change values to dogbone preset    
def dogbone():
    global texts            #array of variable names
    global text_variable    #dictionary with StringVar as values
    
    dogbone_data = ["regularDogBone", "1.09", "2000", "10, 50",                #part parameters
            "10, 35, 60", "0", "8",                                                 #part parameters
            "None", "0",                                                            #part parameters
            "0, -45, 90, 45, 45, 90, -45", "0.5", "0.4",                            #layer parameters
            "0", "0", "13,1,1,0,0,1,1",  "2*c.EPSILON",                             #layer parameters
            "'ZigZag.gcode'", "'Start_Gcodee_Taz5.txt'", "'End_Gcode_Taz5.txt'",    #file parameters
            "currPath + '\\Gcode'", "currPath + '\\Start_End_Gcode'"]               #file parameters
            
    for x in range(0,len(texts)):
        text_variable[texts[x]].set(dogbone_data[x])        #change values to dogbone values
        
def convert():
    global filename    #string of name to save file as
    #save file
    save()
    
    conversion = Main(filename)
    conversion.run()
    
    
#only works if program is used as the main program, not as a module    
#if __name__ == '__main__':
    

#####################
#   GUI creation    #
#####################

#create window    
root = Tk()

#set window title
root.title("3D Printer Parameter Setter")
#format window size -- width=500, height=600, 100px from left of screen, 100px from top of screen
root.geometry("500x475+100+100")

#initial creation of labels and entries
set_labels()
set_entries()

#set up save option
save_option()

#set up upload option
upload_option()

#tab buttons (commonly used, all, part, layer, and file parameters)
tab_buttons()

#preset buttons (dogbone)
presets()

#convert to Gcode button
gcode()

#keeps GUI open, always necessary
root.mainloop() 