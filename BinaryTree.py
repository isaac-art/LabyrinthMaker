from random import choice
from Grid import Grid

class BinaryTree():

    def on(grid):
        for cell in grid.each_cell():
            nei = []
            if cell.north:
                nei.append(cell.north)
            if cell.east:
                nei.append(cell.east)
            if len(nei) > 0:
                neib = choice(nei)
                cell.link(neib)
