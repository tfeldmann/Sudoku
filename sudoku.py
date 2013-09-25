from constraint import *


class Sudoku(object):

    def __init__(self, grid):
        self.grid = grid
        self.size = int(len(grid) ** 0.5)

        if self.size ** 2 != len(grid):
            raise ValueError("Expecting a square grid")

    @property
    def rows(self):
        return [self.grid[n * self.size:self.size * (n + 1)]
                for n in range(self.size)]

    @property
    def columns(self):
        return [self.grid[n::self.size] for n in range(self.size)]

    @property
    def blocks(self):
        result = []
        block_size = int(self.size ** 0.5)

        for _y in range(0, block_size):
            for _x in range(0, block_size):
                block = []
                x = _x * block_size
                y = _y * block_size * self.size
                start = x + y
                for r in range(block_size):
                    block += self.grid[start:start+block_size]
                    start += self.size
                result.append(block)
        return result

    def solve(self):
        pass

    def __str__(self):
        pass


def print_sudoku(sudoku):
    for i in range(size):
        print sudoku[i * size: i * size + size]

if __name__ == '__main__':

    s = Sudoku([1, 0, 0, 0, 0, 0, 0, 0, 0,
                0, 0, 0, 0, 0, 0, 0, 0, 0,
                3, 0, 0, 0, 0, 0, 0, 0, 0,
                0, 0, 0, 0, 0, 0, 0, 0, 0,
                4, 0, 0, 0, 0, 0, 0, 0, 0,
                0, 0, 0, 0, 0, 0, 0, 0, 0,
                5, 0, 0, 0, 0, 0, 0, 0, 0,
                0, 0, 0, 0, 0, 0, 0, 0, 0,
                6, 0, 0, 0, 0, 0, 0, 0, 0])

    for row in s.rows:
        print row

    for col in s.columns:
        print col

    size = 9
    sudoku = [i for i in range(size ** 2)]

    # todo: blocks
    # i = 3
    # print sudoku[i*3:i*3+3] + sudoku[i*3+9:i*3+3+9] + sudoku[i*3+18:i*3+3+18]
    exit()

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
