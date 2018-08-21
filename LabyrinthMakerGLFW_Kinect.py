import glfw
import cv2
import random
import freenect
import numpy as np
import frame_convert2
from Mask import Mask
from PIL import Image
from OpenGL.GL import *
from pseyepy import Camera
from datetime import datetime
from MaskedGrid import MaskedGrid
from RecursiveBacktracker import RecursiveBacktracker


class LabyrinthMaker():
    """LabyrinthMaker"""
    def __init__(self):
        # store time for logging
        self.start = datetime.now()

        # PS3EYECAM SETUP
        # self.cap = Camera([0], fps=30, resolution=Camera.RES_LARGE, colour=True, auto_gain=True, auto_exposure=True, auto_whitebalance=True)

        # WEBCAM SETUP
        # self.cap = cv2.VideoCapture(0)


        
        # LABY and GL 
        self.laby = []
        self.frame = 0
        self.l_bg = None
        self.width = 1280
        self.height = 720
        self.l_average = 0
        self.l_frame = None
        self.grid = None
        self.mask = None 
        self.f_num = 0
        self.saturation = 5
        self.point_size = 13.333

        # KINECT VALS
        self.kinect_threshold = 474
        self.kinect_current_depth = 45
    


    # PROCESS THE CAMERA INPUT
    def process_cam(self, sz, flip, bw=True, sm_dp=False):
        # get the frame
        # frame, timestamp = self.cap.read()
        # ret, frame = self.cap.read()
        frame = self.kinect_get_image()
        depth = self.kinect_get_depth()

        # UNDISTORT HERE?
        # need to undistort the rgb and the depth. 
        # or should i distort before cropping and scaling???
        # https://docs.opencv.org/3.0-beta/doc/py_tutorials/py_calib3d/py_calibration/py_calibration.html
        # https://docs.opencv.org/3.0-beta/modules/imgproc/doc/geometric_transformations.html

        # rgb_camera_matrix = [[fx, 0, cx][0, fy, cy][0, 0, 1]]
        # rgb_dist_coeffs = (k_1, k_2, p_1, p_2[, k_3[, k_4, k_5, k_6]]) 
        # depth_camera_matrix = [[fx, 0, cx][0, fy, cy][0, 0, 1]]
        # depth_dist_coeffs = (k_1, k_2, p_1, p_2[, k_3[, k_4, k_5, k_6]]) 

        rgb_camera_matrix = np.array([[5.2161910696979987e+02, 0.0, 3.1755491910920682e+02], 
                            [0.0, 5.2132946256749767e+02, 2.5921654718027673e+02], 
                            [0.0, 0.0, 1.0]])

        rgb_dist_coeffs = np.array([[2.5673002693536984e-01, -9.3976085633794137e-01, -1.8605549188751580e-03, -2.2232238578189420e-03, 1.2453643444153988e+00]])

        depth_camera_matrix = np.array([[5.8818670481438744e+02, 0.0, 3.1076280589210484e+02], 
                                [0.0, 5.8724220649505514e+02, 2.2887144980135292e+02], 
                                [0.0, 0.0, 1.0]])

        depth_dist_coeffs = np.array([[-1.8932947734719333e-01, 1.1358015104098631e+00, -4.4260345347128536e-03, -5.4869578635708153e-03, -2.2460143607712921e+00]])

        rgb_undistorted = cv2.undistort(frame, rgb_camera_matrix, rgb_dist_coeffs, None, rgb_camera_matrix)

        depth_undistorted = cv2.undistort(depth, depth_camera_matrix, depth_dist_coeffs, None, depth_camera_matrix)


        # crop to correct ratio
        frame = rgb_undistorted[0:360, 0:640]
        depth = depth_undistorted[0:360, 0:640]

        # -1 flip hori+vert / 1 flip vert / 0 flip hori
        frame = cv2.flip(frame, flip)
        depth = cv2.flip(depth, flip)
        # resize smaller for faster processing
        # small = cv2.resize(frame, (0, 0), fx=0.15, fy=0.15)
        small_depth = cv2.resize(depth, (0, 0), fx=sz, fy=sz)
        small = cv2.resize(frame, (0, 0), fx=sz, fy=sz)
        # small = cv2.cvtColor(small, cv2.COLOR_RGB2BGR)


        self.l_frame = small
        if not bw:
            return small
        if sm_dp:
            return small_depth
        # grayscale image, alreay gray if kinect
        # gray = cv2.cvtColor(small, cv2.COLOR_BGR2GRAY)
        # blur a small amount to smooth
        blur_depth = cv2.blur(small_depth, (2, 2))
        # threshold the image
        # otsu threshold is adaptive
        #   so will adjust to the range present in the image
        ret, thr = cv2.threshold(blur_depth, 1, 255, cv2.THRESH_BINARY_INV + cv2.THRESH_OTSU)
        # opening and dilating to remove noise
        # kernel size is size of operation
        kernel = np.ones((1, 1), np.uint8)
        opening = cv2.morphologyEx(thr, cv2.MORPH_OPEN, kernel, iterations=1)
        bg = cv2.dilate(opening, kernel, iterations=5)
        return bg


    # KINECT CONTROLS
    def kinect_change_threshold(self, value):
        self.kinect_threshold = value

    def kinect_change_depth(self, value):
        self.kinect_current_depth = value


    def kinect_get_depth(self):
        # depth: A numpy array, shape:(640,480) dtype:np.uint16
        # timestamp: int representing the time
        depth, timestamp = freenect.sync_get_depth()

        # filter depth range
        depth = 255 * np.logical_and(depth >= self.kinect_current_depth - self.kinect_threshold,
                                     depth <= self.kinect_current_depth + self.kinect_threshold)
        # convert to 8bit
        depth = depth.astype(np.uint8)
        # return image
        return depth

    def kinect_get_image(self):
        # im: A numpy array, shape:(480, 640, 3) dtype:np.uint8
        # timestamp: int representing the time
        img, timestamp = freenect.sync_get_video()
        return frame_convert2.video_cv(img)
         
    def change_saturation(self, value):
        self.saturation = value

    # KINECT CONTROLS GUI
    def draw_gui(self):  
        cv2.namedWindow("gui")
        cv2.createTrackbar('threshold', 'gui', self.kinect_threshold, 500, self.kinect_change_threshold)
        cv2.createTrackbar('depth', 'gui', self.kinect_current_depth, 2048, self.kinect_change_depth)
        # cv2.createTrackbar('saturation', 'gui', 5, 10, self.change_saturation)


    # DRAW CAMERA IMAGE
    def draw_cam(self):
        # draws the camera to a second window
        bg = self.process_cam(0.5, 0, bw=False)
        cv2.namedWindow("camera")
        # cv2.moveWindow("camera", 0, 0)
        cv2.imshow("camera", bg)

    # DRAW DEPTH IMAGE
    def draw_depth(self):
        # draws the camera to a second window
        bg = self.process_cam(0.5, 0, bw=True, sm_dp=True)
        cv2.namedWindow("depth")
        cv2.imshow("depth", bg)

    # DRAW THE IMAGE COLOURS TO THE GL BUFFER
    def draw_mask(self):   
        if self.mask is not None:

            # saturate
            # l_frame_hsv = cv2.cvtColor(self.l_frame, cv2.COLOR_BGR2HSV).astype("float32")
            # h, s, v = cv2.split(l_frame_hsv)
            # s = s * self.saturation
            # s = np.clip(s, 0, 255)
            # l_frame_hsv = cv2.merge([h, s, v])
            # self.l_frame = cv2.cvtColor(l_frame_hsv.astype("uint8"), cv2.COLOR_HSV2BGR) 

            # Blur the camera image 
            self.l_frame = cv2.blur(self.l_frame, (int(self.point_size/2), int(self.point_size/2)))

            # glPointSize(13.333*2)   
            glPointSize(self.point_size)
            glBegin(GL_POINTS)
            for r in range(self.mask.rows):
                for c in range(self.mask.columns):
                    if not self.mask.cell_at(r, c):
                        # if r-3 < self.mask.rows and c-3 > 0:
                        #     bb, gg, rr = self.l_frame[r-3, c-3]
                        # elif r-2 < self.mask.rows and c-2 > 0:
                        #     bb, gg, rr = self.l_frame[r-2, c-2]
                        # elif r-1 < self.mask.rows and c-1 > 0:
                        #     bb, gg, rr = self.l_frame[r-1, c-1]
                        # else:
                        #     bb, gg, rr = self.l_frame[r, c]
                        
                        bb, gg, rr = self.l_frame[r, c]

                        glColor3f(rr/255, gg/255, bb/255)
                        # offsetby 0.5 to fit colours inside mask
                        glVertex2f((c+0.5)*(self.point_size), (r+0.5)*(self.point_size))
                        # glVertex2f((c+0.5)*(13.333*2), (r+0.5)*(13.333*2))
                        # bb, gg, rr = self.l_frame[r+1, c+1]
                        # glColor3f(rr/255, gg/255, bb/255)
                        # glVertex2f(c*13.333+12, r*13.333+12)
            glEnd()


    # DRAW THE LABYRINTH PATH TO THE GL BUFFER
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
            glVertex2f(x1*3.333, y1*3.333)
            glVertex2f(x2*3.333, y2*3.333)
            # glVertex2f(x1*6.666, y1*6.666)
            # glVertex2f(x2*6.666, y2*6.666)
            # glVertex2f(x1*4, y1*4)
            # glVertex2f(x2*4, y2*4)
        # complete the shape and draw everything
        glEnd()


    # REFRESH THE GL BUFFERS
    def refresh_scene(self):
        # refresh the gl scene
        # NOTE: DOUBLE HEIGHT AND WIDTH FOR HIGHDPI(macbook), REDUCE FOR STANDARD(tv)
        # glViewport(0, 0, self.width*2, self.height*2)
        glViewport(0, 0, self.width, self.height)
        glMatrixMode(GL_PROJECTION)
        glLoadIdentity()
        glOrtho(0.0, self.width, 0.0, self.height, 0.0, 1.0)
        # glOrtho(0.0, self.width*2, 0.0, self.height*2, 0.0, 1.0)
        glMatrixMode (GL_MODELVIEW)
        glLoadIdentity()


    # LABYRINTH UPDATE LOOP
    def update(self):
        # update the labyrinth from camera image
        bg = self.process_cam(0.15, 0)
        # if not first frame
        if self.l_bg is not None:
            # calculate the average of the current bg
            average = np.average(bg)
            # compare to the last stored average
            diff = average - self.l_average
            # if there is a big enough difference +/-
            if diff > 0.65 or diff < -0.65:
            # if True:
                # translate numpy array to PIL image
                pil_im = Image.fromarray(bg)

                # TODO: PERHAPS CULD PUT SOME KIND OF BACKGROUND SUBTRACTION HERE ??
                # SOLVED: USE KINECT AND THRESHOLD ON DISTANCE TO REMOVE BG

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


    # SAVING IMAGES OF FRAMES OR TO VIDEO CAPTURE
    def save_frame(self):
        glReadBuffer(GL_BACK)
        fbuffer = glReadPixels(0, 0, self.width, self.height, GL_RGB, GL_UNSIGNED_BYTE)
        imagebuffer = np.fromstring(fbuffer, np.uint8)
        fimage = imagebuffer.reshape(self.height, self.width, 3)
        image = Image.fromarray(fimage)
        image.save("video_out/frames/live/%s.png" % self.f_num, 'png')
        outim = cv2.cvtColor(fimage, cv2.COLOR_RGB2BGR)
        self.out.write(outim)


    # THE GL DRAW LOOP
    def draw(self):
        glClearColor(1, 1, 1, 1)
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
        glLoadIdentity()
        self.refresh_scene()
        self.update()
        self.draw_mask()
        self.draw_laby()
        # self.save_frame()
        self.draw_cam()
        self.draw_depth()
        self.draw_gui()
        self.f_num = self.f_num + 1

    # MAKE GLFW WINDOW AND START THE LOOP
    def main(self):
        if not glfw.init():
            return
        # http://www.glfw.org/docs/latest/monitor_guide.html#monitor_monitors
        # monitor = glfw.get_primary_monitor()
        # mode = monitor.video_mode
        window = glfw.create_window(self.width, self.height, "LabyrinthMaker_GLFW", None, None)
        if not window:
            glfw.terminate()
            return
        glfw.make_context_current(window)
        while not glfw.window_should_close(window):
            # render
            self.draw()
            glfw.swap_buffers(window)
            glfw.poll_events()
        glfw.terminate()

# init labyrinth
labyrinth = LabyrinthMaker()
# start the whole thing up
labyrinth.main()
