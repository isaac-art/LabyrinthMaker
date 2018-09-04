import os
import cv2
import numpy as np
# import sys
# from PIL import Image


# 
# This was an earlier version for static labyrinths
# They were processed as individual tiles and this 
# joined the tiles together as one image
# 


def parse_name(name):
    # split the name on the underscore
    xx, yy = name.split("_")
    # remove the extra bits from the strings
    x = xx[1:]
    y = yy[1:-4]
    # return integer version of x & y pos
    return int(x), int(y)


def main(folder):
    pos = {}
    x_lim = 0
    y_lim = 0
    # For every image in the folder
    for file in os.listdir("split/"):
        # call parse name finction which returns a tuple
        x, y = parse_name(file)
        # check against boundaries
        if x > x_lim:
            x_lim = x
        if y > y_lim:
            y_lim = y
        pos[(x, y)] = file
    # print(pos)
    # print("x_lim: %s, y_lim: %s" % (x_lim, y_lim))

    # for everything in the range (aka all the images)
    for x in range(x_lim):
        for y in range(y_lim):
            # print(pos[(x, y)])
            if y == 0:
                if x > 0:
                    # the column is completer
                    cv2.imwrite('strips/out_%s_%s.png' % (x, y), vis)
                # read the pixels of the tile
                vis = cv2.imread('mz/%s' % pos[(x, y)])
                # the first image
            else:
                # read pixels of tile
                imgb = cv2.imread('mz/%s' % pos[(x, y)])
                # add the list to the other list on coreect axis
                vis = np.concatenate((vis, imgb), axis=0)
    # return full

    strips = {}
    co = 0
    # for every column prep the size
    for file in os.listdir("strips/"):
        num = file[4:-6]
        strips[num] = file
        co += 1

    # for every column image
    for x in range(co):
        y = "%s" % (x+1)
        # print(strips[y])
        if x == 0:
            # get the pixels
            vis = cv2.imread('strips/%s' % strips[y])
        # elif y == '63':
        #     pass
        else: 
            imgb = cv2.imread('strips/%s' % strips[y])
            # add to horizontal side of list
            vis = np.concatenate((vis, imgb), axis=1)

    # SAVE THE COMPLETED IMAGE
    cv2.imwrite('mz_tiled/out_.png', vis)

# main("mz/")
