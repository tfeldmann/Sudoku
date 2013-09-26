from constraint import *


class Sudoku(object):

    def __init__(self, grid):
        self.grid = grid
        self.size = int(len(grid) ** 0.5)
        self.block_size = int(self.size ** 0.5)

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
        for _y in range(0, self.block_size):
            for _x in range(0, self.block_size):
                block = []
                x = _x * self.block_size
                y = _y * self.block_size * self.size
                start = x + y
                for r in range(self.block_size):
                    block += self.grid[start:start + self.block_size]
                    start += self.size
                result.append(block)
        return result

    def solve(self):
        problem = Problem()

        for i, n in enumerate(self.grid):
            problem.addVariable(i, range(1, self.size + 1) if n == 0 else [n])

        _s = Sudoku(range(len(self.grid)))
        for row in _s.rows:
            problem.addConstraint(AllDifferentConstraint(), row)
        for col in _s.columns:
            problem.addConstraint(AllDifferentConstraint(), col)
        for block in _s.blocks:
            problem.addConstraint(AllDifferentConstraint(), block)

        solution = problem.getSolution()
        self.grid = solution.values()

    def __str__(self):
        result = ''
        number_width = len(str(self.size)) + 1
        block_count = int(self.size / self.block_size)
        block_width = block_count * number_width

        for y, row in enumerate(self.rows):
            if y % self.block_size == 0 and y > 0:
                # insert horizontal line
                result += "+-".join(["-" * block_width] * block_count) + "\n"
            for x, num in enumerate(row):
                if x % self.block_size == 0 and x > 0:
                    # insert vertical line
                    result += "| "
                # draw numbers
                result += str(num).ljust(number_width)
            result += "\n"
        return result

if __name__ == '__main__':
    hardest = [8, 0, 0, 0, 0, 0, 0, 0, 0,
               0, 0, 3, 6, 0, 0, 0, 0, 0,
               0, 7, 0, 0, 9, 0, 2, 0, 0,
               0, 5, 0, 0, 0, 7, 0, 0, 0,
               0, 0, 0, 0, 4, 5, 7, 0, 0,
               0, 0, 0, 1, 0, 0, 0, 3, 0,
               0, 0, 1, 0, 0, 0, 0, 6, 8,
               0, 0, 8, 5, 0, 0, 0, 1, 0,
               0, 9, 0, 0, 0, 0, 4, 0, 0]

    empty = [0] * 81

    s = Sudoku(hardest)
    s.solve()
    print(s)
