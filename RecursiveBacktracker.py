from Cell import Cell
from random import choice, randint


class RecursiveBacktracker():

    def on(grid):

        stack = []
        start = grid.cell_at(0, 0)
        stack.append(start)

        while len(stack) > 0:
            current = stack[-1]
            # add cell check for masking
            if isinstance(current, Cell):
                col = (255, 255, 255)
                current.set_colour(col)
                # print(current)
                neighs = []
                for n in current.neighbours():
                    if len(n.links) == 0:
                        neighs.append(n)
                if len(neighs) == 0:
                    stack.pop()
                else:
                    neighbour = choice(neighs)
                    current.link(neighbour, True)
                    stack.append(neighbour)
            else:
                stack.pop()
