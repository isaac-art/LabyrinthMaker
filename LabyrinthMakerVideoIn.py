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


class LabyrinthMaker():
    """LabyrinthMaker"""
    def __init__(self):
        self.start = datetime.now()
        self.laby = []
        self.l_bg = None
        self.width = 1280
        self.height = 720
        # self.width = 1280
        # self.height = 720   
        # 425 for bloom videos
        # self.width = 425
        # self.height = 425
        self.l_average = 0
        self.l_frame = None
        self.grid = None
        self.mask = None 
        self.f_num = 0
        # camera and output video 
        # self.cap = Camera([0], fps=30, resolution=Camera.RES_LARGE, colour=True, auto_gain=True, auto_exposure=True, auto_whitebalance=True)
        self.cap = cv2.VideoCapture("video_in/TheDead.mkv")
        self.fourcc = cv2.VideoWriter_fourcc(*'MJPG')
        self.out = cv2.VideoWriter('video_out/bb.avi', self.fourcc, 20.0, (self.width,self.height))


    def process_cam(self, sz, flip, bw=True):
        # get the frame
        ret, frame = self.cap.read()
        if ret:
            # crop to correct ratio
            # frame = frame[100:460, 0:640]
            # frame = frame[0:360, 0:640]
            # -1 flip hori+vert / 1 flip vert / 0 flip hori
            # frame = cv2.flip(frame, 1)
            # resize smaller for faster processing
            # small = cv2.resize(frame, (0, 0), fx=0.15, fy=0.15)
            small = cv2.resize(frame, (0, 0), fx=sz, fy=sz)
            # small = cv2.cvtColor(small, cv2.COLOR_RGB2BGR)
            self.l_frame = small
            if not bw:
                return small
            gray = cv2.cvtColor(small, cv2.COLOR_BGR2GRAY)
            # threshold the image
            # otsu threshold is adaptive
            #   so will adjust to the range present in the image
            ret, thr = cv2.threshold(gray, 1, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)
            # opening and dilating to remove noise
            # kernel size is size of operation
            kernel = np.ones((1, 1), np.uint8)
            opening = cv2.morphologyEx(thr, cv2.MORPH_OPEN, kernel, iterations=1)
            bg = cv2.dilate(opening, kernel, iterations=3)
            return bg
        else:
            self.cap.release()
            self.out.release()
            exit()


    def draw_cam(self):
        # draws the camera to a second window
        bg = self.process_cam(0.5, 1, bw=False)
        cv2.namedWindow("camera")
        cv2.moveWindow("camera", 0, 0)
        cv2.imshow("camera", bg)


    def draw_mask(self):   
        if self.mask is not None:
            # saturate 
            l_frame_hsv = cv2.cvtColor(self.l_frame, cv2.COLOR_BGR2HSV).astype("float32")
            h, s, v = cv2.split(l_frame_hsv)
            s = s * 10
            s = np.clip(s, 0, 255)
            l_frame_hsv = cv2.merge([h, s, v])
            self.l_frame = cv2.cvtColor(l_frame_hsv.astype("uint8"), cv2.COLOR_HSV2BGR) 

            # Blur the camera image 
            self.l_frame = cv2.blur(self.l_frame, (12, 12))

            glPointSize(20)     
            glBegin(GL_POINTS)
            for r in range(self.mask.rows):
                for c in range(self.mask.columns):
                    if not self.mask.cell_at(r, c):
                        bb, gg, rr = self.l_frame[r, c]
                        glColor3f(rr/255, gg/255, bb/255)
                        # glVertex2f((c+0.5)*13.333, (r+0.5)*13.333)
                        glVertex2f((c+0.5)*20, (r+0.5)*20)

                        # bb, gg, rr = self.l_frame[r+1, c+1]
                        # glColor3f(rr/255, gg/255, bb/255)
                        # glVertex2f(c*13.333+12, r*13.333+12)

            glEnd()


    def draw_laby(self):
        # Draws the labyrinth to gl
        # set the line width for drawing
        glLineWidth(1)
        # set the color of the line
        glColor3f(0.1, 0.1, 0.2)
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
            glVertex2f(x1*5, y1*5)
            glVertex2f(x2*5, y2*5)
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
        bg = self.process_cam(0.05, 1)
        # if not first frame
        if self.l_bg is not None:
            # calculate the average of the current bg
            average = np.average(bg)
            # compare to the last stored average
            diff = average - self.l_average
            # if there is a big enough difference +/-
            if diff > 1.5 or diff < -1.5:
                # translate numpy array to PIL image
                pil_im = Image.fromarray(bg)
                # make a mask from the image
                self.mask = Mask.from_img_data(pil_im)
                # build a grid from the unmasked areas
                self.grid = MaskedGrid(self.mask)
                # build walls in the grid
                RecursiveBacktracker.on(self.grid)
                # get walls as list of coordinate pairs for drawing
                self.laby = self.grid.to_point_pairs(cell_size=4)
            # save the new average
            self.l_average = average
        # save the background
        self.l_bg = bg


    def save_frame(self):
        glReadBuffer(GL_BACK)
        fbuffer = glReadPixels(0, 0, self.width, self.height, GL_RGB, GL_UNSIGNED_BYTE)
        imagebuffer = np.fromstring(fbuffer, np.uint8)
        fimage = imagebuffer.reshape(self.height, self.width, 3)
        # image = Image.fromarray(fimage)
        # image.save("video_out/frames/%s.png" % self.f_num, 'png')
        outim = cv2.cvtColor(fimage, cv2.COLOR_RGB2BGR)
        self.out.write(outim)


    def draw(self):
        glClearColor(1, 1, 1, 1)
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
        glLoadIdentity()
        self.refresh_scene()
        self.update()
        self.draw_mask()
        self.draw_laby()
        # self.draw_cam()
        self.save_frame()
        self.f_num += 1
        glutSwapBuffers()


    def main(self):
        glutInit()
        glutInitDisplayMode(GLUT_RGBA | GLUT_DOUBLE | GLUT_ALPHA | GLUT_DEPTH)
        glutInitWindowSize(self.width, self.height)
        glutInitWindowPosition(1280, 0)
        glutSetCursor(GLUT_CURSOR_NONE)
        window = glutCreateWindow("PathMaker")
        glutDisplayFunc(self.draw)
        glutIdleFunc(self.draw)
        glutMainLoop()


labyrinth = LabyrinthMaker()
labyrinth.main()
