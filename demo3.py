import os
import sys
# import stitch
# import split
# import svgwrite

from OpenGL.GL import *
from OpenGL.GLUT import *
from OpenGL.GLU import *

from Mask import Mask
from MaskedGrid import MaskedGrid
# from BinaryTree import BinaryTree
# from Sidewinder import Sidewinder
from RecursiveBacktracker import RecursiveBacktracker
from datetime import datetime


def draw_mz(mz):
    glLineWidth(2)
    glBegin(GL_LINES)
    for loc in mz:  
        x1, y1, x2, y2 = loc                 
        glVertex2f(x1*2, y1*2)            
        glVertex2f(x2*2, y2*2)                   
    glEnd() 


def refresh2d(width, height):
    glViewport(0, 0, width, height)
    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()
    glOrtho(0.0, width, 0.0, height, 0.0, 1.0)
    glMatrixMode (GL_MODELVIEW)
    glLoadIdentity()


def draw():      
    global mz  
    glClearColor(1, 1, 1, 1)
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
    glLoadIdentity()
    refresh2d(width, height)
    glColor3f(0.2, 0.2, 0.2)
    draw_mz(mz)  
    start = datetime.now()
    glutSwapBuffers()   


def maze(sfile):
    out = "laby/"
    if not os.path.exists(out):
        os.makedirs(out)
    mask = Mask.from_png(sfile)
    grid = MaskedGrid(mask)
    RecursiveBacktracker.on(grid)
    global mz
    mz, wid, hei = grid.to_point_pairs(cell_size=4)
    return mz, wid, hei



global mz
global start
global width
global height
window = 0
start = datetime.now()

mz, wid, hei = maze("_full_cv.png")
width = wid*2
height = hei*2

glutInit()
glutInitDisplayMode(GLUT_RGBA | GLUT_DOUBLE | GLUT_ALPHA | GLUT_DEPTH)
glutInitWindowSize(width, height)
glutInitWindowPosition(0, 0)
window = glutCreateWindow("test")
glutDisplayFunc(draw)
glutIdleFunc(draw)
glutMainLoop()

