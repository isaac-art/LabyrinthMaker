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
    mask = Mask.from_png(img_path)
    grid = MaskedGrid(mask)
    RecursiveBacktracker.on(grid)
    split = img_path.split("/")
    split_two = split[1].split(".")
    label = split_two[0]
    # print(label)
    img = grid.to_png(cell_size=4, folder=folder, name=label, save=True)
    return img

def main(img_path, folder):
    img = makeMaze(img_path, "live_mz")
    return img


if __name__ == "__main__":
    # python demo4.py file:cv
    startTime = datetime.now()
    main(sys.argv[1], sys.argv[1])
    print("Completed In: %s" % (datetime.now() - startTime))
