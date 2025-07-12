"""
Demo script for Rush Hour Puzzle Solver
Tests the solver with the provided puzzle data
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from rushhour import RushHourGame

def main():
    # Puzzle data từ user
    puzzle_data = {
        "size": [6, 6],
        "vehicles": [
            {"name": "A", "row": 0, "col": 2, "length": 2, "orientation": "H"},
            {"name": "B", "row": 1, "col": 1, "length": 2, "orientation": "H"},
            {"name": "C", "row": 1, "col": 4, "length": 2, "orientation": "V"},
            {"name": "D", "row": 1, "col": 5, "length": 2, "orientation": "V"},
            {"name": "E", "row": 4, "col": 0, "length": 2, "orientation": "H"},
            {"name": "F", "row": 4, "col": 2, "length": 2, "orientation": "V"},
            {"name": "G", "row": 4, "col": 4, "length": 2, "orientation": "H"},
            {"name": "X", "row": 2, "col": 1, "length": 2, "orientation": "H"}
        ]
    }
    
    # Tạo game instance
    game = RushHourGame()
    
    # Load puzzle
    print("Loading puzzle...")
    game.load_puzzle(puzzle_data)
    
    # Hiển thị trạng thái ban đầu
    print("\nInitial state:")
    print(game.current_state.display_board())
    print("\nGame info:", game.get_game_info())
    
    # Test các thuật toán
    algorithms = ['BFS', 'DFS', 'UCS', 'A*']
    
    for algorithm in algorithms:
        print(f"\n{'='*50}")
        print(f"Solving with {algorithm}...")
        print('='*50)
        
        try:
            solution, stats = game.solve_puzzle(algorithm)
            
            if solution:
                print(f"✅ Solution found!")
                print(f"Number of moves: {len(solution)}")
                print(f"Nodes explored: {stats['nodes_explored']}")
                print(f"Execution time: {stats['execution_time']:.4f} seconds")
                print(f"Max queue size: {stats['max_queue_size']}")
                
                print(f"\nSolution moves:")
                for i, (vehicle, direction) in enumerate(solution, 1):
                    print(f"{i:2d}. Move {vehicle} {direction}")
                
                # Hiển thị một vài bước đầu của solution
                print(f"\nFirst few steps of solution:")
                step_count = 0
                for state in game.animate_solution():
                    print(f"Step {step_count}:")
                    print(state.display_board())
                    print()
                    step_count += 1
                    if step_count > 3:  # Chỉ hiện 4 bước đầu
                        print("... (showing first 4 steps only)")
                        break
                        
            else:
                print(f"❌ No solution found")
                print(f"Nodes explored: {stats['nodes_explored']}")
                print(f"Execution time: {stats['execution_time']:.4f} seconds")
                
        except Exception as e:
            print(f"❌ Error solving with {algorithm}: {e}")
    
    # Test manual moves
    print(f"\n{'='*50}")
    print("Testing manual moves...")
    print('='*50)
    
    game.reset_puzzle()
    print("Possible moves:", game.get_possible_moves())
    
    # Thử một vài moves
    test_moves = [("X", "right"), ("B", "left"), ("A", "left")]
    
    for vehicle, direction in test_moves:
        print(f"\nTrying to move {vehicle} {direction}...")
        if game.make_move(vehicle, direction):
            print(f"✅ Move successful!")
            print("Current state:")
            print(game.current_state.display_board())
            print(f"Is solved: {game.is_solved()}")
        else:
            print(f"❌ Move failed!")
    
    print(f"\nMove history: {game.move_history}")

if __name__ == "__main__":
    main()
