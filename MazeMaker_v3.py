import os
import sys
import cv2
import random
from skimage.measure import compare_ssim
from datetime import datetime
from tomorrow import threads
from PIL import Image
import numpy as np
from pseyepy import Camera

from OpenGL.GL import *
from OpenGL.GLUT import *
from OpenGL.GLU import *

from Mask import Mask
from MaskedGrid import MaskedGrid
from RecursiveBacktracker import RecursiveBacktracker


class MazeMaker():
    """docstring for MazeMaker"""
    def __init__(self):
        self.start = datetime.now()
        self.cap = Camera([0], fps=30, resolution=Camera.RES_LARGE, colour=False)
        self.mz = []
        self.l_bg = None
        self.width = 1280
        self.height = 720
        self.l_average = 0


    def draw_maze(self):
        # set the color of the line
        glColor3f(0.3, 0.3, 0.5)
        # set the line width for drawing
        glLineWidth(2)
        # begin shape with pairs of lines
        glBegin(GL_LINES)
        # the list of points is backwards so reverse it
        self.mz.reverse()
        # loop over coordinates adding all the vertices
        for loc in self.mz:
            x1, y1, x2, y2 = loc    
            # @ 0.1  = *5
            # @ 0.25 = *2 
            # @ 0.15 = *3.333
            glVertex2f(x1*3.333, y1*3.333)            
            glVertex2f(x2*3.333, y2*3.333)  
        # complete the shape and draw everything 
        glEnd() 


    def refresh_scene(self):
        glViewport(0, 0, self.width, self.height)
        glMatrixMode(GL_PROJECTION)
        glLoadIdentity()
        glOrtho(0.0, self.width, 0.0, self.height, 0.0, 1.0)
        glMatrixMode (GL_MODELVIEW)
        glLoadIdentity()


    def update(self):
        # get the frame
        frame, timestamp = self.cap.read()
        # crop to correct ratio
        frame = frame[100:460, 0:640]
        # resize smaller for faster processing
        small = cv2.resize(frame, (0, 0), fx=0.15, fy=0.15)
        # threshold the image
        # otsu threshold is adaptive
        #   so will adjust to the range present in the image
        ret, thr = cv2.threshold(small, 1, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)
        # opening and dilating to remove noise
        # kernel size is size of operation 
        kernel = np.ones((1, 1), np.uint8)
        opening = cv2.morphologyEx(thr, cv2.MORPH_OPEN, kernel, iterations=1)
        bg = cv2.dilate(opening, kernel, iterations=2)
        # if not first frame
        if self.l_bg is not None:
            # calculate the average of the current bg
            average = np.average(bg)
            # compare to the last stored average
            diff = average - self.l_average
            # if there is a big enough difference +/-
            if diff > 0.8 or diff < -0.8:
                # translate numpy array to PIL image
                pil_im = Image.fromarray(bg)
                # make a mask from the image
                mask = Mask.from_img_data(pil_im)
                # build a grid from the unmasked areas
                grid = MaskedGrid(mask)
                # build walls in the grid
                RecursiveBacktracker.on(grid)
                # get walls as list of coordinate pairs for drawing
                self.mz = grid.to_point_pairs(cell_size=4)
            # save the new average
            self.l_average = average
        # save the background
        self.l_bg = bg


    def draw(self):      
        glClearColor(1, 1, 1, 1)
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
        glLoadIdentity()
        self.refresh_scene()
        self.update()
        self.draw_maze()  
        glutSwapBuffers()  


    def main(self):
        glutInit()
        glutInitDisplayMode(GLUT_RGBA | GLUT_DOUBLE | GLUT_ALPHA | GLUT_DEPTH)
        glutInitWindowSize(self.width, self.height)
        glutInitWindowPosition(0, 0)
        glutSetCursor(GLUT_CURSOR_NONE)
        window = glutCreateWindow("MazeMaker")
        glutDisplayFunc(self.draw)
        glutIdleFunc(self.draw)
        glutMainLoop()


mazemaker = MazeMaker()
mazemaker.main()

