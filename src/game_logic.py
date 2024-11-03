from dataclasses import dataclass
from typing import List, Tuple
from gui import Cell

@dataclass
class GameLogic:
    def __init__(self, grid: List[List[Cell]]):
        self.grid = grid

    @classmethod
    def __update__(cls) -> None:
        # TODO
        pass

    @classmethod
    def count_neighbors(cls, row: int, col: int) -> int:
        # TODO
        pass

