## ODLC Generation Script ##
This script can create a set amount of randomized ODLC shape objects or a comprehensive list of all possible ODLC shape objects.

**main.py**
* This file is where users can use desired function.

**ODLCcharacteristics.py**
* This file contains lists of all possible shapes, colors, and character symbols that can be used to form an ODLC shape object.

**ODLCgenerationFuncs.py**
* This file contains generation functions for all the different shapes and for the randomized generation function and comprehensive generation function.



**IMPORTANT NOTES**
* Once the generation functions are called, the generated images will be created in a new directory named "random-generated-ODLCs-day-month-year-hours-minutes-seconds"
* Every image file (png format) is named "shapeColor-shape-charColor-char.png"