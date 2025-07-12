"""
Rush Hour Puzzle Game Implementation
Main game class that coordinates all components
"""

from .vehicle import RushHourVehicle
from .state import RushHourState
from .solver import get_solver
import json

class RushHourGame:
    def __init__(self):
        self.current_state = None
        self.initial_state = None
        self.solution = None
        self.solution_stats = None
        self.move_history = []
        
    def load_puzzle(self, puzzle_data):
        """
        Load a puzzle from data
        
        Args:
            puzzle_data (dict): Puzzle configuration with size and vehicles
        """
        board_size = puzzle_data["size"][0]  # Assuming square board
        vehicles = []
        
        for vehicle_data in puzzle_data["vehicles"]:
            vehicle = RushHourVehicle(
                name=vehicle_data["name"],
                row=vehicle_data["row"],
                col=vehicle_data["col"],
                length=vehicle_data["length"],
                orientation=vehicle_data["orientation"]
            )
            vehicles.append(vehicle)
        
        self.initial_state = RushHourState(vehicles, board_size)
        self.current_state = RushHourState(vehicles, board_size)
        self.move_history = []
        
    def load_puzzle_from_file(self, file_path):
        """
        Load puzzle from JSON file
        
        Args:
            file_path (str): Path to JSON file containing puzzle data
        """
        with open(file_path, 'r') as f:
            puzzle_data = json.load(f)
        self.load_puzzle(puzzle_data)
    
    def solve_puzzle(self, algorithm='BFS'):
        """
        Solve the current puzzle using specified algorithm
        
        Args:
            algorithm (str): Algorithm to use ('BFS', 'DFS', 'UCS', 'A*')
            
        Returns:
            tuple: (solution_path, statistics) or (None, statistics) if no solution
        """
        if not self.initial_state:
            raise ValueError("No puzzle loaded")
        
        solver = get_solver(algorithm)
        self.solution, self.solution_stats = solver.solve(self.initial_state)
        
        return self.solution, self.solution_stats
    
    def make_move(self, vehicle_name, direction):
        """
        Make a move in the current game state
        
        Args:
            vehicle_name (str): Name of vehicle to move
            direction (str): Direction to move ('up', 'down', 'left', 'right')
            
        Returns:
            bool: True if move was successful, False otherwise
        """
        if not self.current_state:
            return False
        
        possible_moves = self.current_state.get_possible_moves()
        
        if (vehicle_name, direction) in possible_moves:
            self.current_state = self.current_state.make_move(vehicle_name, direction)
            self.move_history.append((vehicle_name, direction))
            return True
        
        return False
    
    def undo_move(self):
        """
        Undo the last move
        
        Returns:
            bool: True if undo was successful, False if no moves to undo
        """
        if not self.move_history or not self.initial_state:
            return False
        
        # Recreate state by replaying all moves except the last one
        self.move_history.pop()
        self.current_state = RushHourState(
            self.initial_state.vehicles, 
            self.initial_state.board_size
        )
        
        for vehicle_name, direction in self.move_history:
            self.current_state = self.current_state.make_move(vehicle_name, direction)
        
        return True
    
    def reset_puzzle(self):
        """Reset puzzle to initial state"""
        if self.initial_state:
            self.current_state = RushHourState(
                self.initial_state.vehicles,
                self.initial_state.board_size
            )
            self.move_history = []
    
    def is_solved(self):
        """
        Check if current state is solved
        
        Returns:
            bool: True if puzzle is solved
        """
        return self.current_state and self.current_state.is_goal_state()
    
    def get_board_representation(self):
        """
        Get current board state for display
        
        Returns:
            list: 2D list representing the board
        """
        return self.current_state.board if self.current_state else None
    
    def get_possible_moves(self):
        """
        Get all possible moves from current state
        
        Returns:
            list: List of (vehicle_name, direction) tuples
        """
        return self.current_state.get_possible_moves() if self.current_state else []
    
    def get_solution_summary(self):
        """
        Get summary of the solution
        
        Returns:
            dict: Summary including moves count, algorithm stats
        """
        if not self.solution or not self.solution_stats:
            return None
        
        return {
            'solution_found': self.solution is not None,
            'moves_count': len(self.solution) if self.solution else 0,
            'solution_moves': self.solution,
            'statistics': self.solution_stats
        }
    
    def animate_solution(self):
        """
        Generator that yields each state in the solution sequence
        
        Yields:
            RushHourState: Each state in the solution path
        """
        if not self.solution or not self.initial_state:
            return
        
        current_state = RushHourState(
            self.initial_state.vehicles,
            self.initial_state.board_size
        )
        
        yield current_state
        
        for vehicle_name, direction in self.solution:
            current_state = current_state.make_move(vehicle_name, direction)
            yield current_state
    
    def get_game_info(self):
        """
        Get current game information
        
        Returns:
            dict: Game state information
        """
        if not self.current_state:
            return None
        
        return {
            'board_size': self.current_state.board_size,
            'vehicles_count': len(self.current_state.vehicles),
            'moves_made': len(self.move_history),
            'is_solved': self.is_solved(),
            'possible_moves_count': len(self.get_possible_moves())
        }
