import unittest
import random

from minesweeper.components import Board, Cell


class TestBoard(unittest.TestCase):
    @staticmethod
    def get_adjacent_cells(x, y):
        return [
            (x - 1, y),  # left
            (x + 1, y),  # right
            (x, y - 1),  # top
            (x, y + 1),  # bottom
            (x - 1, y - 1),  # top left
            (x + 1, y - 1),  # top right
            (x - 1, y + 1),  # bottom left
            (x + 1, y + 1)  # bottom right
        ]

    def test_init(self):
        size = 3
        num_holes = 2
        board = Board(size, num_holes)

        self.assertEqual(board.height, size)
        self.assertEqual(board.width, size)
        self.assertEqual(len(board.black_holes), num_holes)
        self.assertEqual(board.debug, False)

        board = Board(size, num_holes, debug=True)
        self.assertEqual(board.debug, True)

        self.assertRaises(ValueError, Board, 0, num_holes)
        self.assertRaises(ValueError, Board, size, -1)
        self.assertRaises(ValueError, Board, size, size**2+1)

    def test_generate_black_holes(self):
        board = Board(n=5, k=0, debug=True)
        num_holes = 8
        board.black_holes = board.generate_black_holes(num_holes)
        board.calculate_adjacent_holes()
        self.assertEqual(len(board.black_holes), num_holes)

        for cell in board.black_holes:
            self.assertTrue(board.cells[cell].is_black_hole, True)

        for cell in board.cells.keys():
            if cell not in board.black_holes:
                self.assertFalse(board.cells[cell].is_black_hole)

    def test_calculate_adjacent_holes(self):
        for _ in range(100):
            size = random.randint(1, 50)
            num_holes = random.randint(0, size**2)

            board = Board(n=size, k=num_holes, debug=False)

            for x in range(size):
                for y in range(size):
                    if (x, y) in board.black_holes:
                        continue
                    if board.cells.get((x, y), None) is None:
                        calc = 0
                    else:
                        calc = board.cells[(x, y)].adjacent_black_holes

                    target = sum([1 if cell in board.cells and board.cells[cell].is_black_hole
                                  else 0 for cell in self.get_adjacent_cells(x, y)])

                    self.assertEqual(calc, target)

    def test_reveal(self):
        size = 5
        board = Board(n=size, k=0, debug=True)
        board.black_holes = [(1, 1), (1, 2), (2, 3), (3, 3)]
        board.cells = {coords: Cell(*coords, is_black_hole=True) for coords in board.black_holes}
        board.calculate_adjacent_holes()
        print(board)
        """"
            | 1 | 2 | 2 | 1 | 0 |
            | 1 | H | H | 2 | 1 |
            | 1 | 2 | 4 | H | 2 |
            | 0 | 0 | 2 | H | 2 |
            | 0 | 0 | 1 | 1 | 1 |
        """

        revealed = board.reveal(1, 3)
        print(board)
        """
            | 1 | 2 | 2 | 1 | 0 |
            | 1 | H | H |2R | 1 |
            | 1 | 2 | 4 | H | 2 |
            | 0 | 0 | 2 | H | 2 |
            | 0 | 0 | 1 | 1 | 1 |
        """
        self.assertEqual(revealed, 1)
        self.assertEqual(board.cells[(1, 3)].is_revealed, True)
        self.assertEqual(board.cells[(1, 3)].print(debug=True)[-1], 'R')

        for cell in ((0, 2), (0, 3), (0, 4), (1, 4)):
            if board.cells.get(cell, None) is None:
                continue
            self.assertFalse(board.cells[cell].is_revealed)
            self.assertFalse(board.cells[cell].print(debug=True)[-1] == 'R')

        revealed = board.reveal(1, 3)
        self.assertEqual(revealed, 0)

        revealed = board.reveal(1, 2)
        self.assertEqual(revealed, -1)

        board.reveal(3, 1)
        print(board)
        """
            | 1 | 2 | 2 | 1 | 0 |
            | 1 | H | H |2R | 1 |
            |1R |2R |4R | H | 2 |
            |0R |0R |2R | H | 2 |
            |0R |0R |1R | 1 | 1 |
        """
        cells = [(2, 0), (2, 1), (2, 2), (3, 0), (3, 1), (3, 2), (4, 0), (4, 1), (4, 2)]
        for cell in cells:
            self.assertTrue(board.cells[cell].is_revealed)
            self.assertEqual(board.cells[cell].print(debug=True)[-1], 'R')

        self.assertEqual(board.reveal(-1, -1), -2)
        self.assertEqual(board.reveal(size, 1), -2)
        self.assertEqual(board.reveal(1, size), -2)
        self.assertEqual(board.reveal(1, size**size), -2)

        for _ in range(100):
            size = random.randint(1, 50)
            x, y = random.randint(0, size-1), random.randint(0, size-1)

            board = Board(n=size, k=0, debug=False)
            board.reveal(x, y)

            for x in range(size):
                for y in range(size):
                    self.assertTrue(board.cells[(x, y)].is_revealed)

    def test_debug_mode(self):
        board = Board(n=5, k=0)
        self.assertFalse(board.debug)

        board.debug_mode()
        self.assertTrue(board.debug)

    def test_disable_debug_mode(self):
        board = Board(n=5, k=0)
        board.debug_mode()
        self.assertTrue(board.debug)

        board.disable_debug_mode()
        self.assertFalse(board.debug)

    def test__str__(self):
        board = Board(n=5, k=2)
        board.debug_mode()
        self.assertTrue(str(board) != '')

        board.disable_debug_mode()
        self.assertTrue(str(board) != '')

        board = Board(n=5, k=0, debug=True)
        self.assertTrue(str(board) != '')

        board = Board(n=5, k=0, debug=False)
        self.assertTrue(str(board) != '')
