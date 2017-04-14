# SciSlice - The Scientific Slicer

SciSlice is a program that creates custom tool paths for Fused Filament Fabrication
3D printers (also known as FDM&trade;). The motivation for creating
this program was to allow the user to independently adjust as many printing
parameters as possible for the purpose of researching and characterizing each
parameter's effect on a part's properties. These printing parameters can be changed
between layers and even within sub-regions of a layer. The program cannot create
support structure. 

SciSlice can tool path both STL files and pre-defined shapes.
Executing RUN_ME.py with Python 3+ will display a GUI through which you can enter
all of the parameters for printing.

## What it Does Well
SciSlice is best at using its predefined outlines and varying many printing parameters.
It tool paths these part in a reasonable amount of time and, through caching, can make
multiple parts per print with little additional computation. If you want to print five
tensile specimens in one print, possibly all the same, possibly all different, this is
the program for you. SciSlice does this quickly with an easy method for adjusting parameters
and saving those parameters for later use and reference.  

SciSlice is reasonably good at slicing simple STL files, especially if you want to
treat the STL as an extrusion and just extract a single "loop" from the STL and use
that as the outline for your part. With a little extra effort creating a separate parameters
JSON file it will also do multiple STL files at once, each with different layer parameters.

If you want to slice a whole STL, you will find SciSlice to be a little slow. It also
has difficulty handling more complex STLs, especially with thin features. Its weakness in
this area is mostly from using Shapely to create offsets (shells). I would be interested
in learning of other libraries which could handle offsets in a faster and more robust
fashon. SciSlice cannot create support structure.

If you want to create your own predefined outlines please look at the doneshapes.py
module for examples. linegroup.py contains several helper methods to make creating outlines
relatively easy with only a little Python programming experience.

## Easy Getting Started Instructions  
If you have no idea how to get started using SciSlice hopefully these instructions will help. If you kind of know what you are doing then use this as an outline to really mess it all up.  

> **Note:** I would really like to get SciSlice onto Anaconda so it can be installed, with all
its dependencies, simply using:  
`conda install -c vanhulleone SciSlice`  
However, after many attempts
I can't seem to figure out how to get the directory structure correct. If anyone knows how to do this I
would appreciate assistance. It will make installation and updating much easier for the users. Thanks.

