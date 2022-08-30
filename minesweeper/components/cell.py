from dataclasses import dataclass

unraveled_print = '*'


@dataclass()
class Cell:
    """
    A cell in the minesweeper game.
    """
    x: int
    y: int
    is_black_hole: bool = False
    is_revealed: bool = False
    adjacent_black_holes: int = 0

    def __str__(self):
        return f"{self.adjacent_black_holes if self.is_revealed else unraveled_print}"

    def __repr__(self):
        return self.__str__()

    def print(self, debug: bool = False) -> str:
        """
        Return a string representation of the cell.
        :param debug: output in debug mode.
        :return: string representation of the cell.
        """
        if debug:
            return 'H' if self.is_black_hole else f'{self.adjacent_black_holes}{"R" if self.is_revealed else ""}'
        return self.__str__()
