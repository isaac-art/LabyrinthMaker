from random import randrange
from PIL import Image


class Mask():

    def cell_at(self, row, col):
        if not (0 <= row <= self.rows - 1):
            return False
        if not (0 <= col <= self.columns - 1):
            return False
        # print(self.bits[row, col])
        return self.bits[row, col]

    def set_cell(self, row, col, val):
        self.bits[row, col] = val

    def __init__(self, rows, columns):
        self.rows = rows
        self.columns = columns
        self.bits = dict( ((r, c), True) for c in range(self.columns) for r in range(self.rows))
        # print(self.bits)

    def __getitem__(self, key):
        return self.cell_at(*key)

    def __setitem__(self, key, val):
        self.set_cell(*key, val)

    def count(self):
        count = 0
        for row in range(self.rows):
            for column in range(self.columns):
                if self.bits[row, column]:
                    count += 1
        return count

    def rand_loc(self):
        a = True
        while a:
            row = randrange(0, self.rows)
            col = randrange(0, self.columns)
            if self.bits[row, col]:
                a = False
                return row, col

    def from_png(file):
        img = Image.open(file)
        pix = img.load()
        width, height = img.size
        mask = Mask(height, width)

        for r in range(mask.rows):
            for c in range(mask.columns):
                # print(pix[c,r])
                # if (c, r) == (0, 0):
                #     mask[r, c] = True
                if pix[c, r] == (0, 0, 0, 255) or pix[c, r] == (0, 0, 0) or pix[c, r] == 0:
                    # print("False")
                    mask[r, c] = False
                else:
                    # print("True")
                    mask[r, c] = True
        return mask
