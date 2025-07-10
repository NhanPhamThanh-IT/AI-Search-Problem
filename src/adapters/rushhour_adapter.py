"""
Adapter để tích hợp hệ thống Rush Hour mới vào game hiện tại
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from rushhour import RushHourGame, get_solver

class RushHourAdapter:
    """Adapter class để tương thích với hệ thống game hiện tại"""
    
    def __init__(self, map_path, algorithm='BFS'):
        self.game = RushHourGame()
        self.algorithm = algorithm
        self.solution = []
        self.expanded_nodes = 0
        self.time_taken = 0
        
        # Load map
        self.game.load_puzzle_from_file(map_path)
        
        # Solve puzzle
        self._solve()
    
    def _solve(self):
        """Solve the puzzle and store results"""
        solution, stats = self.game.solve_puzzle(self.algorithm)
        
        if solution:
            # Convert solution format từ format mới sang format cũ
            self.solution = []
            for vehicle_name, direction in solution:
                # Convert direction to delta format
                if direction == 'left':
                    delta = -1
                elif direction == 'right':
                    delta = 1
                elif direction == 'up':
                    delta = -1
                elif direction == 'down':
                    delta = 1
                else:
                    delta = 0
                
                self.solution.append((vehicle_name, delta))
            
            self.expanded_nodes = stats['nodes_explored']
            self.time_taken = stats['execution_time']
        else:
            self.solution = []
            self.expanded_nodes = stats['nodes_explored']
            self.time_taken = stats['execution_time']
    
    def get_initial_board(self):
        """Get initial board state in old format"""
        return self._convert_to_old_board_format()
    
    def _convert_to_old_board_format(self):
        """Convert new board format to old format for compatibility"""
        # Create a simple object that mimics the old board structure
        class OldVehicle:
            def __init__(self, name, row, col, length, orientation):
                self.name = name
                self.row = row
                self.col = col
                self.length = length
                self.orientation = orientation
            
            def clone(self):
                return OldVehicle(self.name, self.row, self.col, self.length, self.orientation)
        
        class OldBoard:
            def __init__(self, vehicles):
                self.vehicles = {v.name: v for v in vehicles}
            
            def clone(self):
                cloned_vehicles = [v.clone() for v in self.vehicles.values()]
                return OldBoard(cloned_vehicles)
        
        # Convert vehicles
        old_vehicles = []
        for vehicle in self.game.initial_state.vehicles:
            old_vehicle = OldVehicle(
                vehicle.name, 
                vehicle.row, 
                vehicle.col, 
                vehicle.length, 
                vehicle.orientation
            )
            old_vehicles.append(old_vehicle)
        
        return OldBoard(old_vehicles)


def create_rush_hour_solver(map_path, algorithm='BFS'):
    """
    Factory function để tạo solver tương thích với hệ thống cũ
    
    Args:
        map_path (str): Path to map file
        algorithm (str): Algorithm to use
        
    Returns:
        RushHourAdapter: Solver instance
    """
    return RushHourAdapter(map_path, algorithm)
