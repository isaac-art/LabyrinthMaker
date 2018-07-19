import cv2
from datetime import datetime
from PIL import Image
import numpy as np
from pseyepy import Camera
from OpenGL.GL import *
from OpenGL.GLUT import *
from OpenGL.GLU import *
from Mask import Mask
from MaskedGrid import MaskedGrid
from RecursiveBacktracker import RecursiveBacktracker


class LabyrinthMaker():
    """LabyrinthMaker"""
    def __init__(self):
        self.start = datetime.now()
        # self.cap = Camera([0], fps=30, resolution=Camera.RES_LARGE, colour=False)
        self.cap = cv2.VideoCapture(0)
        self.laby = []
        self.l_bg = None
        self.width = 1280
        self.height = 720
        self.l_average = 0


    def process_cam(self, sz, flip):
        # get the frame
        ret, frame = self.cap.read()
        frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        # crop to correct ratio if pseyecam
        # frame = frame[0:360, 0:640]
        # -1 flip hori+vert / 1 flip vert / 0 flip hori
        frame = cv2.flip(frame, flip)
        # resize smaller for faster processing
        # small = cv2.resize(frame, (0, 0), fx=0.15, fy=0.15)
        small = cv2.resize(frame, (0, 0), fx=sz, fy=sz)
        # threshold the image
        # otsu threshold is adaptive
        #   so will adjust to the range present in the image
        ret, thr = cv2.threshold(small, 1, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)
        # opening and dilating to remove noise
        # kernel size is size of operation
        kernel = np.ones((1, 1), np.uint8)
        opening = cv2.morphologyEx(thr, cv2.MORPH_OPEN, kernel, iterations=1)
        bg = cv2.dilate(opening, kernel, iterations=3)
        return bg


    def draw_cam(self):
        # draws the camera to a second window
        bg = self.process_cam(0.5, 1)
        cv2.namedWindow("camera")
        cv2.moveWindow("camera", 0, 0)
        cv2.imshow("camera", bg)


    def draw_laby(self):
        # Draws the labyrinth to gl
        # set the line width for drawing
        glLineWidth(1)
        # set the color of the line
        glColor3f(0.1, 0.1, 0.1)
        # begin shape with pairs of lines
        glBegin(GL_LINES)
        # the list of points is backwards so reverse it
        # self.mz.reverse()
        # loop over coordinates adding all the vertices
        for loc in self.laby:
            x1, y1, x2, y2 = loc
            # @ 0.1  = *5
            # @ 0.25 = *2
            # @ 0.15 = *3.333 
            # glVertex2f(x1*3.333, y1*3.333)
            # glVertex2f(x2*3.333, y2*3.333)
            glVertex2f(x1*2, y1*2)
            glVertex2f(x2*2, y2*2)
        # complete the shape and draw everything
        glEnd()


    def refresh_scene(self):
        # refresh the gl scene
        glViewport(0, 0, self.width, self.height)
        glMatrixMode(GL_PROJECTION)
        glLoadIdentity()
        glOrtho(0.0, self.width, 0.0, self.height, 0.0, 1.0)
        glMatrixMode (GL_MODELVIEW)
        glLoadIdentity()


    def update(self):
        # update the labyrinth from camera image
        bg = self.process_cam(0.125, -1)
        # if not first frame
        if self.l_bg is not None:
            # calculate the average of the current bg
            average = np.average(bg)
            # compare to the last stored average
            diff = average - self.l_average
            # if there is a big enough difference +/-
            if diff > 1 or diff < -1:
                # translate numpy array to PIL image
                pil_im = Image.fromarray(bg)
                # make a mask from the image
                mask = Mask.from_img_data(pil_im)
                # build a grid from the unmasked areas
                grid = MaskedGrid(mask)
                # build walls in the grid
                RecursiveBacktracker.on(grid)
                # get walls as list of coordinate pairs for drawing
                self.laby = grid.to_point_pairs(cell_size=4)
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
        self.draw_laby()
        self.draw_cam()
        glutSwapBuffers()


    def main(self):
        glutInit()
        glutInitDisplayMode(GLUT_RGBA | GLUT_DOUBLE | GLUT_ALPHA | GLUT_DEPTH)
        glutInitWindowSize(self.width, self.height)
        glutInitWindowPosition(1280, 0)
        glutSetCursor(GLUT_CURSOR_NONE)
        window = glutCreateWindow("LabyrinthMaker")
        glutDisplayFunc(self.draw)
        glutIdleFunc(self.draw)
        glutMainLoop()


labyrinth = LabyrinthMaker()
labyrinth.main()
