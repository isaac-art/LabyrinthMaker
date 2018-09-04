import os
import sys
import cv2
import shutil
import numpy as np
from Mask import Mask
from MaskedGrid import MaskedGrid
from RecursiveBacktracker import RecursiveBacktracker
from datetime import datetime


def makeMaze(img_path, folder):
    # use the provided image and make a mask
    mask = Mask.from_png(img_path)
    # make a grid from the mask
    grid = MaskedGrid(mask)
    # run the backtracker
    RecursiveBacktracker.on(grid)
    # get label from filename
    split = img_path.split("/")
    split_two = split[1].split(".")
    label = split_two[0]
    # print(label)
    # genertae image
    img = grid.to_png(cell_size=4, folder=folder, name=label, save=True)
    # send the image back up
    return img

def main(img_path, folder):
    # generate from the path provided
    img = makeMaze(img_path, "live_mz")
    # return the response
    return img


if __name__ == "__main__":
    # python demo4.py file:cv
    startTime = datetime.now()
    main(sys.argv[1], sys.argv[1])
    print("Completed In: %s" % (datetime.now() - startTime))
