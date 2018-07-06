from random import randrange
from Cell import Cell
from PIL import Image, ImageDraw
import uuid
import os


class Grid():

    def cell_at(self, row, col):
        if not (0 <= row <= self.rows - 1):
            return None
        if not (0 <= col <= self.columns - 1):
            return None
        # print("row=%s, col=%s"%(row, col))
        return self.grid[row][col]

    def set_cell(self, row, col, val):
        self.grid[row][col] = val

    def __init__(self, rows, columns):
        self.rows = rows
        self.columns = columns
        self.grid = self.prep_grid()
        self.config_cells()

    def prep_grid(self):
        return [[Cell(r, c) for c in range(self.columns)] for r in range(self.rows)]

    def config_cells(self):
        for cell in self.each_cell():
            # print("config_cells: cell : %s" % cell)
            row = cell.row
            col = cell.column
            cell.north = self[row - 1, col]
            cell.south = self[row + 1, col]
            cell.east = self[row, col + 1]
            cell.west = self[row, col - 1]

    def each_cell(self):
        for row in self.each_row():
            for cell in row:
                if isinstance(cell, Cell):
                    yield cell
                else:
                    pass

    def each_row(self):
        for row in range(self.rows):
            yield self.grid[row]

    def rand_cell(self):
        row = randrange(0, self.rows)
        col = randrange(0, self.columns)
        return self[row, col]

    def size(self):
        return self.rows * self.columns

    def __getitem__(self, key):
        return self.cell_at(*key)

    def __setitem__(self, key, val):
        self.set_cell(*key, val)

    def check_deadends(self):
        return [cell for cell in self.each_cell() if len(cell.links) == 1]

    def to_ascii(self):
        output = "+" + "---+" * self.columns + "\n"
        for row in self.each_row():
            top = "|"
            bottom = "+"
            for cell in row:
                body = "   "
                east_boundary = " " if cell.is_linked(cell.east) else "|"
                top += body + east_boundary
                south_boundary = "   " if cell.is_linked(cell.south) else "---"
                corner = "+"
                bottom += south_boundary + corner
            output += top + "\n"
            output += bottom + "\n"
        print(output)

    def to_png(self, cell_size=10, folder="out", name="nm"):
        img_wid = cell_size * self.columns
        img_hei = cell_size * self.rows
        bg = (255, 255, 255)
        wall = (0, 0, 0)
        img = Image.new("RGBA", (img_wid + 1, img_hei + 1), bg)
        draw = ImageDraw.Draw(img)

        for cell in self.each_cell():
            x1 = cell.column * cell_size
            y1 = cell.row * cell_size
            x2 = (cell.column + 1) * cell_size
            y2 = (cell.row + 1) * cell_size

            if not cell.north:
                draw.line((x1, y1, x2, y1), fill=wall, width=int(cell_size/4))
            if not cell.west:
                draw.line((x1, y1, x1, y2), fill=wall, width=int(cell_size/4))
            if not cell.is_linked(cell.east):
                draw.line((x2, y1, x2, y2), fill=wall, width=int(cell_size/4))
            if not cell.is_linked(cell.south):
                draw.line((x1, y2, x2, y2), fill=wall, width=int(cell_size/4))

            half_cell = cell_size / 2
            if cell.is_linked(cell.east):
                draw.line((x1 + half_cell, y1 + half_cell, x2 + half_cell, y1 + half_cell), fill=wall, width=int(cell_size/4))
            if cell.is_linked(cell.south):
                draw.line((x1 + half_cell, y1 + half_cell, x1 + half_cell, y2 + half_cell), fill=wall, width=int(cell_size/4))
            # Originally:
            # if not cell.north:
            #     draw.line((x1, y1, x2, y1), fill=wall, width=1)
            # if not cell.west:
            #     draw.line((x1, y1, x1, y2), fill=wall, width=1)
            # if not cell.is_linked(cell.east):
            #     draw.line((x2, y1, x2, y2), fill=wall, width=1)
            # if not cell.is_linked(cell.south):
            #     draw.line((x1, y2, x2, y2), fill=wall, width=1)

        if not os.path.exists(folder):
            os.makedirs(folder)
        img.save("{}/{}.png".format(folder, name), "PNG", optimize=True)
        return img
