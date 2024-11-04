import pygame
from dataclasses import dataclass
from typing import List, Tuple

CELL_SIZE = 20
ROWS = 30
COLS = 30

@dataclass
class Cell:
    """Class representing a cell in the grid."""
    x: int # X coordinate of the cell
    y: int # Y coordinate of the cell
    is_active: bool = False # state of the cell (active or inactive)
    is_contagious: bool = False # state of the contagious cell
    is_defensive: bool = False # state of the defensive cell

    def copy(self):
        return Cell(self.x, self.y, self.is_active, self.is_contagious, self.is_defensive)

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
    RED = (255, 0, 0)
    BLUE = (0, 0, 255)

    grid = [[Cell(x=col * CELL_SIZE, y=row * CELL_SIZE) for col in range(COLS)] for row in range(ROWS)]

    for row in grid:
        for cell in row:
            rect = pygame.Rect(cell.x, cell.y, CELL_SIZE, CELL_SIZE)

            if cell.is_active:
                color = GREEN
            elif cell.is_contagious:
                color = RED
            elif cell.is_defensive:
                color = BLUE
            else:
                color = WHITE

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
            if cell.is_active:
                color = (0, 255, 0)  # Green for active cells
            elif cell.is_contagious:
                color = (255, 0, 0)  # Red for contagious cells
            elif cell.is_defensive:
                color = (0, 0, 255)  # Blue for defensive cells
            else:
                color = (128, 128, 128)  # Gray for inactive cells

            pygame.draw.rect(window, color, rect)
            pygame.draw.rect(window, (0, 0, 0), rect, 1)

def toggle_cell_state(grid: List[List[Cell]],
                      mouse_pos: Tuple[int, int],
                      single_click: bool = False,
                      contagious: bool = False,
                      defensive: bool = False) -> None:
    """Toggle the state of a cell when clicked, with options for contagious and defensive states.

    Args:
        grid (List[List[Cell]]): The grid of cells.
        mouse_pos (Tuple[int, int]): The x and y coordinates of the mouse position.
        single_click (bool): If True, toggles the cell state; if False, sets the cell to active.
        contagious (bool): If True, toggle the contagious state.
        defensive (bool): If True, toggle the defensive state.

    Returns:
        None
    """
    col = mouse_pos[0] // CELL_SIZE
    row = mouse_pos[1] // CELL_SIZE

    if 0 <= row < len(grid) and 0 <= col < len(grid[0]):
        cell = grid[row][col]
        if single_click:
            if contagious:
                cell.is_contagious = not cell.is_contagious
            elif defensive:
                cell.is_defensive = not cell.is_defensive
            else:
                cell.is_active = not cell.is_active
        else:
            cell.is_active = True
