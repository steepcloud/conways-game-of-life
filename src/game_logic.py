from dataclasses import dataclass
from typing import List, Tuple
import pickle
from gui import Cell, CELL_SIZE, ROWS, COLS

@dataclass
class GameLogic:
    """Class to manage the logic of Conway's Game of Life."""
    grid: List[List[Cell]]

    def __post_init__(self):
        """Initialize the grid with inactive cells."""
        self.grid = [
            [Cell(x=col * CELL_SIZE, y=row * CELL_SIZE)
             for col in range(COLS)]
            for row in range(ROWS)
        ]

    def _initialize_grid(self, pattern: str) -> None:
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

    def set_pattern(self, coordinates: List[Tuple[int, int]], contagious=False, defensive=False) -> None:
        """Set a pattern of active cells with optional contagious or defensive properties.

        Args:
            coordinates (List[Tuple[int, int]]): List of coordinates for the pattern.
            contagious (bool): If True, cells will be set as contagious.
            defensive (bool): If True, cells will be set as defensive.

        Returns:
            None
        """
        for row, col in coordinates:
            if 0 <= row < len(self.grid) and 0 <= col < len(self.grid[0]):
                cell = self.grid[row][col]
                cell.is_active = True
                if contagious:
                    cell.is_contagious = True
                if defensive:
                    cell.is_defensive = True

    def get_current_state(self) -> List[List[bool]]:
        """Get the current state of the grid.

        Returns:
            List[List[bool]]: A 2D list representing the active states of the cells.
        """
        return [[cell.is_active for cell in row] for row in self.grid]

    def save_state(self, filename: str) -> None:
        """Save the current state of the grid to a file.

        Args:
            filename (str): The filename to save the state.

        Returns:
            None
        """
        with open(filename, 'wb') as file:
            pickle.dump([[cell.is_active for cell in row] for row in self.grid], file)

    def load_state(self, filename: str) -> None:
        """Load the grid state from a file.

        Args:
            filename (str): The filename to load the state from.

        Returns:
            None
        """
        with open(filename, 'rb') as file:
            state = pickle.load(file)
            for row_index, row in enumerate(state):
                for col_index, is_active in enumerate(row):
                    self.grid[row_index][col_index].is_active = is_active

    def update(self) -> None:
        """Update the grid according to the Game of Life rules, including contagion effects.

        Returns:
            None
        """
        new_grid = [[cell.copy() for cell in row] for row in self.grid]

        for row in range(len(self.grid)):
            for col in range(len(self.grid[0])):
                live_neighbors = self.count_neighbors(row, col)
                contagious_neighbors = self.count_contagious_neighbors(row, col)

                current_cell = self.grid[row][col]

                if current_cell.is_active:
                    new_grid[row][col].is_active = live_neighbors in (2, 3)
                else:
                    # inactive cells become active if they have 3 live neighbors
                    # or at least one contagious neighbor
                    new_grid[row][col].is_active = live_neighbors == 3 or contagious_neighbors > 0

                # applying defensive mechanism
                if current_cell.is_defensive:
                    new_grid[row][col].is_active = False # defense: remain inactive

        self.grid = new_grid

    def count_neighbors(self, row: int, col: int) -> int:
        """Count the number of active neighbors around a given cell.

        Args:
            row (int): The row index of the cell.
            col (int): The column index of the cell.

        Returns:
            int: The number of active neighbors.
        """
        return sum(
            self.grid[(row + dr) % len(self.grid)][(col + dc) % len(self.grid[0])].is_active
            for dr in [-1, 0, 1]
            for dc in [-1, 0, 1]
            if (dr != 0 or dc != 0)  # Exclude the cell itself
        )

    def count_contagious_neighbors(self, row: int, col: int) -> int:
        """Count the number of contagious neighbors around a given cell.

        Args:
            row (int): The row index of the cell.
            col (int): The column index of the cell.

        Returns:
            int: The number of contagious neighbors.
        """
        return sum(
            self.grid[(row + dr) % len(self.grid)][(col + dc) % len(self.grid[0])].is_contagious
            for dr in [-1, 0, 1]
            for dc in [-1, 0, 1]
            if (dr != 0 or dc != 0)  # exclude the cell itself
        )