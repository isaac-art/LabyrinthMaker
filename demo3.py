import os
import sys
# import stitch
# import split
from Mask import Mask
from MaskedGrid import MaskedGrid
# from BinaryTree import BinaryTree
# from Sidewinder import Sidewinder
from RecursiveBacktracker import RecursiveBacktracker
from datetime import datetime


# invoke: $ python demo2.py "image.png" 100
def main(sfile):
    out = "laby/"
    if not os.path.exists(out):
        os.makedirs(out)
    mask = Mask.from_png(sfile)
    grid = MaskedGrid(mask)
    loc = sfile[:-4]
    RecursiveBacktracker.on(grid)
    img = grid.to_png(cell_size=4, folder=out, name=loc)
    return


if __name__ == "__main__":
    start = datetime.now()
    main(sys.argv[1])
    print("Completed In: %s" % (datetime.now() - start))

