import os
import sys
import cv2
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


def draw_mz(mz):
    # print("draw mz")
    glLineWidth(2)
    glBegin(GL_LINES)
    for loc in mz:  
        x1, y1, x2, y2 = loc                 
        glVertex2f(x1*3, y1*3)            
        glVertex2f(x2*3, y2*3)                   
    glEnd() 


def find_mz(): 
    global mz
    global cap
    # print("find mz")
    frame, timestamp = cap.read()
    # crop to correct ratio
    frame = frame[100:320, 100:540]
    small = cv2.resize(frame, (0, 0), fx=0.25, fy=0.25)
    ret, thr = cv2.threshold(small, 1, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)
    kernel = np.ones((1, 1), np.uint8)
    opening = cv2.morphologyEx(thr, cv2.MORPH_OPEN, kernel, iterations=1)
    bg = cv2.dilate(opening, kernel, iterations=2)
    pil_im = Image.fromarray(bg)
    mask = Mask.from_img_data(pil_im)
    grid = MaskedGrid(mask)
    RecursiveBacktracker.on(grid)
    mz = grid.to_point_pairs(cell_size=4)


def refresh2d(width, height):
    glViewport(0, 0, width, height)
    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()
    glOrtho(0.0, width, 0.0, height, 0.0, 1.0)
    glMatrixMode (GL_MODELVIEW)
    glLoadIdentity()


def draw():      
    global mz  
    global width
    global height
    glClearColor(1, 1, 1, 1)
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
    glLoadIdentity()
    refresh2d(width, height)
    glColor3f(0.2, 0.2, 0.2)
    find_mz()
    draw_mz(mz)  
    glutSwapBuffers()   


global mz
global start
global width
global height
global processing
global cap
processing = False
window = 0
start = datetime.now()
cap = Camera([0], fps=30, resolution=Camera.RES_LARGE, colour=False)
find_mz()
width = 1400
height = 880

glutInit()
glutInitDisplayMode(GLUT_RGBA | GLUT_DOUBLE | GLUT_ALPHA | GLUT_DEPTH)
glutInitWindowSize(width, height)
glutInitWindowPosition(0, 0)
glutSetCursor(GLUT_CURSOR_NONE)
window = glutCreateWindow("test")
glutDisplayFunc(draw)
glutIdleFunc(draw)
glutMainLoop()

