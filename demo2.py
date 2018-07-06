import os
import sys
import stitch
import split
from Mask import Mask
from MaskedGrid import MaskedGrid
# from BinaryTree import BinaryTree
# from Sidewinder import Sidewinder
from RecursiveBacktracker import RecursiveBacktracker


# invoke: $ python demo2.py "image.png" 100
# "off"
sfile = sys.argv[1]
# op = sys.argv[2] 
sz = int(sys.argv[2])


print("splitting image ...")
split.main(sfile, sz)
print("splits saved!")

out = "mz/"
if not os.path.exists(out):
    os.makedirs(out)

print("making mazes ...")
for file in os.listdir("split/"):
    fl = "split/%s" % file
    mask = Mask.from_png(fl)
    grid = MaskedGrid(mask)
    loc = file[:-4]
    RecursiveBacktracker.on(grid)
    # rb = "out/recursivebacktracker/%s" % loc
    img3 = grid.to_png(cell_size=4, folder=out, name=loc)

print("mazes complete!")

print("stitching segments ...")
stitch.main("mz/")
print("stitching complete!")


# if op == "on":
#     img3.show()

# BinaryTree.on(grid)
# bt = "out/binarytree/%s" % loc
# img = grid.to_png(cell_size=10, folder=bt)
# if op == "on":
#     img.show()

# grid3 = MaskedGrid(mask)
# Sidewinder.on(grid)
# sw = "out/sidewinder/%s" % loc
# img2 = grid.to_png(cell_size=10, folder=sw)
# if op == "on":
#     img2.show()

