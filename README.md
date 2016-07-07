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
open the parameters.py file in your preferred Python IDE or with a text editor
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
change between parts (except for outline). The longest list of part parameters
determines how many parts will be created. The part parameters are:<br/>
* outline<br/>
* solidity ratio<br/>
* print speed (mm/min)<br/>
* shift X<br/>
* shift Y<br/>
* number of layers<br/>

#### Outline
The outline of the part to be made. An outline must be of type Shape. The doneShapes
module contains several methods which return pre-defined shapes. Only one outline
is allowed.

#### Solidity Ratio
Solidity ratio is used to calculate the extrusion rate for each layer.<br/>
`extrusion_rate = solidity_ratio*layer_height*padth_width/filament_area`<br/>

#### Print Speed mm/min
Print speed is how fast in millimeters per minute the print head moves while printing.
It seems most slicing software uses mm/sec but the G-code it send to the printer
is still defined in mm/min so that is the default I have chosen.

#### Shift X and Shift Y
To print multiple parts without them attempting to occupy the same space you
must use Shift X and Shift Y. These shifts are absolute shifts (they are not relative
to the previous shift). Since it does not make sense to have two parts printed in the
same location at least one of these two parameters should be the longest list of
part parameters and determine how many parts are printed.

#### Number of Layers
How many layers are printed in the part. They layer parameters are continuously
cycled until this number is reached for the part being printed. They are then reset
for the next part.

### Layer Parameters
Layer parameters are unique to each layer of a part. Each list of parameters is
cycled until the Number of Layers for the part is met. The lists are then started
over at the start of the next part. The layer parameters are:<br/>
* Infill Angle (degrees)<br/>
* Path Width (mm)<br/>
* Layer Height (mm)<br/>
* Infill Shift X (mm)<br/>
* Infill Shift Y (mm)<br/>
* Number of Shells <br/>
* Trim Adjust (mm)<br/>

#### Infill Angle degrees
The angle of the infill for the part. Zero (0) degrees is in the positive X direction
with the angles moving around in the counter clockwise direction.

#### Path Width mm
The distance between the centerlines of two adjacent passes. Re


## *Notepad++
If you have Python and the appropriate dependencies installed you can use
Notepad++ to edit the parameters.py files and then run the program with
Python. To do this in the menu bar select Run-> Run (F5) type the following:
<br/><br/>
`<your python path>\python.exe -i "$(FULL_CURRENT_PATH)"`
<br/><br/>
`<your python path>` is the actual path to python. For me Python was in my 
Anaconda3 folder. `FULL_CURRENT_PATH` is a variable in Notepad++ so type
that exactly. On my computer the full command was: <br/>
<br/>
`C:\Anaconda3\python.exe -i "$(FULL_CURRENT_PATH)"`<br/><br/>
Now select save. For a command I chose ctrl-r and hit ok. Now you can edit
the parameters.py file, **save the changes** (if you do not save the changes
then it will run the old changes, which can be confusing) and finally hit your
hot keys (ctrl-r). Notepad++ will call Python and run your program.