### Installation  
You will need Python 3.5+ and all of the required dependencies to run SciSlice. Downloading and
installing Anaconda will get you Python and most of the needed libraries (dependencies). Anaconda can be
found on the [Continuum](https://www.continuum.io/downloads) website. Choose the Python 3.5 version
installer appropriate for your operating system. This is a pretty large installation so it will take a bit.

### Dependencies
[matplotlib](http://matplotlib.org/)<br/>
[NumPy](http://www.numpy.org/)<br/>
[trimesh](https://pypi.python.org/pypi/trimesh/1.14.9)<br/>
[Shapely](https://pypi.python.org/pypi/Shapely)<br/>
[Pygame](https://pypi.python.org/pypi/Pygame/1.9.2b8)  
[Rtree](https://pypi.python.org/pypi/Rtree/0.8.2) 

Even though Anaconda comes with many libraries already installed I managed to design SciSlice to need several libraries which are not included. Sorry about that. Luckily Anaconda comes with a program called Conda which makes this processes fairly easy. First you need to get to the Anaconda prompt. On my Windows machine I went to the Start Menu -> All Programs -> Anaconda3 -> Anaconda Prompt. Selecting Anaconda Prompt will pop up a black command line
window. From this window you will be able to install the additional libraries: Pygame, Shapely, Rtree, and trimesh.
In the command prompt type:  
`conda install -c cogsci pygame`  
This will install Pygame from the CogSci profile on anaconda.org.  
Next install Shapely with the same process but from the IOOS channel.  
`conda install -c IOOS shapely`   
Third, install Rtree also from the IOOS channel.  
`conda install -c IOOS rtree`   
Finally we need trimesh. As of this writing there was not a Conda version of trimesh so we will use pip.  
`pip install trimesh`  

All in a row you will have typed into the command prompt (hitting enter after each line and waiting for each install):
```
conda install -c cogsci pygame  
conda install -c ioos shapely  
conda install -c ioos rtree    
pip install trimesh  
```

Now you have the additional libraries needed to run SciSlice.

### Installing SciSlice  
The most up-to-date version of SciSlice is located on GitHub in its
[repository](https://github.com/VanHulleOne/SciSlice). Once there select the clone/download dropdown (a green button) and download the .zip file. Extract the file into whichever folder you like and you have it installed.  

Since SciSlice is not fully stable yet it may be worth while to download [Git Desktop](https://desktop.github.com/) so you can clone the repository to more easily and quickly download bug fixes.

### Running the Program
To run the program either cd into the folder in which you unzipped the program and then type in the
Conda prompt `python RUN_ME.py` or open Spyder, which came with the Anaconda installation, open the RUN_ME.py
and run the program from Spyder. 


## Getting Started
After downloading the zip file and extracting it in an appropriate location and installing
the dependencies simply run RUN_ME.py in your preferred Python IDE or from the command line. A GUI
interface will be displayed which allows for either entering new parameters or for uploading previously
defined parameter files (JSON files).  The user adjustable printing parameters are broken into
five sections:<br/>
* [Part](#part-parameters)<br/>
* [Layer](#layer-parameters)<br/>
* [File](#file-parameters)<br/>
* [Print](#print-parameters)<br/>
* [Printer](#printer-parameters)<br/>

Parameters types are indicated after the name of the parameter. Types [enclosed in square brackets]
can be lists, comma or space separated. For **_part parameters_** _the
longest list determines_ **_how many_** _parts are printed_ all other
parameters are repeated, one for each part, until the longest list is exhausted. For layer parameters
the parameters are cycled layer by layer until the specified number of layers have been printed.

The sorting of parameters displayed below into the categories: part, layer, print, printer; are the
current division as downloaded. Most parameters can be switched into any other group by altering the parameters
list in RUN_ME.py. See the advanced user section for more details.

To know which parameters are in which group simply select the group from the right hand side buttons.

### Part Parameters
Part parameters are parameters that are constant throughout a single part but can
change between parts (except for outline). The longest list of part parameters
determines how many parts will be created. The part parameters are:<br/>
* Outline<br/>
* Pattern<br/>
* Extrusion factor<br/>
* Print Speed (mm/min*)<br/>
* Shift X<br/>
* Shift Y<br/>
* Shift Z<br/>
* Number of Layers<br/>
* Design Type (not implemented)<br/>
* Brims<br/>
* Horizontal Expansion<br/>
* randomStartLoc  

#### Outline
The outline of the part to be made. The drop down menu is populated by the properly decorated
functions in the doneshapes.py module. See [doneshapes](#doneshapes) for more information on
the outline dropdown options.

#### Pattern
This is the infill pattern which will be used to fill your part. If you choose `noInfill` remember
to select at least one shell.

#### Extrusion Factor
Extrusion factor is used to calculate the extrusion rate for each layer.<br/>
`extrusion_rate = extrusionFactor*layer_height*nozzle_diameter/filament_area`<br/>
Use this to determine how full of a bead area you want or to compensate for under/over filling
cause by inaccurate feeding speeds (which should be fixed in your firmware) or
manufacturing tolerances in your filament.

#### Print Speed (mm/min*)
Print speed is how fast the print head moves while printing. 

*The output is actually unit agnostic and will depend on how your firmware interrupts
its feed rate commands. It seems most slicing software uses
mm/sec at the GUI but the RepRap G-code they create and send to the printer
is still defined in mm/min. So instead of asking you for units of mm/sec and then
dividing by 60 behind the scenes SciSlice just asks for a number and writes it.
Who chose to not ask for feed rate in the native machine units anyway?

#### Shift X, Shift Y
To print multiple parts without them attempting to occupy the same space you
must use **shiftX** and **shiftY**. These shifts are absolute shifts (they are not relative
to the previous shift). Since it does not make sense to have two parts printed in the
same location at least one of these two parameters should be the longest list of
part parameters and determine how many parts are printed.

#### Shift Z
Adjust parts in the Z direction. Mostly used for pragmatically accounting for an improperly
leveled/zeroed bed.

#### Number of Layers
How many layers are printed in the part. The layer parameters are continuously
cycled until this number is reached for the part being printed. They are then reset
for the next part. For Outlines which come from an STL, if you want to print all
of their layers then you must enter the flag **-1** into `numLayers`. If you enter
any number larger than zero for an STL then that number of layers will be printed.

In the future I would like to implement slices in `numLayer` so you could easily print
sub-slices of an STL. 

#### Brims
The number of brims to place around the first layer. The brims will be printed
around the exterior side of every loop on the part including internal holes
at a distance of `nozzleDiameter` between each brim. The brims are printed in order
farthest from part to closest to part.

#### Design Type (Not yet implemented, just leave it at 0)
Custom infill patterns can be designed for your part. The pattern must be of
type LineGroup. The pattern is extended by copying the design and then
connecting the start of the first line in the copy the end of the last of
the original and saving that as the new original. This process is repeated
until the design is sufficiently longer than the outline. This whole new
line group is then copied and translated in Y by `pathWidth` until a full
field is created. Please read the comments in the
[InFill](https://github.com/VanHulleOne/DogBoneV2/blob/master/InFill.py)
module for more details.

#### Horizontal Expansion
If your prints are coming out incorrectly sized in the XY plane then you can use this value
to adjust them. A positive value will offset the outer `outline` by that value making it larger
(and holes smaller). A negative value will decrease the size of the part (and increase hole sizes).

#### Random Start Location  
`randomStartLocation` allows the layers to be started at pseudo-random locations instead
of always the minimum X and Y locations. If `randomStartLocation` is set to 0 then each layer
will always start at the point in the toolpath closest to the point (minX, minY). Any other integer value will
be used as the seed for the random number generation. Since this value is the seed, identical
prints which are tool pathed at different times will still produce the same "random" starting
locations. The point is chosen by finding the LineGroup with the left most point, the minX,
and then choosing a random point from that LineGroup. For single region shapes with at least one
shell this will ensure that the random point is on the outer most shell, although it could start
at the outer most shell of a hole. For shapes without a shell this will pick a random location
from the infill. For multi-region parts this technique will cause the tool path to only start
somewhere on the left most region and nowhere else. Hopefully this will be fixed. 

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
* Infill Overlap (mm)<br/>

#### Infill Angle degrees
The angle of the infill for the part. Zero (0) degrees is in the positive X direction
with the positive angles moving around counter clockwise.

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

#### Infill Overlap mm
How much the infill should overlap with the inner most shell. To create the infill a `trimshape`
must first be created offset inside the inner most shell by a distance of `nozzleDiameter`,
or in the case of no shells offset from the defined outline. This shape is then used to trim the
infill throwing away any new lines which do not lie inside the `trimshape`. If the infill is not bonding well
to the shell `infillOverlap` can be increased making a `trimshape` which is closer to the inner most shell allowing
the infill and shell to squish together more completely. If there is overfilling with the shell this value can be
decreased. Due to computational uncertainties between lines in the `trimShape` and lines in the infill which are
co-linear overlapping it is best to not set this value directly at zero. A value of 0.0002 has
been found to produce the best results; including lines which we want to be included without
over filling the shell-infill boundary.

### File Parameters
* start_Gcode_FileName - Name of the file which contains all of the starting
Gcode commands
* end_Gcode_FileName - File with end Gcode commands
The program currently looks into the Start_End_Gcode folder when searching for
these files.

### Print Parameters
* bed_temp (C) - flag = `#BED_TEMP`
* extruder_temp (C) - flag = `#EXTRUDER_TEMP`

The start G-code file must be properly formatted in order to allow the bed and extruder temperatures
to be set in the output machine code file. The constants.py module defines the two flags which must
be used in the start file. They are `#BED_TEMP` and `#EXTRUDER_TEMP` placing these flags after
the appropriate machine code will allow SciSlice to write the values into the output machine code file.
For standard RepRap G-code the temperature section will look as follows:

```
M109 #EXTRUDER_TEMP ;
M190 #BED_TEMP ;
```


### Printer Parameters
These are parameters related to the printer itself.

* nozzleDiameter (mm) - Nozzle outlet diameter
* filamentDiameter (mm)- The diameter of the incoming filament.
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
* retractDistance (mm) - how far to retract the filament to prevent nozzle
drool when traversing around the part.
* retractMinTravel - if the move to the next printing position is less than
this value the head is not lifted up, no filament retract is performed, and it is moved
at the print velocity. If the move to the next printing position is larger than
this value the head is lifted by `ZHopHeight` and the material is retracted
by `retractDistance`
* ZHopeHeight (mm) - Distance up the head is moved when traversing the part.
* APPROACH_FR (mm/min) - Speed the printer should move when approaching the part.
A slightly slower speed helps prevent hard crashes and allows the filament more
time to move forward in the nozzle in preparation for printing.
* comment - Every system seems to require a different comment character. Enter the required comment
character here.

### Parameter Files
All of the parameters are saved in a JSON file. When the program is first loaded the parameters from
the DEFAULT.json file in the JSON sub-directory are loaded into the GUI. After you have changed the parameters
to your desired values you can save them by hitting the `Save` button at the top of the gui. A file navigation
window should pop up. If you have saved parameters and wish to use them again select the `Upload` button
and chose your desired parameter file. If you always use a similar parameter profile you can save over
the DEFAULT.json file and your parameters will be loaded at startup. However, if you are using a git client
to pull new changes you will have to make sure your default parameters are not changed during the next pull
and merge.

### Create 3D model
The `Create 3D Model` button calculates the tool paths for your current parameters and generates
a window showing you the printed tool path. Instructions are included on the window for how to navigate
through the window and how to change which layers you are viewing. At this time the line thickness does not
represent the actual thickness of the printed tool path. Also, there is a known issue when rotating the part
more than 180 degrees. You don't actually see the bottom of the part but instead it is flipped and you see the
top again. You are more then welcome to provide a patch which fixes either of the problems (or anything else
for that matter)

### Generate Code
When the `Generate Code` button is selected a file chooser pop-up window is created. After the output file
has been chosen the tool path is first calculated if needed* and then is converted into the desired machine
language. Currently the default choices are Gcode or RobotCode. Gcode is RepRap G-code in the Marlin flavor and specifically set up for a Taz5 printer. RobotCode is in ABB's RAPID language and is currently being used
for UW-Madison PEC's IRB120 robot for full 5-axis 3D printing research.

\* "_if needed_": When either `Create 3D model` or `Generate Code` are selected the program creates a temporary 
machine code file. If `Generate Code` is selected again and the parameters have not changed, this temporary
file is copied to the desired location and name instead of re-calculating the tool path and machine code.
This saves a lot of time on larger parts. However, the current parameter checking only checks the parameters
from the gui, not any additional parameters from a multi-region file. To curcumvent this problem you can either comment out the section of code responsible for the parameter checking. This code is in RUN_ME.py
module inside the convert() method and is marked which a comment. (currently around line 720) or make a small
change to one parameter in the GUI such as a sub-micro change to `infillOverlap`. I hope to enable
adding the multi-region parameters to the main parameter JSON file preventing this problem.

### Doneshapes
The doneshapes.py module contains all of the functions which generate the drop-down lists for
outline and pattern. Outlines are marked with an `@outline` decorator and patterns are marked with
an `@infill` decorator. Type hints are used in the functions to help the user know what information
should be entered into the text field. File name parameters named `fname` will have a file chooser
pop-up button created.
#### Outline default options
* fromSTL  
* fromSTL_oneLevel  
* multiRegion
* multiRegion_oneLevel
* regularDogBone
* wideDogBone
* circle
* rectangle
* polygon

##### fromSTL and multiRegion
Take in and tool path entire .STL files. They enable choosing a file (the STL for fromSTL and the 
parameter file for multiRegion).
The `change_units_from` parameter allows you to say in what
units your STL(s) are in so they can be converted to millimeters. This conversion is done by Trimesh.
The most common units are m, mm, and in. With a wide range of [units allowed](https://github.com/mikedh/trimesh/blob/master/trimesh/units.py). For both of these options `numLayers` is usually set to the flag -1.  
Since SciSlice cannot create support structure the STL files are often extrusions.
To make slicing faster and more repeatable both fromSTL and multiRegion have a `_oneLevel` counterpart that allows
the user to specify a `sliceHeight`. A single outline will be created from the slice at that height which will be used to create the entire part. You are required to set `numLayers` if this option is used.

##### regularDogBone
An ASTM D-638 type 1 tensile specimen. 

##### wideDogBone
Same general shape as the ASTM D638 but allows you to specify a gage width, either wider or more narrow.

### Multi Region
Both multiRegion options allow the user to use multiple STL files in a single print and provide
different parameters for each region. This is especially useful when a user wants to control the layer
orientation in specific regions to ensure beads align with tensile forces.  
To use multiRegion you must create an additional JSON file and place it in the same directory
as the STL files it references. The file must contain a list of
dictionaries, each dictionary containing the file name of the STL which should be used and the
parameters for that file. Any parameter from the GUI can be specified in the JSON without
receiving an error however not all of the parameters will actually work for each region. Currently
only the parameters used by the `make_region()` function in figura.py plus `layerHeight` (used by
the `Region` class in doneshapes.py) will actually affect each region.
An example JSON is given below:
```
[{"fileName": "C-Bracket_0_90.stl",
"numShells": [0,1],
"pathWidth": [0.5, 1.0],
"infillAngleDegrees": [0, 90.0],
"infillShiftX": [0.0],
"infillShiftY": [0.0],
"layerHeight": [0.1,0.2]},
{"fileName": "C-Bracket_minus45.stl",
"numShells": [0],
"pathWidth": [0.5],
"infillAngleDegrees": [-45,0],
"infillShiftX": [0.0],
"infillShiftY": [0.0],
"infillOverlap": [0.0002]},
{"fileName": "C-Bracket_plus45.STL",
"numShells": [0],
"infillAngleDegrees": [45],
"infillShiftX": [2,7],
"infillShiftY": [0.0],
"infillOverlap": [0.0002]}]
```
The JSON format is a little particular so remember to not have any trailing commas. The parameter
names can be in any order and each region does not need to specify the same parameters. Any parameter
not listed will default to the parameter in the GUI. After each region has been made they will all be toolpathed together as a layer.
To help prevent typos I like to save a parameters JSON and then copy the needed dictionary entries into
my multiRegion file.

### Changing Parameter Groups
SciSlice enables a user to decide which parameters are for parts and which are for layers. If multiple
parts are being printed and you want to change the layer height between parts but have it be constant within
a part, you would have to change `layerHeight` into the `PART` group.  
  
Inside the RUN\_ME.py module in the Page_Variables class there is a list named `parameters`.
`parameters` is a list of namedtuples, one for almost every parameter in the GUI.
(The two dropdowns are in the `dropdowns` list, the radio buttons are handled elsewhere.)
The first vlue in the namedtuple is the parameter name, next is what type of variable
it accepts, declared from the constants provided above. All Layer and Part parameters must be lists so they
can be properly handles by the `zipVariables_gen()` generator in parameters.py. The final field is a
tuple containing the variable groups constants. If the tuple contains `PART` then the variable will
be used as a part parameter. If it contains `LAYER` then it iwll be a layer parameter. If both `LAYER`
and `PART` appear in the tuple, no error is thrown, the variable will appear under both buttons
but `LAYER` will win for the actual tool path creation. Please note that in Python parentheses
are used for tuples but if only one item is in the parentheses a tuple will not be created. It
instead must have a trailing comma. `(42)` means simply fourty two. `(42,)` is a tuple of length one
containing the number fourty two. Through this technique you can also change which parameters are
in the `COMMON` group.

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
Now select save. For a command I chose ctrl-r and hit ok. Now you can hit your
hot keys (ctrl-r) and Notepad++ will call Python and run your program.
