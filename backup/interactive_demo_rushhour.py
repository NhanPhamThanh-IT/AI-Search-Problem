"""
Interactive Console Demo for Rush Hour Puzzle Solver
Enhanced version with interactive features
"""

import sys
import os
import time
from typing import List, Tuple, Optional

sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from rushhour import RushHourGame

class RushHourInteractiveDemo:
    def __init__(self):
        self.game = RushHourGame()
        self.load_demo_puzzle()
        
    def load_demo_puzzle(self):
        """Load the demo puzzle data"""
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
        
        self.game.load_puzzle(puzzle_data)
        
    def display_menu(self):
        """Display the main menu"""
        print("\n" + "="*60)
        print("🚗 RUSH HOUR PUZZLE SOLVER - INTERACTIVE DEMO 🚗")
        print("="*60)
        print("1. View current puzzle state")
        print("2. Solve with algorithm")
        print("3. Interactive solving mode")
        print("4. View solution animation")
        print("5. Test manual moves")
        print("6. Reset puzzle")
        print("7. Compare all algorithms")
        print("0. Exit")
        print("-"*60)
        
    def display_current_state(self):
        """Display current puzzle state"""
        print("\n🎯 Current Puzzle State:")
        print(self.game.current_state.display_board())
        print(f"\nIs solved: {'✅ YES' if self.game.is_solved() else '❌ NO'}")
        if self.game.move_history:
            print(f"Moves made: {len(self.game.move_history)}")
            print(f"Last moves: {self.game.move_history[-3:] if len(self.game.move_history) > 3 else self.game.move_history}")
        
    def solve_with_algorithm_menu(self):
        """Algorithm selection and solving"""
        print("\n🔍 Choose Algorithm:")
        algorithms = ['BFS', 'DFS', 'UCS', 'A*']
        
        for i, algo in enumerate(algorithms, 1):
            print(f"{i}. {algo}")
        print("0. Back to main menu")
        
        try:
            choice = int(input("\nEnter choice (0-4): "))
            if choice == 0:
                return
            elif 1 <= choice <= 4:
                algorithm = algorithms[choice - 1]
                self.solve_puzzle(algorithm)
            else:
                print("❌ Invalid choice!")
        except ValueError:
            print("❌ Please enter a valid number!")
            
    def solve_puzzle(self, algorithm):
        """Solve puzzle with given algorithm"""
        print(f"\n🔄 Solving with {algorithm}...")
        print("Please wait...")
        
        start_time = time.time()
        try:
            solution, stats = self.game.solve_puzzle(algorithm)
            end_time = time.time()
            
            print(f"\n{'='*50}")
            print(f"📊 RESULTS FOR {algorithm}")
            print('='*50)
            
            if solution:
                print(f"✅ Solution found!")
                print(f"📏 Number of moves: {len(solution)}")
                print(f"🔍 Nodes explored: {stats['nodes_explored']}")
                print(f"⏱️  Execution time: {stats['execution_time']:.4f} seconds")
                print(f"📦 Max queue size: {stats['max_queue_size']}")
                
                print(f"\n📋 Solution moves:")
                for i, (vehicle, direction) in enumerate(solution, 1):
                    print(f"{i:2d}. Move {vehicle} {direction}")
                    
                # Ask if user wants to see animation
                choice = input("\n🎬 View step-by-step animation? (y/n): ").lower()
                if choice == 'y':
                    self.animate_solution(solution)
                    
            else:
                print(f"❌ No solution found")
                print(f"🔍 Nodes explored: {stats['nodes_explored']}")
                print(f"⏱️  Execution time: {stats['execution_time']:.4f} seconds")
                
        except Exception as e:
            print(f"❌ Error solving with {algorithm}: {e}")
            
    def animate_solution(self, solution):
        """Animate the solution step by step"""
        if not solution:
            print("❌ No solution to animate!")
            return
            
        print(f"\n🎬 Animating solution ({len(solution)} moves)")
        print("Press Enter to continue each step, 'q' to quit animation")
        
        self.game.reset_puzzle()
        print(f"\n📍 Initial state:")
        print(self.game.current_state.display_board())
        
        for i, (vehicle, direction) in enumerate(solution):
            user_input = input(f"\nStep {i+1}: Press Enter to move {vehicle} {direction} (or 'q' to quit): ")
            if user_input.lower() == 'q':
                break
                
            if self.game.make_move(vehicle, direction):
                print(f"✅ Move {i+1}: {vehicle} moved {direction}")
                print(self.game.current_state.display_board())
                
                if self.game.is_solved():
                    print("\n🎉 PUZZLE SOLVED! 🎉")
                    break
            else:
                print(f"❌ Failed to move {vehicle} {direction}")
                
        self.game.reset_puzzle()
        
    def interactive_solving_mode(self):
        """Interactive mode where user can try moves"""
        print("\n🎮 Interactive Solving Mode")
        print("Try to solve the puzzle manually!")
        print("Commands: 'move <vehicle> <direction>', 'hint', 'reset', 'quit'")
        print("Example: move X right")
        
        self.game.reset_puzzle()
        
        while not self.game.is_solved():
            print(f"\n📍 Current state:")
            print(self.game.current_state.display_board())
            print(f"Moves made: {len(self.game.move_history)}")
            
            possible_moves = self.game.get_possible_moves()
            print(f"💡 Possible moves: {len(possible_moves)}")
            
            command = input("\n> ").strip().lower()
            
            if command == 'quit':
                break
            elif command == 'reset':
                self.game.reset_puzzle()
                print("🔄 Puzzle reset!")
                continue
            elif command == 'hint':
                self.show_hint()
                continue
            elif command.startswith('move '):
                self.handle_manual_move(command)
            else:
                print("❌ Invalid command! Use: move <vehicle> <direction>, hint, reset, or quit")
                
        if self.game.is_solved():
            print("\n🎉 CONGRATULATIONS! You solved the puzzle! 🎉")
            print(f"Total moves: {len(self.game.move_history)}")
            
    def handle_manual_move(self, command):
        """Handle manual move command"""
        try:
            parts = command.split()
            if len(parts) != 3:
                print("❌ Invalid format! Use: move <vehicle> <direction>")
                return
                
            vehicle = parts[1].upper()
            direction = parts[2].lower()
            
            if direction not in ['left', 'right', 'up', 'down']:
                print("❌ Invalid direction! Use: left, right, up, down")
                return
                
            if self.game.make_move(vehicle, direction):
                print(f"✅ Move successful: {vehicle} moved {direction}")
            else:
                print(f"❌ Cannot move {vehicle} {direction}")
                
        except Exception as e:
            print(f"❌ Error processing move: {e}")
            
    def show_hint(self):
        """Show a hint for the next move"""
        try:
            # Try to get a quick solution
            solution, _ = self.game.solve_puzzle('BFS')
            if solution and len(solution) > 0:
                vehicle, direction = solution[0]
                print(f"💡 Hint: Try moving {vehicle} {direction}")
            else:
                print("💡 No hint available - puzzle might already be solved!")
        except:
            print("💡 Unable to generate hint at this time")
            
    def compare_all_algorithms(self):
        """Compare performance of all algorithms"""
        print("\n📊 Comparing All Algorithms...")
        print("This may take a moment...")
        
        algorithms = ['BFS', 'DFS', 'UCS', 'A*']
        results = {}
        
        for algorithm in algorithms:
            print(f"Testing {algorithm}...")
            try:
                solution, stats = self.game.solve_puzzle(algorithm)
                results[algorithm] = {
                    'solution_found': solution is not None,
                    'moves': len(solution) if solution else 0,
                    'nodes_explored': stats['nodes_explored'],
                    'execution_time': stats['execution_time'],
                    'max_queue_size': stats['max_queue_size']
                }
            except Exception as e:
                results[algorithm] = {'error': str(e)}
                
        # Display comparison table
        print(f"\n{'='*80}")
        print("📊 ALGORITHM COMPARISON RESULTS")
        print('='*80)
        print(f"{'Algorithm':<10} {'Solution':<8} {'Moves':<6} {'Nodes':<8} {'Time(s)':<8} {'Queue':<8}")
        print('-'*80)
        
        for algo, result in results.items():
            if 'error' in result:
                print(f"{algo:<10} {'ERROR':<8} {'-':<6} {'-':<8} {'-':<8} {'-':<8}")
            else:
                solution_str = "YES" if result['solution_found'] else "NO"
                print(f"{algo:<10} {solution_str:<8} {result['moves']:<6} "
                     f"{result['nodes_explored']:<8} {result['execution_time']:<8.4f} "
                     f"{result['max_queue_size']:<8}")
                     
        print('='*80)
        
    def test_manual_moves(self):
        """Test some predefined manual moves"""
        print("\n🔧 Testing Manual Moves...")
        
        self.game.reset_puzzle()
        print("Initial state:")
        print(self.game.current_state.display_board())
        
        test_moves = [("X", "right"), ("B", "left"), ("A", "left"), ("X", "right")]
        
        print(f"\nTesting moves: {test_moves}")
        
        for i, (vehicle, direction) in enumerate(test_moves, 1):
            print(f"\n--- Move {i}: {vehicle} {direction} ---")
            
            if self.game.make_move(vehicle, direction):
                print(f"✅ Move successful!")
                print("Current state:")
                print(self.game.current_state.display_board())
                print(f"Is solved: {'✅ YES' if self.game.is_solved() else '❌ NO'}")
                
                if self.game.is_solved():
                    print("🎉 Puzzle solved during testing!")
                    break
            else:
                print(f"❌ Move failed!")
                
        print(f"\nMove history: {self.game.move_history}")
        self.game.reset_puzzle()
        
    def run(self):
        """Main demo loop"""
        print("🚗 Welcome to Rush Hour Puzzle Solver Interactive Demo! 🚗")
        
        while True:
            self.display_menu()
            
            try:
                choice = input("Enter your choice (0-7): ").strip()
                
                if choice == '0':
                    print("👋 Thanks for using Rush Hour Solver! Goodbye!")
                    break
                elif choice == '1':
                    self.display_current_state()
                elif choice == '2':
                    self.solve_with_algorithm_menu()
                elif choice == '3':
                    self.interactive_solving_mode()
                elif choice == '4':
                    # Quick solve and animate
                    solution, _ = self.game.solve_puzzle('BFS')
                    if solution:
                        self.animate_solution(solution)
                    else:
                        print("❌ No solution found to animate!")
                elif choice == '5':
                    self.test_manual_moves()
                elif choice == '6':
                    self.game.reset_puzzle()
                    print("🔄 Puzzle reset to initial state!")
                elif choice == '7':
                    self.compare_all_algorithms()
                else:
                    print("❌ Invalid choice! Please try again.")
                    
                input("\nPress Enter to continue...")
                
            except KeyboardInterrupt:
                print("\n\n👋 Interrupted by user. Goodbye!")
                break
            except Exception as e:
                print(f"❌ Unexpected error: {e}")
                input("Press Enter to continue...")

def main():
    """Run the interactive console demo"""
    try:
        demo = RushHourInteractiveDemo()
        demo.run()
    except Exception as e:
        print(f"Error running interactive demo: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    main()
