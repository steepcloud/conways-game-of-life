import numba
import numpy as np
from numba import cuda, float32, int32
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

            nx, ny = (x + dx) % width, (y + dy) % height

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
        rng_states: Random number generator states for each thread.
    """
    x, y = cuda.grid(2)
    if x >= width or y >= height:
        return

    live_neighbors = neighbor_count[y, x]

    if grid[y, x]:  # cell is alive
        new_grid[y, x] = True if live_neighbors in (2, 3) else False
    else:  # cell is dead
        new_grid[y, x] = True if live_neighbors == 3 else False

def run_cuda_kernels(grid, death_prob, base_revival_prob, max_revival_prob):
    """
        Run the CUDA kernels for updating the grid.
        grid: The grid data as a numpy array.
        death_prob: The death probability for overcrowded cells.
        base_revival_prob: The base revival probability for dead cells.
        max_revival_prob: The maximum revival probability for sparse grids.
    """
    width = np.int32(grid.shape[1])
    height = np.int32(grid.shape[0])

    # allocating memory on the GPU
    grid_device = cuda.to_device(grid)
    neighbor_count_device = cuda.device_array(grid.shape, dtype=np.int32)
    new_grid_device = cuda.device_array(grid.shape, dtype=np.bool_)

    # creating the random number generator states
    seed = 42
    #rng_states_device = cuda.random.create_xoroshiro128p_states(int(width * height), seed=seed).reshape((height, width))
    rng_states_device = cuda.random.create_xoroshiro128p_states(int(width * height), seed=seed)

    # setting up block and grid dims
    threads_per_block = (16, 16)  # based on GPU's capabilities
    blocks_per_grid = (grid.shape[1] // threads_per_block[0] + 1, grid.shape[0] // threads_per_block[1] + 1)

    # Print types of arguments for debugging
    print(f"grid_device type: {type(grid_device)}")
    print(f"neighbor_count_device type: {type(neighbor_count_device)}")
    print(f"new_grid_device type: {type(new_grid_device)}")
    print(f"width type: {type(width)}")
    print(f"height type: {type(height)}")
    print(f"death_prob type: {type(death_prob)}")
    print(f"base_revival_prob type: {type(base_revival_prob)}")
    print(f"max_revival_prob type: {type(max_revival_prob)}")
    print(f"rng_states_device type: {type(rng_states_device)}")

    # launching neighbor counting kernel
    count_neighbors_kernel[blocks_per_grid, threads_per_block](grid_device, neighbor_count_device, width, height)

    death_prob = np.float32(death_prob)
    base_revival_prob = np.float32(base_revival_prob)
    max_revival_prob = np.float32(max_revival_prob)

    # launching grid update kernel
    update_grid_kernel[blocks_per_grid, threads_per_block](grid_device, neighbor_count_device, new_grid_device, width,
                                                           height, death_prob, base_revival_prob, max_revival_prob,
                                                           rng_states_device)

    # copy the updated grid back
    new_grid = new_grid_device.copy_to_host()

    return new_grid
