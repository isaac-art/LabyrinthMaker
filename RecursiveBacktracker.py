from Cell import Cell
from random import choice, randint


class RecursiveBacktracker():

    def on(grid):
        stack = []
        start = grid.cell_at(0, 0)
        stack.append(start)

        while len(stack) > 0:
            current = stack[-1]
            if isinstance(current, Cell):
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