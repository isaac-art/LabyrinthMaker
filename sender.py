import os
import sys
import time
import cv2
import random
import shutil
import OneTile
import numpy as np
from math import floor
from tomorrow import threads
from skimage.measure import compare_ssim
from datetime import datetime

# 
# This is an earlier version of the program
# when i was still making large still images
# for prints
# 


# use multithreading to process multiple sections of the
# image simultaneously, makes it faster!
@threads(20)
def callTile(path):
    # call the OneTile script
    OneTile.main(path, "live_mz")
    return


def maze(width, height, sz):
    # for each area of variable size across the image
    for x in range(width // sz):
        for y in range(height // sz):
            # image name
            lab = "live_cv/x%s_y%s.png" % (x, y)
            # process it
            callTile(lab)
            y += sz
        x += sz
    return


def save_seg(seg, lab):
    # try save the image and if it fails skip it
    try:
        cv2.imwrite(lab, seg)
    except Exception as e:
        print(e)
        pass


def save(width, height, sz, bg):
    for x in range(width // sz):
        for y in range(height // sz):
            # print("w:%s, h:%s, sz:%s" % (width, height, sz))
            seg = bg[y * sz:y * sz + sz, x * sz:x * sz + sz]
            lab = "live_cv/x%s_y%s.png" % (x, y)
            try:
                cv2.imwrite(lab, seg)
            except Exception as e:
                print(e)
                pass
            y += sz
        x += sz
    return


def detect_diffs(vals, c, width, height, sz, bg):
    # detect differces in the sturctual similarity

    # this allows us to only update sections of the image
    # that have changed! rather than processing everything 
    # every single frame

    for x in range(width // sz):
        for y in range(height // sz):
            lab = "live_cv/x%s_y%s.png" % (x, y)
            imageB = cv2.imread(lab, 0)
            seg = bg[y * sz:y * sz + sz, x * sz:x * sz + sz]

            #mean squared error
            # err = np.sum((seg.astype("float") - imageB.astype("float")) ** 2)
            # err /= float(seg.shape[0] * seg.shape[1])
            #structural similarity
            err = compare_ssim(seg, imageB)
            if c == 0:
                # print("val: x%s, y%s err:%s" % (x, y, err))
                vals[(x, y)] = err
            else:
                diff = vals[(x, y)] - err
                # print("val: x%s, y%s diff:%s" % (x, y, diff))
                if diff > 0.1:
                    vals[(x, y)] = err
                    # print("saving")
                    save_seg(seg, lab)
                    # print("mazing")
                    callTile(lab)
                    # print("done")
            y += sz
        x += sz
    return


def main(cam, show):
    # get camera from args
    cap = cv2.VideoCapture(cam)
    # get size of image
    width = floor(cap.get(3)) // 2
    height = floor(cap.get(4)) // 2
    # variables
    sz = 100
    run = True
    vals = {}
    c = 0
    # is there a window, faster without
    if show == 0:
        window = False
    else:
        window = True

    # While loop runs
    while(run):
        # get the frame
        ret, frame = cap.read()
        # applu transformations, see LabyrinthMakerGLFW_Kinect.py for
        # full explanations
        small = cv2.resize(frame, (0,0), fx=0.5, fy=0.5)
        gray = cv2.cvtColor(small,cv2.COLOR_BGR2GRAY)
        ret, thr = cv2.threshold(gray, 1, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)
        kernel = np.ones((2, 2), np.uint8)
        opening = cv2.morphologyEx(thr, cv2.MORPH_OPEN, kernel, iterations=2)
        bg = cv2.dilate(opening, kernel, iterations=3)

        if window:
            cv2.imshow('a', bg)
        # if (c % 20) == 0:
        #    detect_diffs(vals, c, width, height, sz, bg)
            # print("----")
        k = cv2.waitKey(1)
        if k == ord('q'):
            run = False
        c += 1
    # close camera and quit
    cap.release()
    cv2.destroyAllWindows()


if __name__ == "__main__":
    # invoke: python sender.py cam_num show(0=false)
    cam = int(sys.argv[1])
    window = int(sys.argv[2])
    if window == 0:
        print("loading camera %s with no window. Ctrl-C to quit" % cam)
    else:
        print("loading camera %s with window. q to quit" % cam)
    main(cam, window)


