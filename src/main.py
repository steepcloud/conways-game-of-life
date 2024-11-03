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

    window = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT), pygame.HWSURFACE | pygame.DOUBLEBUF)
    pygame.display.set_caption("Conway's Game of Life")

    grid = initialize_gui(window)
    back_buffer = pygame.Surface((WINDOW_WIDTH, WINDOW_HEIGHT))

    #game_logic = GameLogic()

    running = True
    mouse_dragging = False
    mouse_clicked_pos = None

    clock = pygame.time.Clock()

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1: # lmb
                    mouse_dragging = True
                    mouse_clicked_pos = pygame.mouse.get_pos()
                    toggle_cell_state(grid, mouse_clicked_pos, single_click=True)

            if event.type == pygame.MOUSEBUTTONUP:
                if event.button == 1:
                    mouse_dragging = False
                    mouse_clicked_pos = None

        if mouse_dragging:
            mouse_pos = pygame.mouse.get_pos()
            if mouse_pos != mouse_clicked_pos:
                toggle_cell_state(grid, mouse_pos)
                mouse_clicked_pos = mouse_pos

        #game_logic.update()

        #window.fill((0, 0, 0)) # fill the window with black (can be other color)
        back_buffer.fill((0, 0, 0))

        for row in grid:
            for cell in row:
                rect = pygame.Rect(cell.x, cell.y, CELL_SIZE, CELL_SIZE)
                color = (0, 255, 0) if cell.is_active else (255, 255, 255)
                pygame.draw.rect(back_buffer, color, rect)
                pygame.draw.rect(back_buffer, (0, 0, 0), rect, 1)

        #game_logic.draw(window)

        #initialize_gui(window)

        window.blit(back_buffer, (0, 0))
        pygame.display.flip()
        clock.tick(60)

    pygame.quit()

if __name__ == "__main__":
    print(f"Version: {__version__}")
    main()