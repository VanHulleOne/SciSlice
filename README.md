# DogBone v1.2

DogBone is a program that creates custom tool paths for Fused Filament Fabrication
3D printers (also known by the trade marked term FDM). The motivation for creating
this program was to allow the user to independently adjust as many printing
parameters as possible for the purpose of researching and characterizing each
parameter's effect on a part's properties.

Version 1 can only produce single profile parts (parts which can be extruded).
Version 2 can also tool path STL files. Through the parameters.py module the user
can a large group of printing parameters. Most parameters can be adjusted for each
individual layer. The program contains some methods to make it easier to print
multiple parts.

## Dependencies
NumPy

## Getting Started
After downloading the zip file and extracting it in an appropriate location either
open the parameters.py file in your prefered Python IDE or with a text editor
(I prefer Notepad++)*. The user adjustable printing parameters are broken into
five section:<br/>
* Part<br/>
* Layer<br/>
* File<br/>
* Misc<br/>
* Printer<br/>

Parameters which are in Python lists [enclosed in square brackets] can very varied
between either parts or layers depending on which parameter set they are located.
For **_part parameters_** _the longest list determines_ **_how many_** _parts are printed_
all other parameters a cycled until the longest list is exhausted. For layer parameters
the parameters are cycled until the specified number of layers have been printed.

### Part Parameters
Part parameters are parameters that are constant throughout a single part but can
change between parts. Part parameters also 


## *Notepad++
If you have Python and the appropriate dependancies installed you can use
Notepad++ to edit the parameters.py files and then run the program with
Python. To do this in the menu bar select Run-> Run (F5) type the following:
<br/><br/>
`<your python path>\python.exe -i "$(FULL_CURRENT_PATH)"`
<br/><br/>
`<your python path>` is the actual path to python. For me Python was in my 
Anaconda3 folder. `FULL_CURRENT_PATH` is a variable in Notepad++ so type
that exactly. On my computer the full command was: <br/>
<br/>
`C:\Anaconda3\python.exe -i "$(FULL_CURRENT_PATH)"`
