## ISAAC CLARKE - LABYRINTH MAKER 
### MA COMPUTATIONAL ART
### 2018

### CONTENTS
1. Requirements
1. References
1. Libraries
1. Main Files
1. Additional Files

**************************************************

## 1 - REQUIREMENTS
* Python3 (tested on 3.5.4)
* KINECT v1 MODEL 1414
* An external monitor (attemps to run on disply 2, will die if not there)
libfreenect, numpy, pseyepy, OpenGl, OpenCV, GLFW, Pillow

## 2 - REFERENCES
* BUCK, J. (2015) MAZES FOR PROGRAMMERS. Pragmatic Bookshelf
* Cannon, M. (2011) Carcanet Press. London.
* Borges, J.L. (1962) Labyrinths. New Directions.
* Joyce, J (1914) The Dead. Grant Richards Ltd.

## 3 - LIBRARIES
* NumPy (2006). http://www.numpy.org/
* OpenCV (2000) The OpenCV Library. https://opencv.org/
* libfreenect (2010) OpenKinect. https://github.com/OpenKinect/libfreenect
* Graphics Library Framework GLFW (2006). glfw.org
* OpenGL (2006) Khronos Group. https://www.opengl.org/
* pseyepy (2017) bensondaled. https://github.com/bensondaled/pseyepy
* Python Imaging Library (2009) Secret Labs AB. http://www.pythonware.com/products/pil/


**************************************************

## 4 - MAIN FILES

### LabyrinthMakerGLFW_Kinect.py
This is the main file for the installation. It connects to the kinect and external monitor, and processes the image feed through opencv then the labyrinth generator, and finally draws it in opengl. 

### Grid.py
### Cell.py
### Mask.py
### MaskedGrid.py
These are the Classes which process an image and turn it into a labyrinth. These are translated into python from Jamis Buck's Ruby examples in Mazes For Programmers (2015). Alongside the porting to python I have also added a few functions which allow me to get a list of points so I can draw in opengl rather than drawing to file as show in the examples. I also add a key addition to the Grid Class so that I can generate Unicursal Mazes (Labyrinths with one continous path with no dead ends or loops) which is entirely my own solution.

### frame_convert2.py
This is a libfreenect provided file needed for translating the kinect images into the correct formats for use with numpy etc.

### RecursiveBacktracker.py
### Sidewinder.py
These are algorithms for joining cells in a grid to create mazes. Again adapted into python from Buck's Mazes for programmers. 
I have provided two examples, the sidewinder algorithm is incompatible as it does not create orthogonal/perfect mazes (there are loops) so they cannot be converted into the single path labyrinth that I wanted. The recursive backtracker does create orthoganal mazes so I am using this in as the base algorithm to build upon.


## 5 - ADDITIONAL FILES

### LabyrinthMarkerVideoIn.py
This is similar to the main file at the top of the list. But instead of a kinect this takes a video input and records to a video output. So you can use it as a video proceesing effect, where every frame is a labyrinth!

### saveTestImages.py
This is a program I wrote to quickly catch still images from the kinect rgb/ir cameras in order to calibrate them.

### calibrate.py
This is an adaptation of an opencv example to get the Camera Matrix and Distortion coefficients used in the main program to correct the images and remove lens distortion. 

### stitch.py
### split.py
### sender.py
### OneTile.py
These are examples of my earlier work creating large scale high resolution still images. You can provide an image and get either a single image or a tiled image in return.

### StillLabyrinthMakerPSEYE.py
Similar ot the above, but this creates single large images from a camera feed. For use with the PS Eye camera.

### screencap.txt
bash cron job to catch screenshots.

### runforever.py
This runs the main script and reboots it if it closes.

