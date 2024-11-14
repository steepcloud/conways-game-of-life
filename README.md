# Conway's Game of Life (Non-Deterministic Implementation)

This project is a non-deterministic implementation of **Conway's Game of Life** using **concurrent.futures** for parallel processing and **Pygame** for graphical visualization. (also having a **CUDA** parallel processing implementation on feature/cuda-implementation branch that has the classic rules of the game)

### Key Sections:
1. **Project Title** and **Description**: Brief intro to the project.
2. **Features**: Highlights the unique parts of your project, like non-deterministic behavior and CUDA acceleration.
3. **Requirements**: Lists dependencies that need to be installed.
4. **Installation**: Provides instructions on how to set up and run the project.
5. **Usage**: Brief guide on how to use the project after installation.

## Description

Conway's Game of Life is a cellular automaton devised by mathematician John Conway. The simulation evolves a grid of cells based on simple rules and can generate complex patterns and behaviors.

This implementation enhances the classic Game of Life by:

- **Non-deterministic behavior**: Randomized cell state transitions.
- **CUDA-based parallelization**: Optimized grid updates for faster performance on compatible GPUs.
- **Pygame for visualization**: Provides a simple and interactive graphical interface.

## Features

- **Non-deterministic simulations**: The state of cells can be influenced by random factors, introducing unpredictability into the evolution.
- **GPU acceleration**: Harnesses the power of **CUDA** to parallelize the grid updates, enabling faster processing for large grids.
- **Interactive GUI**: Users can control the simulation, spawn cells, and observe the game's evolution in real-time.

## Requirements

To run the project, you need the following dependencies:

- Python 3.8 or higher
- Pygame (version 2.0 or higher)
- CUDA (version 12.6 or higher)
- NumPy (version 1.21 or higher)

You can install the required dependencies using **Poetry**:

```bash
poetry install
```

## Instalation
# Clone the repository
```shell
git clone https://github.com/steepcloud/conways-game-of-life.git
cd conways-game-of-life
```

# Set up a virtual environment
If you prefer to use a virtual environment, you can set it up with Poetry:
```bash
poetry shell
```

# Install Dependencies
```bash
poetry install
```

## Usage
Once you have everything set up, you can run the Game of Life simulation:
```shell
python main.py
```

The program will open a graphical window where you can observe the simulation. You can interact with it by:

- Clicking on cells / drag 'n' click to toggle their state.
- Pausing and resuming the simulation.
- Saving and loading grid states. (ctrl+S, ctrl+L) (while simulation is paused)
