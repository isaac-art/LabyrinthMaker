import sys
from Grid import Grid
from BinaryTree import BinaryTree
from Sidewinder import Sidewinder


op = sys.argv[1]

grid = Grid(10, 10)
BinaryTree.on(grid)
grid.to_ascii()
# img = grid.to_png(cell_size=10, folder="out/binarytree")
# img.show()


grid2 = Grid(10, 10)
Sidewinder.on(grid2)
grid2.to_ascii()
# print("deadends:%s" % len(grid2.check_deadends()))
img2 = grid2.to_png(cell_size=30, folder="out/sidewinder")
if op == "on":
    img2.show()
