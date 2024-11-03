from pickle import FALSE

import pygame
from pygame.examples.grid import WINDOW_HEIGHT, WINDOW_WIDTH

from src import __version__
from src.gui import *
# from src.game_logic import GameLogic

WINDOW_WIDTH = 600
WINDOW_HEIGHT = 600

def main():
    """Main entry point of the game."""

    pygame.init()

    window = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
    pygame.display.set_caption("Conway's Game of Life")

    grid = initialize_gui(window)

    #game_logic = GameLogic()

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    mouse_pos = pygame.mouse.get_pos()
                    toggle_cell_state(grid, mouse_pos)

        #game_logic.update()

        window.fill((0, 0, 0)) # fill the window with black (can be other color)

        for row in grid:
            for cell in row:
                rect = pygame.Rect(cell.x, cell.y, CELL_SIZE, CELL_SIZE)
                color = (0, 255, 0) if cell.is_active else (255, 255, 255)
                pygame.draw.rect(window, color, rect)
                pygame.draw.rect(window, (0, 0, 0), rect, 1)

        #game_logic.draw(window)

        #initialize_gui(window)

        pygame.display.flip()

    pygame.quit()

if __name__ == "__main__":
    print(f"Version: {__version__}")
    main()