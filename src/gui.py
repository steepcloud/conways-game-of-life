import pygame
from dataclasses import dataclass
from typing import List, Tuple

CELL_SIZE = 40
ROWS = 20
COLS = 20

@dataclass
class Cell:
    """Class representing a cell in the grid."""
    x: int # X coordinate of the cell
    y: int # Y coordinate of the cell
    is_active: bool = False # State of the cell (active or inactive)

def initialize_gui(window: pygame.Surface) -> List[List[Cell]]:
    """Initialize the GUI and create the grid of cells.

    Args:
        window (pygame.Surface): The Pygame window surface where the grid will be drawn.

    Returns:
        List[List[Cell]]: A 2D list representing the grid of cells.
    """
    # defining colors
    WHITE = (255, 255, 255)
    BLACK = (0, 0, 0)
    GREEN = (0, 255, 0)

    grid = [[Cell(x=col * CELL_SIZE, y=row * CELL_SIZE) for col in range(COLS)] for row in range(ROWS)]

    for row in grid:
        for cell in row:
            rect = pygame.Rect(cell.x, cell.y, CELL_SIZE, CELL_SIZE)

            color = GREEN if cell.is_active else WHITE
            pygame.draw.rect(window, color, rect)

            pygame.draw.rect(window, BLACK, rect, 1)

    return grid

def draw_grid(window: pygame.Surface, grid: List[List[Cell]]) -> None:
    """Draw the grid of cells on the window.

    Args:
        window (pygame.Surface): The surface to draw on.
        grid (List[List[Cell]]): The grid of cells.

    Returns:
        None
    """
    for row in grid:
        for cell in row:
            rect = pygame.Rect(cell.x, cell.y, CELL_SIZE, CELL_SIZE)
            color = (0, 255, 0) if cell.is_active else (255, 255, 255)
            pygame.draw.rect(window, color, rect)
            pygame.draw.rect(window, (0, 0, 0), rect, 1)

def toggle_cell_state(grid: List[List[Cell]], mouse_pos: Tuple[int, int], single_click: bool = False) -> None:
    """Toggle the state of a cell when clicked.

    Args:
        grid (List[List[Cell]]): The grid of cells.
        mouse_pos (Tuple[int, int]): The x and y coordinates of the mouse position.
        single_click (bool): If True, toggles the cell state; if False, sets the cell to active.

    Returns:
        None
    """
    col = mouse_pos[0] // CELL_SIZE
    row = mouse_pos[1] // CELL_SIZE

    if 0 <= row < len(grid) and 0 <= col < len(grid[0]):
        cell = grid[row][col]
        if single_click:
            cell.is_active = not cell.is_active
        else:
            cell.is_active = True
