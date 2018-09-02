from Cell import Cell
from random import choice, randint


# THIS IS THE RECURSIVE BACKTRACKER WHICH MOVES THROUGH 
# THE GRID WE GIVE IT AND JOINS UP ALL OUR VALID UNMASKED CELLS

# I CHOSE THE RECURSIVE BACKTRACKER OVER OTHER MAZE
# ALGORITHMS AS IT WILL ALWAYS RETURN ORTHOGANAL/PERFECT(no loops) PATHS.

# THIS IS VERY IMPORTANT SO THAT I CAN ADAPT IT INTO A UNICURSAL
# LABYRINTH WHEN DRAWING. UNICURSAL LABYRINTHS CAN ONLY BE MADE
# FROM A PERFECT MAZE!

class RecursiveBacktracker():

    def on(grid):
        # create empty list
        stack = []
        # start in the top corner
        # alternatively use random position function
        # it doesnt really matter
        start = grid.cell_at(0, 0)
        stack.append(start)

        # is there something in the list?
        while len(stack) > 0:
            # get the first thing
            current = stack[-1]

            # add cell check for masking
            # we need it to be a valid cell
            if isinstance(current, Cell):
                # here we can play with setting the colors
                # but i have settled on it being the same 
                # everywhere

                # it is useful if you want to colour in and 
                # you can visualize the paths that the
                # recursive backtracker took.
                col = (255, 255, 255)
                current.set_colour(col)
                # print(current)

                # create empty list 
                neighs = []

                # loop over neighbours
                for n in current.neighbours():
                    # does this neighbour have any links?
                    if len(n.links) == 0:
                        # add it to the list
                        neighs.append(n)

                # do we have nothing in the list?
                if len(neighs) == 0:
                    # jump up
                    stack.pop()
                else:
                    # or, pick a random neighbour cell
                    neighbour = choice(neighs)
                    # link this cell and neighbour together
                    # in both directions
                    current.link(neighbour, True)
                    # add the neighbour to the stack 
                    stack.append(neighbour)
            else:
                # jump up
                stack.pop()
