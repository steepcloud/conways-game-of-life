import numba
import numpy as np
from numba import cuda, float32, int32
import math
from numba.cuda import random

print(numba.cuda.driver.get_version())
print(numba.cuda.get_current_device())

@cuda.jit
def count_neighbors_kernel(grid, neighbor_count, width, height):
    """
        CUDA kernel to count live neighbors for each cell.
        grid: The current state of the grid (2D array of boolean values).
        neighbor_count: The result grid (2D array of integers) for neighbor counts.
        width: The width of the grid (number of columns).
        height: The height of the grid (number of rows).
    """
    x, y = cuda.grid(2)

    if x >= width or y >= height:
        return

    live_neighbors = 0
    for dx in range(-1, 2):
        for dy in range(-1, 2):
            if dx == 0 and dy == 0:
                continue
            nx, ny = x + dx, y + dy
            if 0 <= nx < width and 0 <= ny < height:
                live_neighbors += grid[ny, nx]

    neighbor_count[y, x] = live_neighbors

@cuda.jit
def update_grid_kernel(grid, neighbor_count, new_grid, width, height, death_prob, base_revival_prob, max_revival_prob, rng_states):
    """
        CUDA kernel to apply the update rules to the grid.
        grid: The current state of the grid (2D array of boolean values).
        neighbor_count: 2D array with the count of live neighbors for each cell.
        new_grid: 2D array to store the updated state of the grid.
        width: The width of the grid (number of columns).
        height: The height of the grid (number of rows).
        death_prob: The probability of death for overcrowded cells.
        base_revival_prob: The base revival probability for dead cells.
        max_revival_prob: The maximum revival probability for sparse grids.
    """
    x, y = cuda.grid(2)

    if x >= width or y >= height:
        return

    live_neighbors = neighbor_count[y, x]

    # get the random state for this thread
    state = rng_states[x, y]
    rnd = cuda.random.xoroshiro128p_uniform_float32(state)

    if grid[y, x]:  # cell is alive
        if live_neighbors not in (2, 3):
            if live_neighbors > 3 and rnd < death_prob:
                new_grid[y, x] = False
            else:
                new_grid[y, x] = False
        else:
            new_grid[y, x] = True
    else:  # cell is dead
        if live_neighbors == 3:
            new_grid[y, x] = True
        elif (live_neighbors in (2, 4) and
              rnd < (base_revival_prob + (1 - (live_neighbors / 8.0)) * (max_revival_prob - base_revival_prob))):
            new_grid[y, x] = True

def run_cuda_kernels(grid, death_prob, base_revival_prob, max_revival_prob):
    """
        Run the CUDA kernels for updating the grid.
        grid: The grid data as a numpy array.
        death_prob: The death probability for overcrowded cells.
        base_revival_prob: The base revival probability for dead cells.
        max_revival_prob: The maximum revival probability for sparse grids.
    """
    width = grid.shape[1]
    height = grid.shape[0]

    # allocating memory on the GPU
    grid_device = cuda.to_device(grid)
    neighbor_count_device = cuda.device_array(grid.shape, dtype=np.int32)
    new_grid_device = cuda.device_array(grid.shape, dtype=np.bool)

    # creating the random number generator states
    rng_states_device = cuda.device_array((height, width), dtype=np.uint32)
    print("Grid dimensions:", height, width)
    print("RNG states shape:", rng_states_device.shape)
    seed = 42
    cuda.random.create_xoroshiro128p_states(rng_states_device, seed, (height * width,))

    # setting up block and grid dims
    threads_per_block = (16, 16) # based on GPU's capabilities
    blocks_per_grid = (grid.shape[1] // threads_per_block[0] + 1, grid.shape[0] // threads_per_block[1] + 1)

    # launching neighbor counting kernel
    count_neighbors_kernel[blocks_per_grid, threads_per_block](grid_device, neighbor_count_device, width, height)

    # launching grid update kernel
    update_grid_kernel[blocks_per_grid, threads_per_block](grid_device, neighbor_count_device, new_grid_device, width,
                                                           height, death_prob, base_revival_prob, max_revival_prob)

    # copy the updated grid back
    new_grid = new_grid_device.copy_to_host()

    return new_grid

def convert_grid_to_device(grid):
    """
        Convert the grid to a device-compatible format for CUDA.
    """
    return cuda.to_device(grid)

def convert_grid_from_device(grid_device):
    """
        Convert the grid back from the CUDA device to the CPU.
    """
    return grid_device.copy_to_host()