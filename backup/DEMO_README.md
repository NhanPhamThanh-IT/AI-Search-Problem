# Rush Hour Puzzle Solver - Demo Guide

## Available Demo Modes

### 🖼️ GUI Demo (`gui_demo_rushhour.py`)

**Graphical Interface with Pygame**

Features:

- Visual puzzle board with colored vehicles
- Interactive buttons for different algorithms
- Real-time solution animation
- Performance statistics display
- Manual step-through controls

Controls:

- Click "Solve BFS/DFS/UCS/A\*" buttons to find solution
- "Animate Solution" to watch moves
- "Speed+/-" to control animation speed
- "Reset Puzzle" to start over
- **Keyboard shortcuts:**
  - `SPACE` - Start/stop animation
  - `R` - Reset puzzle
  - `←/→` - Step through solution manually

### 🎮 Interactive Console Demo (`interactive_demo_rushhour.py`)

**Enhanced Text-Based Interface**

Features:

- Interactive menu system
- Manual puzzle solving mode
- Step-by-step solution animation
- Algorithm performance comparison
- Move hints and suggestions

Commands in Interactive Mode:

- `move X right` - Move vehicle X to the right
- `hint` - Get a suggestion for next move
- `reset` - Reset puzzle to initial state
- `quit` - Exit interactive mode

### 📊 Original Console Demo (`demo_rushhour.py`)

**Simple Text Output**

Features:

- Tests all algorithms automatically
- Shows solution steps
- Performance metrics
- Basic move testing

## How to Run

### Option 1: Use the Launcher (Recommended)

```bash
cd src
python demo_launcher.py
```

### Option 2: Run Individual Demos

```bash
cd src

# GUI Demo
python gui_demo_rushhour.py

# Interactive Demo
python interactive_demo_rushhour.py

# Original Demo
python demo_rushhour.py
```

## Requirements

- Python 3.7+
- pygame (for GUI demo only)

Install pygame:

```bash
pip install pygame
```

## Puzzle Description

The demo uses a 6x6 Rush Hour puzzle with:

- **Vehicle X** (red) - Target vehicle that needs to reach the exit
- **Vehicles A-G** - Blocking vehicles of various sizes
- **Goal** - Move vehicle X to the right edge (exit)

## Algorithms Tested

1. **BFS (Breadth-First Search)** - Optimal solution, explores level by level
2. **DFS (Depth-First Search)** - May find longer solutions, explores deeply first
3. **UCS (Uniform Cost Search)** - Optimal solution, considers move costs
4. **A\*** - Optimal solution with heuristic guidance, usually fastest

## Tips

- The GUI demo provides the best visual experience
- Interactive demo is great for understanding the puzzle mechanics
- Try manual solving mode to appreciate the algorithm's efficiency
- Compare algorithm performance to see the differences

Enjoy exploring the Rush Hour Puzzle Solver! 🚗
