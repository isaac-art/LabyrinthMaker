import os
import cv2
import numpy as np
# import sys
# from PIL import Image


def parse_name(name):
    xx, yy = name.split("_")
    x = xx[1:]
    y = yy[1:-4]
    return int(x), int(y)


def main(folder):
    pos = {}
    x_lim = 0
    y_lim = 0
    for file in os.listdir("split/"):
        x, y = parse_name(file)
        if x > x_lim:
            x_lim = x
        if y > y_lim:
            y_lim = y
        pos[(x, y)] = file
    # print(pos)
    # print("x_lim: %s, y_lim: %s" % (x_lim, y_lim))
    for x in range(x_lim):
        for y in range(y_lim):
            # print(pos[(x, y)])
            if y == 0:
                if x > 0:
                    cv2.imwrite('strips/out_%s_%s.png' % (x, y), vis)
                vis = cv2.imread('mz/%s' % pos[(x, y)])
                # the first image
            else:
                imgb = cv2.imread('mz/%s' % pos[(x, y)])
                vis = np.concatenate((vis, imgb), axis=0)
    # return full

    strips = {}
    co = 0
    for file in os.listdir("strips/"):
        num = file[4:-6]
        strips[num] = file
        co += 1

    for x in range(co):
        y = "%s" % (x+1)
        # print(strips[y])
        if x == 0:
            vis = cv2.imread('strips/%s' % strips[y])
        # elif y == '63':
        #     pass
        else: 
            imgb = cv2.imread('strips/%s' % strips[y])
            vis = np.concatenate((vis, imgb), axis=1)
    cv2.imwrite('mz_tiled/out_.png', vis)

# main("mz/")
