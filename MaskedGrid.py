from Grid import Grid
from Cell import Cell
# import numpy as np


# THIS IS THE MASKEDGRID CLASS ADAPTED TO PYTHON FROM
# FROM JAMIS BUCK'S MAZES FOR PROGRAMMERS RUBY CODE

# I HAVE TWEAKED THE PREP_GRID SO THAT IT APPENDS CELLS AND NONE 
# NOT JUST THE CELLS. THIS IS SO WE CAN BE EXPLICIT ABOUT SOMETHING
# NOT BEING THERE

# a class that inherits the Grid Class
class MaskedGrid(Grid):

    def __init__(self, mask):
        self.mask = mask
        # print(mask)
        # init the super class with the mask info
        super().__init__(mask.rows, mask.columns)


    def prep_grid(self):
        # OVERRIDES THE PREP GRID IN THE SUPER CLASS
        g = []
        # print("rows: %s, cols: %s" % (self.rows, self.columns))
        for r in range(self.rows):
            l = []
            for c in range(self.columns):
                # THERE IS A VALID POSTION
                if self.mask.cell_at(r, c):
                    # print("cell")

                    # SO WE INIT AND APPEND A CELL IN THIS POSITION
                    l.append(Cell(r, c))
                else:
                    # print("mask")

                    # THIS IS MASKED SO APPEND A NONE SO WHEN WE CHECK IT
                    # WE CAN CHECK AGAINST IT BEING NONE
                    # RATHER THAN IT JUST NOT BEING THERE
                    l.append(None)


                # print(l)
            g.append(l)

        # using numpy to check we are getting what is expected
        # print(np.matrix(g))
        # print(np.shape(g))

        # RETURN THE GRID
        return g 


    def rand_cell(self):
        # OVERRIDES THE RANDOM CELL IN THE SUPER CLASS
        # we ask the mask to get us a vaild position that
        # hasnt been masked
        row, col = self.mask.rand_loc()
        return self[row, col]

    def size(self):
        # OVERRIDES THE SIZE IN THE SUPER CLASS
        # get the size from the mask not the grid
        return self.mask.rows * self.mask.columns
