"""
A module for managing and solving sudokus of variable size
"""
import constraint


class Sudoku(object):

    """
    This class manages Sudoku grids of variable sizes.

    It allows for easy access to the individual rows, columns and blocks of
    the grid. Sudokus can be solved using constraint processing.
    """

    def __init__(self, grid):
        """
        The constructor expects a flat list as a grid, for example:

        >>> grid4x4 = [0, 1, 0, 0,
        ...            0, 0, 4, 0,
        ...            0, 0, 0, 0,
        ...            0, 0, 3, 0]
        >> Sudoku(grid4x4)

        Where zeros indicate an empty field.
        The grid's length must be a a square number.
        """
        self.grid = grid
        self.size = int(len(grid) ** 0.5)
        self.block_size = int(self.size ** 0.5)

        if self.size ** 2 != len(grid):
            raise ValueError('Expecting a square grid')

    @property
    def rows(self):
        """
        Generator expression for accessing the individual rows of the grid
        """
        for n in range(self.size):
            yield self.grid[n * self.size:self.size * (n + 1)]

    @property
    def columns(self):
        """
        Returns a generator for accessing the individual columns of the grid
        """
        for n in range(self.size):
            yield self.grid[n::self.size]

    @property
    def blocks(self):
        """
        Returns a generator for accessing the individual blocks of the grid
        """
        for _y in range(self.block_size):
            for _x in range(self.block_size):
                block = []
                x = _x * self.block_size
                y = _y * self.block_size * self.size
                start = x + y
                for r in range(self.block_size):
                    block += self.grid[start:start + self.block_size]
                    start += self.size
                yield block

    def solve(self):
        """
        Solves the sudoku.

        This will replace the empty cells in this sudoku with the solutions.
        """
        problem = constraint.Problem()
        all_different = constraint.AllDifferentConstraint()

        for i, n in enumerate(self.grid):
            problem.addVariable(i, range(1, self.size + 1) if n == 0 else [n])

        _s = Sudoku(range(len(self.grid)))
        for row in _s.rows:
            problem.addConstraint(all_different, row)
        for col in _s.columns:
            problem.addConstraint(all_different, col)
        for block in _s.blocks:
            problem.addConstraint(all_different, block)

        solution = problem.getSolution()
        if solution:
            self.grid = solution.values()
        else:
            raise ValueError('No solutions found')

    def __str__(self):
        """
        Shows the string representation of the sudoku grid.
        """
        result = ''
        number_width = len(str(self.size)) + 1
        block_count = int(self.size / self.block_size)
        block_width = block_count * number_width

        # Formatting has gotten bit complex because we need to handle grids of
        # variable size. As a result, numbers are often longer than one char.
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
    small = [0, 1, 0, 0,
             0, 0, 4, 0,
             0, 0, 0, 0,
             0, 2, 3, 0]

    hardest = [8, 0, 0, 0, 0, 0, 0, 0, 0,
               0, 0, 3, 6, 0, 0, 0, 0, 0,
               0, 7, 0, 0, 9, 0, 2, 0, 0,
               0, 5, 0, 0, 0, 7, 0, 0, 0,
               0, 0, 0, 0, 4, 5, 7, 0, 0,
               0, 0, 0, 1, 0, 0, 0, 3, 0,
               0, 0, 1, 0, 0, 0, 0, 6, 8,
               0, 0, 8, 5, 0, 0, 0, 1, 0,
               0, 9, 0, 0, 0, 0, 4, 0, 0]

    empty_normal = [0] * (9 ** 2)
    empty_big = [0] * (16 ** 2)

    s = Sudoku(hardest)
    s.solve()

    print(s)
