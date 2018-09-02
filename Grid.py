from random import randrange
from Cell import Cell
from PIL import Image, ImageDraw
import uuid
import os

# THIS IS THE GRID CLASS ADAPTED TO PYTHON FROM
# FROM JAMIS BUCK'S MAZES FOR PROGRAMMERS RUBY CODE

# MY IMPORTANT ADDITION IS THE to_point_pairs() FUNCTION
# WHICH RETURN A LIST OF COORDINATES SO I CAN DRAW WITH
# OPENGL INSTEAD OF USING THE PIL IMAGE WHICH IS VERY SLOW

class Grid():

    def cell_at(self, row, col):
        # check if there is a cell at the provided row/col
        # see if row is in range
        if not (0 <= row <= self.rows - 1):
            # if not return None
            return None
        # see if col is in range
        if not (0 <= col <= self.columns - 1):
            # return none
            return None
        # print("row=%s, col=%s"%(row, col))
        # return the cell at the postion
        return self.grid[row][col]

    def set_cell(self, row, col, val):
        # set the position row col to cell
        self.grid[row][col] = val

    def __init__(self, rows, columns):
        # init the grid object with a number of rows and columns
        self.rows = rows
        self.columns = columns
        # call the prepare function
        self.grid = self.prep_grid()
        # set up the cells in the grid
        self.config_cells()

    def prep_grid(self):
        # Prepare the grid with a 2d for loop
        # go over every row and col and init a Cell object
        # for r in range(self.rows):
        #     for c in range(self.columns):
        #         Cell(r, c)
        # DO this in one line so we can return it all at once to the self.grid val
        return [[Cell(r, c) for c in range(self.columns)] for r in range(self.rows)]

    def config_cells(self):
        # for every cell (one at a time)
        for cell in self.each_cell():
            # print("config_cells: cell : %s" % cell)
            row = cell.row
            col = cell.column
            # set the neighbours, we define the getter and setters  
            # further down so that they use the 'within range' check 
            # at the top of the class. 
            # This lets us set None if we are on an edge.
            cell.north = self[row - 1, col]
            cell.south = self[row + 1, col]
            cell.east = self[row, col + 1]
            cell.west = self[row, col - 1]

    def each_cell(self):
        # this is a generator!
        # return each cell by looping over each row
        for row in self.each_row():
            for cell in row:
                # is there a vaild Cell?
                if isinstance(cell, Cell):
                    # yeild allows us to pass all the things
                    # without storing everything somewhere 
                    # and returning that
                    yield cell
                else:
                    # or skip it
                    pass

    def each_row(self):
        # generate each row from the grid
        for row in range(self.rows):
            yield self.grid[row]

    def rand_cell(self):
        # get a random row and col
        row = randrange(0, self.rows)
        col = randrange(0, self.columns)
        # return the cell at that position
        return self[row, col]

    def size(self):
        # get the size of the grid 
        return self.rows * self.columns

    def __getitem__(self, key):
        # redefined getter to use the cell_at function
        # so we can check position being requested
        return self.cell_at(*key)

    def __setitem__(self, key, val):
        # custom setter to add cells to grid pos
        self.set_cell(*key, val)

    def check_deadends(self):
        # check dead ends by looking for cell that only has one linked neighbour
        return [cell for cell in self.each_cell() if len(cell.links) == 1]

    def to_ascii(self):
        # print maze to ascii
        output = "+" + "---+" * self.columns + "\n"
        # for each row
        for row in self.each_row():
            # append
            top = "|"
            bottom = "+"
            # for each cell
            for cell in row:
                # append text
                body = "   "
                # is the cell linked to the east
                east_boundary = " " if cell.is_linked(cell.east) else "|"
                top += body + east_boundary
                # is the cell linked to the south
                south_boundary = "   " if cell.is_linked(cell.south) else "---"
                corner = "+"
                bottom += south_boundary + corner
            # join it all together
            output += top + "\n"
            output += bottom + "\n"
        # print the text to console
        print(output)

    def to_png(self, cell_size=10, folder="out", name="nm", save=True):
        # to png file
        #  pretty stright forward, draw lines by getting positions
        # and multiplying by desired sizes
        img_wid = cell_size * self.columns
        img_hei = cell_size * self.rows
        bg = (255, 255, 255)
        wall = (56, 50, 38)
        # wall = (255, 150, 138)
        img = Image.new("RGBA", (img_wid + 1, img_hei + 1), bg)
        draw = ImageDraw.Draw(img)

        # for cell in self.each_cell():
        #     x1 = cell.column * cell_size
        #     y1 = cell.row * cell_size
        #     x2 = (cell.column + 1) * cell_size
        #     y2 = (cell.row + 1) * cell_size
        #     box = cell.colour
        #     draw.rectangle([(x1, y1), (x2, y2)], fill=box)

        for cell in self.each_cell():
            x1 = cell.column * cell_size
            y1 = cell.row * cell_size
            x2 = (cell.column + 1) * cell_size
            y2 = (cell.row + 1) * cell_size

            half_cell = cell_size / 2

            # THIS IS MY OWN BIT TO CREATE AN ENTRANCE/EXIT TO THE LABYRINTH
            # THIS MAKES IT UNICURSAL!
            if cell.row == 0 and cell.column == 0:
                if cell.is_linked(cell.south):
                    draw.line((x1+half_cell,y1,x1+half_cell,y2), fill=wall, width=1)
                else:
                    draw.line((x1,y1+half_cell,x2,y1+half_cell), fill=wall, width=1)

            # BACK TO BUCK'S 
            if not cell.north:
                draw.line((x1, y1, x2, y1), fill=wall, width=1)
            if not cell.west:
                draw.line((x1, y1, x1, y2), fill=wall, width=1)
            if not cell.is_linked(cell.east):
                draw.line((x2, y1, x2, y2), fill=wall, width=1)
            if not cell.is_linked(cell.south):
                draw.line((x1, y2, x2, y2), fill=wall, width=1)

            # BACK TO ME
            # THIS SPILTS THE CHANNELS TO MAKE THEM UNICURSAL!
            if cell.is_linked(cell.east):
                draw.line((x1 + half_cell, y1 + half_cell, x2 + half_cell, y1 + half_cell), fill=wall, width=1)
            if cell.is_linked(cell.south):
                draw.line((x1 + half_cell, y1 + half_cell, x1 + half_cell, y2 + half_cell), fill=wall, width=1)
        if not os.path.exists(folder):
            os.makedirs(folder)
        if save:
            # save it
            img.save("{}/{}.png".format(folder, name), "PNG", optimize=True)
        # also return the image to whoever called it!
        return img


    # 
    # THIS IS MY FUNCTION TO WORK WITH MY GL SETUP INSTEAD OF
    # WRITING TO PNG FILE LIKE JAMIS BUCK DOES IN HIS RUBY CODE
    # 
    def to_point_pairs(self, cell_size=4, entrance=True):
        # This returns a list of points so we can draw to screen with 
        # open gl

        img_wid = cell_size * self.columns
        img_hei = cell_size * self.rows

        # empty list to store the points
        draw = []

        # for each cell
        for cell in self.each_cell():
            # work out the points
            x1 = cell.column * cell_size
            y1 = cell.row * cell_size
            x2 = (cell.column + 1) * cell_size
            y2 = (cell.row + 1) * cell_size
            half_cell = cell_size / 2

            # if first row or coloum
            if cell.row == 0 and cell.column == 0:
                # does it start horizontally or vertically
                if cell.is_linked(cell.south):
                    # draw the little line to join up to the edge
                    # and complete the labyrinth
                    # append the four points to the list as one element
                    draw.append((x1+half_cell,y1,x1+half_cell,y2))
                else:
                    draw.append((x1,y1+half_cell,x2,y1+half_cell))

            # check neighbours and join up the walls
            if not cell.north:
                draw.append((x1, y1, x2, y1))
            if not cell.west:
                draw.append((x1, y1, x1, y2))
            if not cell.is_linked(cell.east):
                draw.append((x2, y1, x2, y2))
            if not cell.is_linked(cell.south):
                draw.append((x1, y2, x2, y2))

            # THIS SPILTS THE CHANNELS TO MAKE THEM UNICURSAL!
            if cell.is_linked(cell.east):
                draw.append((x1 + half_cell, y1 + half_cell, x2 + half_cell, y1 + half_cell))
            if cell.is_linked(cell.south):
                draw.append((x1 + half_cell, y1 + half_cell, x1 + half_cell, y2 + half_cell))
        # return the list
        return draw



    def to_png_inset(self, cell_size=8, inset=0.25, folder="out", name="nm", save=True):
        # THIS INSETS A LITTLE, INTERESTING VARIATION ON THE TO PNG
        # BUT PRETTY MUCH THE SAME
        img_wid = cell_size * self.columns
        img_hei = cell_size * self.rows
        inset = cell_size * inset
        bg = (255, 255, 255)
        wall = (56, 50, 38)
        img = Image.new("RGBA", (img_wid + 1, img_hei + 1), bg)
        draw = ImageDraw.Draw(img)

        for cell in self.each_cell():
            x = cell.column * cell_size
            y = cell.row * cell_size
            x1 = x
            x4 = x + cell_size
            x2 = x1 + inset
            x3 = x4 - inset
            y1 = y
            y4 = y + cell_size
            y2 = y1 + inset
            y3 = y4 - inset
            quart_cell = cell_size / 4


            # MY ADDITIONS FOR ENTRANCE/EXIT
            if cell.row == 0 and cell.column == 0:
                if cell.is_linked(cell.south):
                    draw.line((x2+quart_cell,y2,x2+quart_cell,y3), fill=wall, width=int(cell_size/4))
                else:
                    draw.line((x2,y2+quart_cell,x3,y2+quart_cell), fill=wall, width=int(cell_size/4))

            if cell.is_linked(cell.north):
                draw.line((x2, y1, x2, y2), fill=wall, width=int(cell_size/4))
                draw.line((x3, y1, x3, y2), fill=wall, width=int(cell_size/4))
                draw.line((x2 + quart_cell, y1, x2 + quart_cell, y2 + quart_cell), fill=wall, width=int(cell_size/4))
            else:
                draw.line((x2, y2, x3, y2), fill=wall, width=int(cell_size/4))

            if cell.is_linked(cell.south):
                draw.line((x2, y3, x2, y4), fill=wall, width=int(cell_size/4))
                draw.line((x3, y3, x3, y4), fill=wall, width=int(cell_size/4))
                draw.line((x2 + quart_cell, y2 + quart_cell, x2 + quart_cell, y4), fill=wall, width=int(cell_size/4))
                
            else:
                draw.line((x2, y3, x3, y3), fill=wall, width=int(cell_size/4))

            if cell.is_linked(cell.west):
                draw.line((x1, y2, x2, y2), fill=wall, width=int(cell_size/4))
                draw.line((x1, y3, x2, y3), fill=wall, width=int(cell_size/4))
                draw.line((x1, y2 + quart_cell, x2 + quart_cell, y2 + quart_cell), fill=wall, width=int(cell_size/4))
            else:
                draw.line((x2, y2, x2, y3), fill=wall, width=int(cell_size/4))

            if cell.is_linked(cell.east):
                draw.line((x3, y2, x4, y2), fill=wall, width=int(cell_size/4))
                draw.line((x3, y3, x4, y3), fill=wall, width=int(cell_size/4))
                draw.line((x2 + quart_cell, y2 + quart_cell, x4, y2 + quart_cell), fill=wall, width=int(cell_size/4))
            else:
                draw.line((x3, y2, x3, y3), fill=wall, width=int(cell_size/4))

        if not os.path.exists(folder):
            os.makedirs(folder)
        if save:
            img.save("{}/{}.png".format(folder, name), "PNG", optimize=True)
        return img
