from Grid import Grid
from Cell import Cell
# import numpy as np

class MaskedGrid(Grid):

    def __init__(self, mask):
        self.mask = mask
        # print(mask)
        super().__init__(mask.rows, mask.columns)

    def prep_grid(self):
        g = []
        # print("rows: %s, cols: %s" % (self.rows, self.columns))
        for r in range(self.rows):
            l = []
            for c in range(self.columns):
                if self.mask.cell_at(r, c):
                    # print("cell")
                    l.append(Cell(r, c))
                else:
                    # print("mask")
                    l.append(None)
                # print(l)
            g.append(l)
        # print(np.matrix(g))
        # print(np.shape(g))
        return g 

    def rand_cell(self):
        row, col = self.mask.rand_loc()
        return self[row, col]

    def size(self):
        return self.mask.rows * self.mask.columns
