# DogBone v2.1

DogBone is a program that creates custom tool paths for Fused Filament Fabrication
3D printers (also known by the trade marked term FDM). The motivation for creating
this program was to allow the user to independently adjust as many printing
parameters as possible for the purpose of researching and characterizing each
parameter's effect on a part's properties.

Version 2 can tool path both STL files and pre-defined shapes.
Executing RUN_ME.py with Python 3+ will display a GUI through which you can enter
all of the parameters for printing.

## Dependencies
[matplotlib](http://matplotlib.org/)<br/>
[NumPy](http://www.numpy.org/)<br/>
[trimesh](https://pypi.python.org/pypi/trimesh/1.14.9)<br/>
[Shapely](https://pypi.python.org/pypi/Shapely)<br/>


## Getting Started
After downloading the zip file and extracting it in an appropriate location and installing
the dependencies simply run RUN_ME.py in your preferred Python IDE or with a text editor
(I prefer Notepad++)*. The user adjustable printing parameters are broken into
five sections:<br/>
* [Part](#part-parameters)<br/>
* [Layer](#layer-parameters)<br/>
* [File](#file-parameters)<br/>
* [Print](#print-parameters)<br/>
* [Printer](#printer-parameters)<br/>

Parameters types are indicated after the name of the parameter. Types [enclosed in square brackets]
can be lists, comma or space separated. For **_part parameters_** _the
longest list determines_ **_how many_** _parts are printed_ all other
parameters are cycled, one for each part, until the longest list is exhausted. For layer parameters
the parameters are cycled layer by layer until the specified number of layers have been printed.

### Part Parameters
Part parameters are parameters that are constant throughout a single part but can
change between parts (except for outline). The longest list of part parameters
determines how many parts will be created. The part parameters are:<br/>
* outline<br/>
* stl_file<br/>
* solidity ratio<br/>
* print speed (mm/min)<br/>
* shift X<br/>
* shift Y<br/>
* number of layers<br/>
* brims<br/>

#### Outline
The outline of the part to be made. The drop down menu is populated by the functions
in the doneShapes module. An outline must be of type Shape. If an stl file is desired
select `stl_file` from the drop down.

#### Stl File
To slice an .stl file select `stl_file` from the **outline** drop down menu.
From there a file chooser window will pop up allowing you to select an .stl file.

#### Solidity Ratio
Solidity ratio is used to calculate the extrusion rate for each layer.<br/>
`extrusion_rate = solidity_ratio*layer_height*nozzle_diameter/filament_area`<br/>
A solidity ratio of 1 should create a fully filled part, a theoretical minimum
to have all beads in a square just touching is π/4.

#### Print Speed mm/min
Print speed is how fast the print head moves while printing. The units will be
dependent on the hardware you are using. It seems most slicing software uses
mm/sec but the RepRap G-code they create and send to the printer
is still defined in mm/min so that is the units used in the G-code.

#### Shift X and Shift Y
To print multiple parts without them attempting to occupy the same space you
must use **shiftX** and **shiftY**. These shifts are absolute shifts (they are not relative
to the previous shift). Since it does not make sense to have two parts printed in the
same location at least one of these two parameters should be the longest list of
part parameters and determine how many parts are printed.

#### Number of Layers
How many layers are printed in the part. They layer parameters are continuously
cycled until this number is reached for the part being printed. They are then reset
for the next part.  

#### Brims
The number of brims to place around the first layer. The brims will be printed
around the exterior side of every loop on the part including internal holes
at a distance of `pathWidth` between each brim. The brims are printed in order
farthest from part to closest to part.

### Pattern and Design Type (Not yet implemented in V2)
Custom infill patterns can be designed for the part. The pattern must be of
type LineGroup. The pattern is extended by copying the design and then
connecting the start of the first line in the copy the end of the last of
the original and saving that as the new original. This process is repeated
until the design is sufficiently longer than the outline. This whole new
line group is then copied and translated in Y by `pathWidth` until a full
field is created. Please read the comments in the
[InFill](https://github.com/VanHulleOne/DogBoneV2/blob/master/InFill.py)
module for more details.

### Layer Parameters
Layer parameters are unique to each layer of a part. Each list of parameters is
cycled until the value in **numLayers** for the part is met. The lists are then started
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
with the angles moving around counter clockwise.

#### Path Width mm
The distance between the centerlines of two adjacent passes. This is an orthogonal
distance, not a normal distance. If you had a zig-zag infill pattern
v^v^v^v when that pattern is turned into a field it would only be shifted
in the Y direction by **pathwidth**. If the angle were 90 degrees that would mean
a path width of 1.0mm would create a normal distance of 0.707mm which will
then effect your solidity ratio.

#### Infill Shift X and Y mm
Sometimes when the infill is created it is not centered properly in the shape
or you may want to do testing that creates beads which sit in the valley of the lower
bead instead of directly on top of it<br/>
O O O O O<br/>
O O O O O<br/>
O O O O O<br/>
**vs**<br/>
O O O O O<br/>
. O O O O<br/>
O O O O O<br/>
Infill shift X and Y are hacks used so you can adjust the infill to fine tune
your pattern.

#### Number of Shells
The number of shells you want around the part. Shells are created by a
normal offset `pathWidth` away from the previous shell/outline. Keep in mind that
to tool path the infill properly a trim shell is created by the program. For example
if three shells are prescribed a fourth trim shell is created inside the third 
shell to properly trim the infill.

### File Parameters
* outputFileName - The name of the output Gcode file
* start_Gcode_FileName - Name of the file which contains all of the starting
Gcode commands
* end_Gcode_FileName - File with end Gcode commands
The program currently looks into the Start_End_Gcode folder when searching for
these files.

### Print Parameters
* bed_temp (C) - flag = `#BED_TEMP`
* extruder_temp (C) - flag = `#EXTRUDER_TEMP`

To have the GUI set the bed and extruder temperatures you must provide the
appropriate flags in the Start Gcode file. For the Taz5 or other printers using the
Marlin firmware it would look as follows:

```
M109 #EXTRUDER_TEMP ; 
M190 #BED_TEMP ;
```


### Printer Parameters
These are parameters related to the printer itself.

* filamentDiameter (mm)- The diameter of the incoming filament.
* nozzleDiameter (mm) - Nozzle outlet diameter
* RAPID (mm/min) - How fast the printer should move when not printing<br/>
  * The [RepRap wiki (9 July 2016)](http://reprap.org/wiki/G-code#G0_.26_G1:_Move)
says "The RepRap firmware spec treats G0 and G1 as the same command,
since it's just as efficient as not doing so." I strongly disagree with this statement.
A G01 is a feed command and as such needs an F value to know how fast to move.
A G00 command should be a rapid command where the printer knows its max velocity
and therefore does not require an F feed rate. Because of the RepRap design choice G00
needs a feed rate command requiring the programmer/operator to know each
individual machine's max speed and creates larger programs by needing the
additional text on every G00 line. How is that just as efficient?
* TRAVERSE_RETRACT (mm) - how far to retract the filament to prevent nozzle
drool when traversing around the part.
* MAX\_FEED\_TRAVERSE (mm) - if the move to the next printing position is less than
this value the head is not lifted up, no filament retract is performed, and it is moved
at the print velocity. If the move to the next printing position is larger than
this value the head is lifted by **Z_CLEARANCE** and the material is retracted
by **TRAVERSE_RETRACT**
* Z_CLEARANCE (mm) - Relative clearance height to which the head is moved when
traversing the part.
* APPROACH_FR (mm/min) - Speed the printer should move when approaching the part.
A slightly slower speed helps prevent hard crashes and allows the filament more
time to move forward in the nozzle in preparation for printing.

## *Notepad++
If you have Python and the appropriate dependencies installed you can use
Notepad++ to run the RUN_ME.py file.
To do this in the menu bar select Run-> Run (F5) type the following:
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
