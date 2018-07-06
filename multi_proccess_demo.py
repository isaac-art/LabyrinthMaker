import os
import sys
import stitch
import split
from Mask import Mask
from MaskedGrid import MaskedGrid
from RecursiveBacktracker import RecursiveBacktracker
from multiprocessing import Pool
from datetime import datetime


def makeMazes(file, out):
    fl = "split/%s" % file
    mask = Mask.from_png(fl)
    grid = MaskedGrid(mask)
    loc = file[:-4]
    RecursiveBacktracker.on(grid)
    # rb = "out/recursivebacktracker/%s" % loc
    grid.to_png(cell_size=8, folder=out, name=loc)
    return


def main(sfile, sz):
    # invoke: $ python demo2.py "image.png" 80
    print("splitting image ...")
    split.main(sfile, sz)
    print("splits saved!")
    out = "mz/"
    if not os.path.exists(out):
        os.makedirs(out)
    print("making mazes ...")

    pool_size = 192
    pool = Pool(pool_size)
    for file in os.listdir("split/"):
        pool.apply_async(makeMazes, (file, out))
    pool.close()
    pool.join()

    print("mazes complete!")
    print("stitching segments ...")
    stitch.main("mz/")
    print("stitching complete!")
    return


if __name__ == "__main__":
    startTime = datetime.now()
    main(sys.argv[1], int(sys.argv[2]))
    print("Completed In : %s" % (datetime.now() - startTime))
