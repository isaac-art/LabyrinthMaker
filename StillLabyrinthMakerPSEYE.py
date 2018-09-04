import cv2
from datetime import datetime
from random import randint
from PIL import Image
import numpy as np
from pseyepy import Camera
from OpenGL.GL import *
from OpenGL.GLUT import *
from OpenGL.GLU import *
from Mask import Mask
from MaskedGrid import MaskedGrid
from RecursiveBacktracker import RecursiveBacktracker


# 
# THIS IS AN EARLIER VERSION SHOWING A CAMERA BASED
# BUT STILL LABYRINTH.
# IT OPENS CAMERA AND SAVES TO A FILE
# VERY SIMILAR TO sender.py and OneTile.py 
# and influence the final LabyrinthMakerGLFW_Kinect.py
# and LabyrinthMakerVideoIn.py

class StillLabyrinthMaker():
    """StillLabyrinthMaker"""
    def __init__(self):
        self.start = datetime.now()
        self.cap = Camera([0], fps=30, resolution=Camera.RES_LARGE, colour=True, auto_gain=True, auto_exposure=True, auto_whitebalance=True)
        self.laby = []
        self.l_bg = None
        self.width = 1280
        self.height = 720
        self.l_average = 0
        self.mask = None
        self.grid = None
        self.col_frame = None
        self.c_size = 4


    def process_cam(self, sz, flip):
        frame, timestamp = self.cap.read()
        self.col_frame = frame.copy()
        frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        frame = frame[0:360, 0:640]
        # frame = cv2.flip(frame, flip)
        small = cv2.resize(frame, (0, 0), fx=0.25, fy=0.25)
        ret, thr = cv2.threshold(small, 1, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)
        kernel = np.ones((1, 1), np.uint8)
        opening = cv2.morphologyEx(thr, cv2.MORPH_OPEN, kernel, iterations=1)
        bg = cv2.dilate(opening, kernel, iterations=3)
        return bg


    def add_cam_col(self):
        pix = self.laby.load()
        for r in range(self.mask.rows):
            for c in range(self.mask.columns):
                if not self.mask.cell_at(r, c):
                    red, gre, blu = self.col_frame[r*4, c*4]
                    col = (red, gre, blu)
                    pix[c*4, r*4] = col

                    red, gre, blu = self.col_frame[r*4, c*4+1]
                    col = (red, gre, blu)
                    pix[c*4, r*4+1] = col


                    red, gre, blu = self.col_frame[r*4, c*4+2]
                    col = (red, gre, blu)
                    pix[c*4, r*4+2] = col

                    red, gre, blu = self.col_frame[r*4, c*4+3]
                    col = (red, gre, blu)
                    pix[c*4, r*4+3] = col

                    red, gre, blu = self.col_frame[r*4+1, c*4]
                    col = (red, gre, blu)
                    pix[c*4+1, r*4] = col

                    red, gre, blu = self.col_frame[r*4+2, c*4]
                    col = (red, gre, blu)
                    pix[c*4+2, r*4] = col

                    red, gre, blu = self.col_frame[r*4+3, c*4]
                    col = (red, gre, blu)
                    pix[c*4+3, r*4] = col

                    red, gre, blu = self.col_frame[r*4+1, c*4+1]
                    col = (red, gre, blu)
                    pix[c*4+1, r*4+1] = col

                    red, gre, blu = self.col_frame[r*4+2, c*4+1]
                    col = (red, gre, blu)
                    pix[c*4+2, r*4+1] = col

                    red, gre, blu = self.col_frame[r*4+3, c*4+1]
                    col = (red, gre, blu)
                    pix[c*4+3, r*4+1] = col

                    red, gre, blu = self.col_frame[r*4+1, c*4+2]
                    col = (red, gre, blu)
                    pix[c*4+1, r*4+2] = col

                    red, gre, blu = self.col_frame[r*4+2, c*4+2]
                    col = (red, gre, blu)
                    pix[c*4+2, r*4+2] = col

                    red, gre, blu = self.col_frame[r*4+3, c*4+2]
                    col = (red, gre, blu)
                    pix[c*4+3, r*4+2] = col

                    red, gre, blu = self.col_frame[r*4+1, c*4+3]
                    col = (red, gre, blu)
                    pix[c*4+1, r*4+3] = col

                    red, gre, blu = self.col_frame[r*4+2, c*4+3]
                    col = (red, gre, blu)
                    pix[c*4+2, r*4+3] = col

                    red, gre, blu = self.col_frame[r*4+3, c*4+3]
                    col = (red, gre, blu)
                    pix[c*4+3, r*4+3] = col


    def draw(self):
        self.add_cam_col()
        self.laby.save("{}/{}.png".format("laby", "testtesttest"), "PNG", optimize=True)
         

    def main(self):
        bg = self.process_cam(0.125, -1)
        pil_im = Image.fromarray(bg)
        self.mask = Mask.from_img_data(pil_im)
        self.grid = MaskedGrid(self.mask)
        RecursiveBacktracker.on(self.grid)
        self.laby = self.grid.to_png(cell_size=self.c_size, save=False)
        self.draw()
        print("Completed In: %s" % (datetime.now() - self.start))


labyrinth = StillLabyrinthMaker()
labyrinth.main()
