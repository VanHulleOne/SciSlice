# DogBone v1.2

DogBone is a program that creates custom tool paths for Fused Filament Fabrication
3D printers (also known by the trade marked term FDM). The motivation for creating
this program was to allow the user to independently adjust as many printing
parameters as possible for the purpose of researching and characterizing each
parameter's effect on a part's properties.

Version 1 can only produce single profile parts (parts which can be extruded).
Version 2 can also tool path STL files. Through the parameters.py module the user
can a large group of printing parameters. Most parameters can be adjusted for each
individual layer. The program contains some methods to make it easier to print multiple parts.