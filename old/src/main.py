"""Rush Hour Auto Solver - Main Application."""

import sys
import os

# Add the src directory to Python path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from algorithms.rushhour_logic import RushHourSolver
from ui.display import GameDisplay
from ui.game_controller import GameController
from ui.menu import GameMenu
from config.config import DEFAULT_MAP_FILE


def main():
    """Main function - initialize and run the Rush Hour solver."""
    try:
        # Show menu to select level
        menu = GameMenu()
        selected_map = menu.run()
        menu.quit()
        
        if not selected_map:
            print("Game cancelled by user.")
            return
        
        # Check if file exists
        if not os.path.exists(selected_map):
            print(f"Map file not found: {selected_map}")
            print(f"Looking for file at: {os.path.abspath(selected_map)}")
            return
        
        print(f"Loading map: {selected_map}")
        
        # Solve the problem
        solver = RushHourSolver(selected_map)
        result = solver.solve_bfs()
        
        # Handle different return formats
        if isinstance(result, tuple) and len(result) == 3:
            solution, total_cost, expanded_nodes = result
        elif isinstance(result, tuple) and len(result) == 2:
            solution, expanded_nodes = result
            total_cost = 0
        else:
            solution = result
            expanded_nodes = []
            total_cost = 0
        
        if not solution:
            print("No solution found!")
            return
        
        # Debug: Print solution structure
        print(f"Solution found with {len(solution)} steps")
        if len(solution) > 0:
            print(f"First step type: {type(solution[0])}")
            print(f"First step content: {solution[0]}")
        
        # Initialize display
        board = solution[0][0].board if isinstance(solution[0], tuple) else solution[0].board
        display = GameDisplay(len(board[0]), len(board))
        
        # Initialize game controller and run animation
        controller = GameController(display)
        controller.run_solution_animation(solution, len(expanded_nodes) if isinstance(expanded_nodes, list) else expanded_nodes)
        
        # Clean up
        display.quit()
        
    except Exception as e:
        print(f"Error occurred: {e}")
        import traceback
        traceback.print_exc()
    finally:
        sys.exit()


if __name__ == "__main__":
    main()