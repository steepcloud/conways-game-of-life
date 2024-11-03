from dataclasses import dataclass
from typing import List, Tuple
import pickle
from gui import Cell, CELL_SIZE
from main import WINDOW_HEIGHT, WINDOW_WIDTH

@dataclass
class GameLogic:
    grid: List[List[Cell]]

    def _initialize_grid(self, pattern: str) -> None:
        self.grid = [
            [Cell(x * CELL_SIZE, y * CELL_SIZE)
            for x in range(WINDOW_WIDTH // CELL_SIZE)]
            for y in range(WINDOW_HEIGHT // CELL_SIZE)
        ]

        # still life patterns (for the others that don't fit as well, e.g. blinker / glider)
        if pattern == "glider":
            self.set_pattern([(1, 0), (2, 1), (0, 2), (1, 2), (2, 2)])
        elif pattern == "blinker":
            self.set_pattern([(1, 0), (1, 1), (1, 2)])
        elif pattern == "block":
            self.set_pattern([(0, 0), (0, 1), (1, 0), (1, 1)])
        elif pattern == "bee-hive":
            self.set_pattern([(1, 2), (1, 3), (2, 1), (2, 4), (3, 2), (3, 3)])
        elif pattern == "loaf":
            self.set_pattern([(1, 2), (1, 3), (2, 1), (2, 4), (3, 2), (3, 5)])
        elif pattern == "boat":
            self.set_pattern([(1, 1), (1, 2), (2, 1), (2, 3), (3, 2)])
        elif pattern == "tub":
            self.set_pattern([(1, 2), (2, 1), (2, 3), (3, 2)])
        else:
            raise ValueError("Unknown pattern: {}".format(pattern))

    def set_pattern(self, coordinates: List[Tuple[int, int]]) -> None:
        for row, col in coordinates:
            if 0 <= row < len(self.grid) and 0 <= col < len(self.grid[0]):
                self.grid[row][col].is_active = True

    def get_current_state(self) -> List[List[bool]]:
        return [[cell.is_active for cell in row] for row in self.grid]

    def save_state(self, filename: str) -> None:
        with open(filename, 'wb') as file:
            pickle.dump([[cell.is_active for cell in row] for row in self.grid], file)

    def load_state(self, filename: str) -> None:
        with open(filename, 'rb') as file:
            state = pickle.load(file)
            for row_index, row in enumerate(state):
                for col_index, is_active in enumerate(row):
                    self.grid[row_index][col_index].is_active = is_active

    def update(self) -> None:
        new_grid = [[Cell(cell.x, cell.y) for cell in row] for row in self.grid]

        for row in range(len(self.grid)):
            for col in range(len(self.grid[0])):
                live_neighbors = self.count_neighbors(row, col)

                if self.grid[row][col].is_active:
                    new_grid[row][col].is_active = live_neighbors in (2, 3)
                else:
                    new_grid[row][col].is_active = live_neighbors == 3

        self.grid = new_grid

    def count_neighbors(self, row: int, col: int) -> int:
        return sum(
            self.grid[neighbor_row][neighbor_col].is_active
            for direction in [1j, 1, -1j, -1, 1j - 1, 1j + 1, -1j - 1, -1j + 1]
            if (0 <= (neighbor_row := row + int(direction.imag)) < len(self.grid) and
                0 <= (neighbor_col := col + int(direction.real)) < len(self.grid[0]))
        )