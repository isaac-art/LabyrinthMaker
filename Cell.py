class Cell():

    def __init__(self, row, column):
        self.row = row
        self.column = column
        self.links = {}
        self.north = None
        self.south = None
        self.east = None
        self.west = None

    def link(self, cell, bidi=True):
        if not isinstance(cell, Cell):
            raise ValueError("must link to cell")
        self.links[cell] = True
        if bidi:
            cell.link(self, bidi=False)
        return self

    def unlink(self, cell, bidi=True):
        if cell is None:
            raise ValueError("trying to unlink none link")
        elif not isinstance(cell, Cell):
            raise ValueError("must unlink to cell")
        self.links[cell] = False
        if bidi:
            cell.unlink(self, bidi=False)
        return self

    def links(self):
        return list(self.links.keys())

    def is_linked(self, cell):
        if isinstance(cell, Cell):
            return cell in self.links
        elif cell is None:
            return False

    def neighbours(self):
        nlist = []
        if self.north:
            nlist.append(self.north)
        if self.south:
            nlist.append(self.south)
        if self.east:
            nlist.append(self.east)
        if self.west:
            nlist.append(self.west)
        return nlist
