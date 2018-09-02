from random import randrange
from PIL import Image

# THIS IS THE MASK CLASS ADAPTED TO PYTHON FROM
# FROM JAMIS BUCK'S MAZES FOR PROGRAMMERS RUBY CODE

# I HAVE ADDED THE from_img_data() FUNCTION SO WE CAN 
# USE CAMERA STREAMS NOT LOAD FROM FILES

class Mask():

    # custom getter, see __getitem__()
    def cell_at(self, row, col):
        # are we in range?
        if not (0 <= row <= self.rows - 1):
            # no
            return False
        if not (0 <= col <= self.columns - 1):
            return False
        # print(self.bits[row, col])
        # if yes return the 
        return self.bits[row, col]

    # custom setter, see __setitem__()
    def set_cell(self, row, col, val):
        self.bits[row, col] = val

    def __init__(self, rows, columns):
        # init the mask to size
        self.rows = rows
        self.columns = columns

        # a dictionary of positions and Booleans
        # we look at positions and see if they are valid or not for a cell.
        # We store them like this so we can look up any at any point 
        # rather than in a list and have to do them all in the same order every time
        self.bits = dict( ((r, c), True) for c in range(self.columns) for r in range(self.rows))
        # print(self.bits)

    def __getitem__(self, key):
        # custom getter to check position truth
        return self.cell_at(*key)

    def __setitem__(self, key, val):
        # custom setter to set position truth
        self.set_cell(*key, val)

    def count(self):
        # This counts how many cells are available
        # to be used (how many positions are true)
        count = 0
        for row in range(self.rows):
            for column in range(self.columns):
                if self.bits[row, column]:
                    count += 1
        return count

    def rand_loc(self):
        # get a random location (usually for starting position)
        a = True
        while a:
            row = randrange(0, self.rows)
            col = randrange(0, self.columns)
            # only return when in a valid cell
            # not in a masked postion
            if self.bits[row, col]:
                a = False
                # retun a tuple 
                return row, col

    # 
    # MY ADDITION 
    # THIS ALLOWS ME TO JUST SEND IN THE IMAGE DATA
    # SO WE CAN USE A STREAM FROM A CAMERA 
    # RATHER THAN LOADING FROM AN IMAGE FILE 
    # 
    def from_img_data(img):
        # take the provided image
        pix = img.load()
        width, height = img.size
        # make a Mask Object 
        mask = Mask(height, width)
        # for every row and col 
        # IMPORTANT: EXCEPT THE FIRST AND LAST COUPLE OF ROWS/COLS
        # THIS STOPS THE MAZE FAILING IF IT IS MASKED IN THE TOP CORNER
        for r in range(1, mask.rows - 1):
            for c in range(1, mask.columns - 1):
                # print(pix[c,r])
                # if (c, r) == (0, 0):
                #     mask[r, c] = True

                # CHECK THE COLOR AT THIS POSTION
                if pix[c, r] == (0, 0, 0, 255) or pix[c, r] == (0, 0, 0) or pix[c, r] == 0:
                    # print("False")
                    # NO CELL HERE
                    mask[r, c] = False
                else:
                    # print("True")
                    # YES CELL HERE!
                    mask[r, c] = True

        return mask
    # 
    # 

    def from_png(file):
        # MAKE A MASK FROM PNG
        # open the image with PIL
        img = Image.open(file)
        # load the pixels from the image object
        pix = img.load()
        # get the size
        width, height = img.size
        # make a Mask Object with this info
        mask = Mask(height, width)
        # for each row and coloum
        for r in range(mask.rows):
            for c in range(mask.columns):
                # print(pix[c,r])
                # if (c, r) == (0, 0):
                #     mask[r, c] = True

                # LOOK at the pixel colour to see if it is black
                if pix[c, r] == (0, 0, 0, 255) or pix[c, r] == (0, 0, 0) or pix[c, r] == 0:
                    # print("False")

                    # it is so the mask position is false
                    # no cell will be active here
                    mask[r, c] = False
                else:
                    # print("True")

                    # it is white so a cell can be here
                    mask[r, c] = True
        # return the mask to whoever called it
        return mask
