# THIS IS THE CELL CLASS
# ADAPTED FROM JAMIS BUCK'S MAZES FOR PROGRAMMERS RUBY CODE

class Cell():

    def __init__(self, row, column):
        # init the object with row and column
        self.row = row
        self.column = column
        # the links is initially empty
        self.links = {}
        # there surrounding is unknown
        self.north = None
        self.south = None
        self.east = None
        self.west = None
        # i decided on the colour being the same for all cells
        # so this doesnt change
        self.colour = (255, 255, 255)

    def set_colour(self, col):
        # function to set the colour of this cell
        self.colour = col

    def link(self, cell, bidi=True):
        # link this cell to the one provided
        # by adding it to the links list
        self.links[cell] = True
        # and also add to the links list of the other cell
        if bidi:
            cell.link(self, bidi=False)
        # return this object
        return self

    def unlink(self, cell, bidi=True):
        # remove this provided cell from the links list
        self.links[cell] = False
        # and remove this cell from the provided cells list
        if bidi:
            cell.unlink(self, bidi=False)
        # return this object
        return self

    def links(self):
        # return a list of the cells linked to
        return list(self.links.keys())

    def is_linked(self, cell):
        # check if we have been sent a valid cell object
        if isinstance(cell, Cell):
            # return the cell that matches if in links
            return cell in self.links
        elif cell is None:
            # or return false
            return False

    def neighbours(self):
        # create an empty list for neighbours
        nlist = []
        # for each direction see if there is anything set
        if self.north:
            # if so add to the list
            nlist.append(self.north)
        if self.south:
            nlist.append(self.south)
        if self.east:
            nlist.append(self.east)
        if self.west:
            nlist.append(self.west)
        # return the list of neighbours
        return nlist
