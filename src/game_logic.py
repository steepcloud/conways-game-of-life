from dataclasses import dataclass
from typing import List, Tuple
import pickle
from gui import Cell
from utils import WINDOW_WIDTH, WINDOW_HEIGHT, CELL_SIZE, BASE_REVIVAL_PROB, MAX_REVIVAL_PROB, DEATH_PROB
import random as rd
from concurrent.futures import ThreadPoolExecutor
from threading import Lock

@dataclass
class GameLogic:
    grid: List[List[Cell]]
    lock: Lock = Lock()

    def _initialize_grid(self, pattern: str) -> None:
        """Initialize the grid with a given pattern.

        Args:
            pattern (str): The name of the pattern to initialize the grid with.
                Supported patterns: "glider", "blinker", "block", "bee-hive", "loaf", "boat", "tub".

        This method creates a grid of `Cell` objects and sets cells to `True` (active) according to
        the specified pattern, such as a "glider" or "block". It raises a `ValueError` if an invalid
        pattern is provided.
        """
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
        """Set a specific pattern of active cells in the grid.

        Args:
            coordinates (List[Tuple[int, int]]): A list of (row, col) tuples specifying the active cells.

        This method marks the cells at the provided coordinates as active (`is_active = True`) in the grid.
        """
        for row, col in coordinates:
            if 0 <= row < len(self.grid) and 0 <= col < len(self.grid[0]):
                self.grid[row][col].is_active = True

    def get_current_state(self) -> List[List[bool]]:
        """Retrieve the current state of the grid as a 2D list of booleans.

        Returns:
            List[List[bool]]: A 2D list where each element represents the `is_active` state of a cell.

        This method returns the current state of the grid, where `True` indicates an active cell and
        `False` indicates an inactive cell.
        """
        return [[cell.is_active for cell in row] for row in self.grid]

    def save_state(self, filename: str) -> None:
        """Save the current state of the grid to a file.

        Args:
            filename (str): The name of the file where the grid state will be saved.

        This method serializes the grid state into a file using pickle, so that it can be loaded later.
        """
        try:
            with open(filename, 'wb') as file:
                pickle.dump([[cell.is_active for cell in row] for row in self.grid], file)
        except (OSError, IOError) as e:
            print(f"Error saving state to {filename}: {e}")

    def load_state(self, filename: str) -> None:
        """Load a previously saved state of the grid from a file.

        Args:
            filename (str): The name of the file to load the grid state from.

        This method attempts to load the grid state from the specified file. If the file is not found or
        the state cannot be unpickled, it will initialize the grid with a default "loaf" pattern.
        """
        try:
            with open(filename, 'rb') as file:
                state = pickle.load(file)
                for row_index, row in enumerate(state):
                    for col_index, is_active in enumerate(row):
                        self.grid[row_index][col_index].is_active = is_active
        except (FileNotFoundError, pickle.UnpicklingError) as e:
            print(f"Error loading state: {e}")
            self._initialize_grid("loaf")

    def update(self) -> None:
        """Update the grid according to the rules of the game with a dynamic revival probability.

        This method calculates the current population density and adjusts the revival probability based
        on the grid's sparsity. It applies the update rules in parallel using a `ThreadPoolExecutor` to
        improve performance by updating each row concurrently.
        """
        # calculating the current population density
        active_cells = sum(cell.is_active for row in self.grid for cell in row)
        total_cells = len(self.grid) * len(self.grid[0])
        density = active_cells / total_cells if total_cells > 0 else 0

        # adjusting revival probability based on population density (sparser -> higher revival chance)
        adjusted_revival_prob = BASE_REVIVAL_PROB + (1 - density) * (MAX_REVIVAL_PROB - BASE_REVIVAL_PROB)

        new_grid = [[Cell(cell.x, cell.y) for cell in row] for row in self.grid]

        # using ThreadPoolExecutor to parallelize the update process
        with ThreadPoolExecutor() as executor:
            futures = [executor.submit(self.update_row, row, new_grid, adjusted_revival_prob)
                       for row in range(len(self.grid))]
            for future in futures:
                future.result()

        self.grid = new_grid

    def update_row(self, row: int, new_grid: List[List[Cell]], adjusted_revival_prob: float) -> None:
        """Update a single row of cells based on the game rules.

        Args:
            row (int): The index of the row to update.
            new_grid (List[List[Cell]]): A grid that will be populated with the updated cell states.
            adjusted_revival_prob (float): The probability of revival for dead cells, adjusted by population density.

        This method processes each cell in the row, applying the standard game rules for cell survival and revival.
        It checks the number of live neighbors and updates the cell's state accordingly.
        """
        for col in range(len(self.grid[0])):
            live_neighbors = self.count_neighbors(row, col)
            cell = self.grid[row][col]

            if cell.is_active:
                if live_neighbors not in (2, 3):
                    if live_neighbors > 3 and rd.random() < DEATH_PROB:
                        new_grid[row][col].is_active = False
                    else:
                        new_grid[row][col].is_active = False
                else:
                    new_grid[row][col].is_active = True
            else:
                if live_neighbors == 3:
                    new_grid[row][col].is_active = True
                elif live_neighbors in (2, 4) and rd.random() < adjusted_revival_prob:
                    new_grid[row][col].is_active = True

    def count_neighbors(self, row: int, col: int) -> int:
        """Count the number of active neighbors of a given cell.

        Args:
            row (int): The row index of the cell.
            col (int): The column index of the cell.

        Returns:
            int: The number of active neighbors surrounding the given cell.

        This method checks the eight surrounding cells (including diagonals) and counts how many are active.
        It handles edge wrapping by using modulo arithmetic to ensure the grid wraps around at the edges (toroidal array).
        """
        with self.lock:
            return sum(
                self.grid[(row + dr) % len(self.grid)][(col + dc) % len(self.grid[0])].is_active
                for dr in [-1, 0, 1] for dc in [-1, 0, 1] if (dr, dc) != (0, 0)
            )
