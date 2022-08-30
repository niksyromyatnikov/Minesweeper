import random
from minesweeper.components import Cell
from minesweeper.components import unraveled_print


class Board:
    def __init__(self, n: int, k: int, debug: bool = False):
        """
        Initialize a board with n rows and columns and k black holes.
        :param n: columns and rows
        :param k: number of black holes
        :param debug: enable debug mode, False by default
        """
        if n < 1:
            raise ValueError('board dimension must be greater than 0')
        if k < 0 or k > n ** 2:
            raise ValueError('number of black holes must be between 0 and board size')
        self.height = n
        self.width = n
        self.debug = debug
        self.cells = {}

        self.black_holes = self.generate_black_holes(k)
        self.calculate_adjacent_holes()

    def generate_black_holes(self, k: int) -> list:
        """
        Generate k black holes in the board.
        :param k: number of black holes
        :return: list of black holes coordinates
        """
        cells = [i for i in range(self.height * self.width)]

        random.shuffle(cells)
        black_holes = []

        for i in cells[:k]:
            x = i // self.width
            y = i % self.width
            black_holes.append((x, y))
            self.cells[(x, y)] = Cell(x, y, True)

        if self.debug:
            print(f'Black holes: {sorted(black_holes)}')

        return black_holes

    def calculate_adjacent_holes(self):
        """
        Calculate the number of adjacent black holes for each cell.
        """
        for x, y in self.black_holes:
            for adjacent_x, adjacent_y in get_adjacent_cells(x, y):

                is_black_hole = self.cells[(adjacent_x, adjacent_y)].is_black_hole if (adjacent_x, adjacent_y) \
                                                                                      in self.cells else False

                if 0 <= adjacent_x < self.height and 0 <= adjacent_y < self.width and \
                        not is_black_hole:

                    if self.cells.get((adjacent_x, adjacent_y), None) is None:
                        self.cells[(adjacent_x, adjacent_y)] = Cell(adjacent_x, adjacent_y)

                    self.cells[(adjacent_x, adjacent_y)].adjacent_black_holes += 1

    def reveal(self, x, y) -> int:
        """
        Reveal a cell in the board by its coordinates and it`s adjacent cells if the cell has no adjacent black holes.
        :param x: x coordinate of the cell
        :param y: y coordinate of the cell
        :return: number of revealed cells or -1 if the cell is a black hole or 0 if the cell is already revealed or -2
        if the cell is outside the board.
        """
        if x < 0 or x >= self.height or y < 0 or y >= self.width:
            print('Coordinates out of bounds!')
            return -2

        if self.debug:
            print(f'Revealing cell ({x}, {y})')

        if self.cells.get((x, y), None) is not None:
            if self.cells[(x, y)].is_revealed:
                return 0
            if self.cells[(x, y)].is_black_hole:
                return -1

        revealed = 0
        queue = [(x, y)]

        while queue:
            coords = queue.pop(0)

            cell_exists = self.cells.get(coords, None) is not None
            if not cell_exists:
                self.cells[coords] = Cell(*coords)

            if self.cells[coords].is_revealed or self.cells[coords].is_black_hole:
                continue

            self.cells[coords].is_revealed = True
            revealed += 1

            if self.debug:
                print(f'Revealed cell {coords} with {self.cells[coords].adjacent_black_holes} adjacent black holes')

            if self.cells[coords].adjacent_black_holes > 0:
                continue

            x1, y1 = coords

            for adjacent_x, adjacent_y in get_adjacent_cells(x1, y1):
                if 0 <= adjacent_x < self.height and 0 <= adjacent_y < self.width:
                    queue.append((adjacent_x, adjacent_y))

        return revealed

    def debug_mode(self):
        """
        Enable debug mode.
        """
        self.debug = True

    def disable_debug_mode(self):
        """
        Disable debug mode.
        """
        self.debug = False

    def __str__(self):
        """
        Return a string representation of the board.
        """

        def get_cell_value(x1: int, y1: int):
            if self.cells.get((x1, y1), None) is not None:
                return self.cells[(x1, y1)].print(self.debug)
            return unraveled_print if not self.debug else '0'

        output = f'Board({self.height}, {self.width}):\n'

        output += '{0:^3s} |'.format('x/y')
        for y in range(self.width):
            output += '{0:^3s}'.format(str(y)) + '|'
        output += '\n'

        for x in range(self.height):
            output += '{0:^3s} |'.format(str(x))
            for y in range(self.width):
                output += '{0:^3s}'.format(get_cell_value(x, y)) + '|'
            output += '\n'

        return output

    def __repr__(self):
        """
        Return a string representation of the board.
        """
        return self.__str__()


def get_adjacent_cells(x, y) -> tuple:
    """
    Get the adjacent cells of a cell.
    :param x: x coordinate of the cell
    :param y: y coordinate of the cell
    :return: tuple of adjacent cells
    """
    return (
        (x - 1, y),  # top
        (x + 1, y),  # bottom
        (x, y - 1),  # left
        (x, y + 1),  # right
        (x - 1, y - 1),  # top left
        (x - 1, y + 1),  # top right
        (x + 1, y - 1),  # bottom left
        (x + 1, y + 1))  # bottom right
