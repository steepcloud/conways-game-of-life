import unittest
import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../src')))
from src.game_logic import *
from src.gui import *


class TestGameLogic(unittest.TestCase):
    def setUp(self):
        """Setting up the test environment for the game logic."""
        self.game_logic = GameLogic(grid=[])
        self.game_logic._initialize_grid("block") # we initialize it with a default known pattern

    def test_initialize_grid(self):
        """Testing the grid initialization with a known pattern."""
        grid = self.game_logic.grid
        # Testing for specific patterns like "block"
        self.assertEqual(grid[0][0].is_active, True)
        self.assertEqual(grid[1][0].is_active, True)
        self.assertEqual(grid[0][1].is_active, True)
        self.assertEqual(grid[1][1].is_active, True)

    def test_get_current_state(self):
        """Testing that the current state of the grid is correct."""
        current_state = self.game_logic.get_current_state()
        # Checking the state of specific cells, e.g., for "block" pattern
        self.assertTrue(current_state[0][0])
        self.assertTrue(current_state[1][1])
        self.assertFalse(current_state[0][2])

    def test_save_and_load_state(self):
        """Testing saving and loading the game state."""
        window = pygame.Surface((100, 100))
        grid = initialize_gui(window)
        self.game_logic._initialize_grid("block")
        self.game_logic.save_state("test_state.pkl")
        new_game_logic = GameLogic(grid)
        new_game_logic.load_state("test_state.pkl")

        self.assertEqual(len(new_game_logic.grid), len(self.game_logic.grid))
        self.assertEqual(len(new_game_logic.grid[0]), len(self.game_logic.grid[0]))

        # Checking that the state is the same after loading
        loaded_state = new_game_logic.get_current_state()
        self.assertEqual(self.game_logic.get_current_state(), loaded_state)

    def test_update_with_active_cells(self):
        """Testing updating the grid with some active cells."""
        # Setting some cells to be active
        self.game_logic.grid[0][0].is_active = True
        self.game_logic.grid[0][1].is_active = True
        self.game_logic.update()

        # Checking if the active cells have changed based on rules
        updated_state = self.game_logic.get_current_state()
        # For simplicity, let's just test that the first few cells remain alive
        self.assertTrue(updated_state[0][0])
        self.assertTrue(updated_state[0][1])

    def test_update_with_edge_case_cells(self):
        """Testing grid update with edge cases, such as cells on the grid's edge."""
        self.game_logic._initialize_grid("loaf")  # Known pattern with edge interactions

        # Checking some cells to ensure correct transition (for loaf pattern)
        updated_state = self.game_logic.get_current_state()
        self.assertTrue(updated_state[3][5])

    def test_parallel_update(self):
        """Testing that the parallel update works without errors."""
        # Initialize a random grid for testing parallel execution
        self.game_logic._initialize_grid("loaf")
        try:
            self.game_logic.update()  # Will run in parallel
            self.assertTrue(True)  # If no exceptions were raised, the test passes
        except Exception as e:
            self.fail(f"Parallel update failed with exception: {e}")

    def test_cell_toggling(self):
        """Testing the toggling of cell states using GUI interaction."""
        grid = []
        window = pygame.Surface((100, 100))
        grid = initialize_gui(window)
        # Toggle some cells in the grid and check state
        cell = grid[0][0]
        self.assertFalse(cell.is_active)
        cell.is_active = not cell.is_active
        self.assertTrue(cell.is_active)

    def test_random_cell_activation(self):
        """Testing that random cells get activated correctly within defined rules."""
        # Manually set some cells active and check behavior
        self.game_logic._initialize_grid("block")
        self.game_logic.grid[0][0].is_active = True
        self.game_logic.update()
        self.assertTrue(self.game_logic.grid[0][0].is_active)

if __name__ == '__main__':
    unittest.main()
