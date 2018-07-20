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


class StillLabyrinthMaker():
    """StillLabyrinthMaker"""
    def __init__(self):
        self.start = datetime.now()
        self.cap = cv2.VideoCapture(0)
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
        ret, frame = self.cap.read()
        self.col_frame = frame.copy()
        frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        # frame = frame[0:360, 0:640]
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
                    blu, gre, red = self.col_frame[r*4, c*4]
                    col = (red, gre, blu)
                    pix[c*4, r*4] = col

                    blu, gre, red = self.col_frame[r*4, c*4+1]
                    col = (red, gre, blu)
                    pix[c*4, r*4+1] = col


                    blu, gre, red = self.col_frame[r*4, c*4+2]
                    col = (red, gre, blu)
                    pix[c*4, r*4+2] = col

                    blu, gre, red = self.col_frame[r*4, c*4+3]
                    col = (red, gre, blu)
                    pix[c*4, r*4+3] = col

                    blu, gre, red = self.col_frame[r*4+1, c*4]
                    col = (red, gre, blu)
                    pix[c*4+1, r*4] = col

                    blu, gre, red = self.col_frame[r*4+2, c*4]
                    col = (red, gre, blu)
                    pix[c*4+2, r*4] = col

                    blu, gre, red = self.col_frame[r*4+3, c*4]
                    col = (red, gre, blu)
                    pix[c*4+3, r*4] = col

                    blu, gre, red = self.col_frame[r*4+1, c*4+1]
                    col = (red, gre, blu)
                    pix[c*4+1, r*4+1] = col

                    blu, gre, red = self.col_frame[r*4+2, c*4+1]
                    col = (red, gre, blu)
                    pix[c*4+2, r*4+1] = col

                    blu, gre, red = self.col_frame[r*4+3, c*4+1]
                    col = (red, gre, blu)
                    pix[c*4+3, r*4+1] = col

                    blu, gre, red = self.col_frame[r*4+1, c*4+2]
                    col = (red, gre, blu)
                    pix[c*4+1, r*4+2] = col

                    blu, gre, red = self.col_frame[r*4+2, c*4+2]
                    col = (red, gre, blu)
                    pix[c*4+2, r*4+2] = col

                    blu, gre, red = self.col_frame[r*4+3, c*4+2]
                    col = (red, gre, blu)
                    pix[c*4+3, r*4+2] = col

                    blu, gre, red = self.col_frame[r*4+1, c*4+3]
                    col = (red, gre, blu)
                    pix[c*4+1, r*4+3] = col

                    blu, gre, red = self.col_frame[r*4+2, c*4+3]
                    col = (red, gre, blu)
                    pix[c*4+2, r*4+3] = col

                    blu, gre, red = self.col_frame[r*4+3, c*4+3]
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
