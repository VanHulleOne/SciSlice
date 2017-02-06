# SciSlice - The Scientific Slicer

SciSlice is a program that creates custom tool paths for Fused Filament Fabrication
3D printers (also known by the trade marked term FDM). The motivation for creating
this program was to allow the user to independently adjust as many printing
parameters as possible for the purpose of researching and characterizing each
parameter's effect on a part's properties. These printing parameters can be changed
between layers and even within sub-regions of a layer.

SciSlice can tool path both STL files and pre-defined shapes.
Executing RUN_ME.py with Python 3+ will display a GUI through which you can enter
all of the parameters for printing.

## Dependencies
[matplotlib](http://matplotlib.org/)<br/>
[NumPy](http://www.numpy.org/)<br/>
[trimesh](https://pypi.python.org/pypi/trimesh/1.14.9)<br/>
[Shapely](https://pypi.python.org/pypi/Shapely)<br/>
[Pygame](https://pypi.python.org/pypi/Pygame/1.9.2b8)  
[Rtree](https://pypi.python.org/pypi/Rtree/0.8.2)  


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

## Easy Getting Started Instructions  
If you have no idea how to get started using SciSlice hopefully these instructions will help. If you kind of know what you are doing then use this as an outline to really mess it all up.  

### Installation  
You will need Python 3.5+ and all of the required dependencies to run SciSlice.py. Downloading and
installing Anaconda will get you Python and most of the needed libraries (dependencies). Anaconda can be
found on the [Continuum](https://www.continuum.io/downloads) website. Choose the Python 3.5 version
installer appropriate for your operating system. This is a pretty large installation so it will take a bit.

### Dependencies
Even though Anaconda comes with many libraries already installed I managed to design SciSlice to need three libraries which are not included. Sorry about that. Luckily Anaconda comes with a program called Conda which makes this processes fairly easy. First you need to get to the Anaconda prompt. On my Windows machine I went to the Start Menu -> All Programs -> Anaconda3 -> Anaconda Prompt. Selecting Anaconda Prompt will pop up a black command line
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

### .json
You can save your print parameters by clicking the Save button on top of the GUI. Previously
saved .json files can be uploaded with the Upload button. When the program is first opened it uses the DEFAULT.json
file. If you always use a similar parameter profile you can save over this file and your parameters will be
loaded at startup.


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
