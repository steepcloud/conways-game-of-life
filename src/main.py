from pickle import FALSE

import pygame
from pygame.examples.grid import WINDOW_HEIGHT, WINDOW_WIDTH

from src import __version__
from gui import *

WINDOW_WIDTH = 600
WINDOW_HEIGHT = 600

def main():
    from game_logic import GameLogic
    """Main entry point of the game."""

    pygame.init()

    window = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT), pygame.HWSURFACE | pygame.DOUBLEBUF)
    pygame.display.set_caption("Conway's Game of Life")

    grid = initialize_gui(window)
    back_buffer = pygame.Surface((WINDOW_WIDTH, WINDOW_HEIGHT))

    game_logic = GameLogic(grid)

    '''Ensuring load_state works'''
    try:
        game_logic.load_state('game_state.pkl')
    except FileNotFoundError:
        print("No saved game state found. Starting with a new grid.")
        game_logic._initialize_grid("tub")

    #game_logic._initialize_grid("tub")

    running = True
    mouse_dragging = False
    mouse_clicked_pos = None
    simulation_running = False

    clock = pygame.time.Clock()

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                '''Testing save_state (can be further used in future)'''
                # game_logic.save_state('game_state.pkl')
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

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    simulation_running = not simulation_running

        if mouse_dragging:
            mouse_pos = pygame.mouse.get_pos()
            if mouse_pos != mouse_clicked_pos:
                toggle_cell_state(grid, mouse_pos)
                mouse_clicked_pos = mouse_pos

        if simulation_running:
            game_logic.update()

        #window.fill((0, 0, 0)) # fill the window with black (can be other color)
        back_buffer.fill((0, 0, 0))

        draw_grid(back_buffer, game_logic.grid)

        grid = game_logic.grid

        #game_logic.draw(window)

        #initialize_gui(window)

        window.blit(back_buffer, (0, 0))
        pygame.display.flip()
        clock.tick(10)

    pygame.quit()

if __name__ == "__main__":
    print(f"Version: {__version__}")
    main()