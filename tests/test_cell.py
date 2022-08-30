import unittest
from minesweeper.components import Cell


class TestCell(unittest.TestCase):
    def test_init(self):
        cell = Cell(x=1, y=1)
        self.assertEqual(cell.x, 1)
        self.assertEqual(cell.y, 1)
        self.assertFalse(cell.is_black_hole)
        self.assertFalse(cell.is_revealed)
        self.assertEqual(cell.adjacent_black_holes, 0)

        cell = Cell(x=1, y=1, is_black_hole=True)
        self.assertTrue(cell.is_black_hole)
        self.assertFalse(cell.is_revealed)
        self.assertEqual(cell.adjacent_black_holes, 0)

        cell = Cell(x=1, y=1, is_revealed=True)
        self.assertFalse(cell.is_black_hole)
        self.assertTrue(cell.is_revealed)
        self.assertEqual(cell.adjacent_black_holes, 0)

        cell = Cell(x=1, y=1, adjacent_black_holes=1)
        self.assertFalse(cell.is_black_hole)
        self.assertFalse(cell.is_revealed)
        self.assertEqual(cell.adjacent_black_holes, 1)

    def test_print(self):
        cell = Cell(x=1, y=1)
        self.assertEqual(cell.print(), '*')

        cell = Cell(x=1, y=1, is_black_hole=True)
        self.assertEqual(cell.print(), '*')

        cell = Cell(x=1, y=1, adjacent_black_holes=1)
        self.assertEqual(cell.print(), '*')

        cell = Cell(x=1, y=1, is_revealed=True)
        self.assertEqual(cell.print(), '0')

        cell = Cell(x=1, y=1, is_revealed=True, adjacent_black_holes=1)
        self.assertEqual(cell.print(), '1')

        cell = Cell(x=1, y=1, is_black_hole=True)
        self.assertEqual(cell.print(debug=True), 'H')

        cell = Cell(x=1, y=1, is_black_hole=True, is_revealed=True)
        self.assertEqual(cell.print(debug=True), 'H')

        cell = Cell(x=1, y=1, is_revealed=True, adjacent_black_holes=1)
        self.assertEqual(cell.print(debug=True), '1R')
