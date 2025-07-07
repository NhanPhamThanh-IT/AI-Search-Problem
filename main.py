"""Rush Hour Auto Solver - Main Application."""

import sys
from rushhour_logic import RushHourSolver
from display import GameDisplay
from game_controller import GameController
from config import DEFAULT_MAP_FILE


def main():
    """Main function - initialize and run the Rush Hour solver."""
    # Solve the problem
    solver = RushHourSolver(DEFAULT_MAP_FILE)
    solution, total_cost, expanded_nodes = solver.solve_bfs()
    
    if not solution:
        print("No solution found!")
        return
    
    # Initialize display
    board = solution[0][0].board
    display = GameDisplay(len(board[0]), len(board))
    
    # Initialize game controller and run animation
    controller = GameController(display)
    controller.run_solution_animation(solution, len(expanded_nodes))
    
    # Clean up
    display.quit()
    sys.exit()


if __name__ == "__main__":
    main() 