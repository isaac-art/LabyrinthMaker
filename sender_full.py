# import os
import sys
# import time
import cv2
# import random
# import shutil
import OneTile
from PIL import Image
import numpy as np
from pseyepy import Camera
# from math import floor
from tomorrow import threads
from skimage.measure import compare_ssim
from datetime import datetime
from Mask import Mask
from RecursiveBacktracker import RecursiveBacktracker
from MaskedGrid import MaskedGrid

processing = False


@threads(20)
def callTile(path):
    OneTile.main(path, "live_mz")
    return


def maze(width, height, sz):
    for x in range(width // sz):
        for y in range(height // sz):
            lab = "live_cv/x%s_y%s.png" % (x, y)
            callTile(lab)
            y += sz
        x += sz
    return


def save_seg(seg, lab):
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
    for x in range(width // sz):
        for y in range(height // sz):
            lab = "live_cv/x%s_y%s.png" % (x, y)
            imageB = cv2.imread(lab, 0)
            seg = bg[y * sz:y * sz + sz, x * sz:x * sz + sz]

            # mean squared error
            # err = np.sum((seg.astype("float") - imageB.astype("float")) ** 2)
            # err /= float(seg.shape[0] * seg.shape[1])
            # structural similarity
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


def detect_diffs_two(vals, c, width, height, sz, bg):
    lab = "live_full_mz/live_full_mz.png"
    image_b_sm = cv2.imread(lab, 0)
    image_b_sm = cv2.resize(image_b_sm, (320, 240))
    wid, hei = image_b_sm.shape
    # print("w:%s, h:%s, iw:%s, ih:%s" % (width//2, height//2, wid, hei))
    err = compare_ssim(bg, image_b_sm)
    return err


@threads(1)
def processFrame(bg):
    start = datetime.now()
    pil_im = Image.fromarray(bg)
    mask = Mask.from_img_data(pil_im)
    grid = MaskedGrid(mask)
    RecursiveBacktracker.on(grid)
    # img = grid.to_png(cell_size=4, folder="live_full_mz", name="live_full_mz", save=False)
    img = grid.to_png_inset(cell_size=8, inset=0.25, folder="live_full_mz", name="live_full_mz", save=False)
    global processing
    processing = False
    print("updated in : %s" % (datetime.now() - start))
    return img


def main(cam, show, pseye):
    if pseye == 1:
        cap = Camera([0], fps=60, resolution=Camera.RES_LARGE, colour=False)
        # frame, timestamp  = cap.read()
        # width, height = frame.shape
    else:
        cap = cv2.VideoCapture(cam)
        # width = floor(cap.get(3)) // 2
        # height = floor(cap.get(4)) // 2
    # sz = 100
    run = True
    # vals = {}
    mz = cv2.imread("live_full_mz/live_full_mz.png")
    # mz_sm =  cv2.resize(mz, (0,0), fx=0.3, fy=0.3)
    global processing
    c = 1
    # last_diff = 0

    cv2.namedWindow("mz", cv2.WND_PROP_FULLSCREEN)
    cv2.setWindowProperty("mz", cv2.WND_PROP_FULLSCREEN, cv2.WINDOW_FULLSCREEN)
    cv2.setWindowProperty("mz", cv2.WND_PROP_ASPECT_RATIO, cv2.WINDOW_FREERATIO)

    if show == 0:
        window = False
    else:
        window = True
    while(run):
        try:
            if pseye == 1:
                frame, timestamp = cap.read()
                # width, height = frame.shape
            else:
                ret, frame = cap.read()

            frame = frame[100:320, 100:540]
            small = cv2.resize(frame, (0, 0), fx=0.25, fy=0.25)
            # gray = cv2.cvtColor(small,cv2.COLOR_BGR2GRAY)
            ret, thr = cv2.threshold(small, 1, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)
            kernel = np.ones((1, 1), np.uint8)
            opening = cv2.morphologyEx(thr, cv2.MORPH_OPEN, kernel, iterations=1)
            bg = cv2.dilate(opening, kernel, iterations=2)

            # if c < 50:
            if not processing:
                    # diff = detect_diffs_two(vals, c, width, height, sz, bg)
                    # print(diff - last_diff)
                    # d_sum = diff - last_diff
                    # if d_sum > 0.005 or d_sum < -0.005:
                processing = True
                mz = processFrame(bg)
                try:
                    mz = np.array(mz)
                    # mz = cv2.resize(mz, (0, 0), fx=4, fy=4)
                except Exception as e:
                    print(e)
                    pass
                    # mz = cv2.imread("live_full_mz/live_full_mz.png")

                    # last_diff = diff
                    # mz_sm =  cv2.resize(mz, (0,0), fx=0.3, fy=0.3)
                    # mz - cv2.imread("live_full/", 1)
                    #  detect_diffs(vals, c, width, height, sz, bg)
                    # print("----")

            if window:
                try:
                    # cv2.imshow('cam', bg)
                    cv2.imshow('mz', mz)
                except Exception as e:
                    print(e)
                    pass
            k = cv2.waitKey(1)
            # if k == ord('+'):
            #     mz = cv2.resize(mz, (0,0), fx=1.1, fy=1.1)
            # if k == ord('-'):
            #     mz = cv2.resize(mz, (0,0), fx=0.9, fy=0.9)
            if k == ord('q'):
                run = False
            c += 1
        except Exception as e:
            print(e)
            pass
    if pseye == 1:
        cap.end()
    else:
        cap.release()
    cv2.destroyAllWindows()


if __name__ == "__main__":
    # invoke: python sender_full.py cam_num show(0=false) pseye(0=false)
    cam = int(sys.argv[1])
    window = int(sys.argv[2])
    pseye = int(sys.argv[3])
    if window == 0:
        print("loading camera %s with no window. Ctrl-C to quit" % cam)
    else:
        print("loading camera %s with window. q to quit" % cam)
    main(cam, window, pseye)
