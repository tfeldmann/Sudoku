from constraint import *


class Sudoku(object):
    def __init__(self, given):
        pass

    def solve(self):
        pass

    def row(self, y):
        pass

    def __str__(self):
        pass


def print_sudoku(sudoku):
    for i in range(size):
        print sudoku[i * size: i * size + size]

if __name__ == '__main__':
    size = 9
    sudoku = [i for i in range(size ** 2)]

    # todo: blocks
    # i = 3
    # print sudoku[i*3:i*3+3] + sudoku[i*3+9:i*3+3+9] + sudoku[i*3+18:i*3+3+18]
    # exit()

    problem = Problem()
    problem.addVariables(sudoku, range(1, size + 1))

    # apply "all different"-constraints on rows and columns
    for i in xrange(size):
        row = sudoku[i * size: size * (i + 1)]
        problem.addConstraint(AllDifferentConstraint(), row)
        col = sudoku[i::size]
        problem.addConstraint(AllDifferentConstraint(), col)

    # apply "all different"-constraint on blocks

    solution = problem.getSolutionIter()
    print_sudoku(solution.next().values())
