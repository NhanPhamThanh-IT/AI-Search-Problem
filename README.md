# Rush Hour Auto Solver

A clean, modular implementation of the Rush Hour puzzle solver with visual animation using pygame.

## Code Structure

The codebase has been organized into separate modules for better maintainability:

### Core Files

- **`main.py`** - Main application entry point
- **`rushhour_logic.py`** - Core game logic and solver algorithms
- **`display.py`** - Visual display handling with pygame
- **`game_controller.py`** - Game animation and control logic
- **`config.py`** - Configuration constants and settings

### Key Classes

#### `RushHourVehicle`

- Represents a vehicle with position and orientation
- Handles vehicle properties and movement validation

#### `RushHourState`

- Represents the current state of the puzzle board
- Handles state transitions and goal checking
- Generates successor states for search algorithms

#### `RushHourSolver`

- Implements multiple search algorithms:
  - BFS (Breadth-First Search)
  - DFS (Depth-First Search)
  - UCS (Uniform Cost Search)
  - A\* (A-Star Search)

#### `GameDisplay`

- Handles all pygame visualization
- Draws board, vehicles, and status information
- Manages colors and UI elements

#### `GameController`

- Controls animation timing and user interaction
- Handles pause/resume functionality
- Manages game state transitions

## Features

- **Multiple Search Algorithms**: Compare different solving approaches
- **Visual Animation**: Watch the solution step-by-step
- **Pause/Resume**: Press SPACE to pause/resume animation
- **Clean Architecture**: Modular design for easy maintenance
- **Type Hints**: Full type annotations for better code clarity
- **Documentation**: Comprehensive docstrings

## Usage

```python
python main.py
```

## Key Improvements

1. **Separation of Concerns**: Each module has a single responsibility
2. **Type Safety**: Full type hints throughout the codebase
3. **Documentation**: Clear docstrings for all classes and methods
4. **Configuration**: Centralized configuration management
5. **Error Handling**: Improved error handling and validation
6. **Code Reusability**: Modular components that can be easily extended
7. **Clean Naming**: Clear, descriptive variable and method names

## Configuration

Edit `config.py` to customize:

- Display settings (cell size, colors, fonts)
- Animation timing
- Color schemes for different vehicles
- Default map file location

## Map Format

Maps are stored in text files with:

- `.` for empty spaces
- Letters (A-Z) for vehicles
- `X` for the target vehicle that needs to reach the exit
