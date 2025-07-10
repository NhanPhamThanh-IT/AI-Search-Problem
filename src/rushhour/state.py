"""
Rush Hour State Class
Represents a state of the Rush Hour puzzle board
"""

from .vehicle import RushHourVehicle

class RushHourState:
    def __init__(self, vehicles, board_size):
        """
        Initialize a puzzle state
        
        Args:
            vehicles (list): List of RushHourVehicle objects
            board_size (int): Size of the square board (e.g., 6 for 6x6)
        """
        self.vehicles = vehicles
        self.board_size = board_size
        self.board = self._create_board()
        
    def _create_board(self):
        """
        Create a 2D board representation
        
        Returns:
            list: 2D list where each cell contains vehicle name or None
        """
        board = [[None for _ in range(self.board_size)] for _ in range(self.board_size)]
        
        for vehicle in self.vehicles:
            cells = vehicle.get_occupied_cells()
            for row, col in cells:
                board[row][col] = vehicle.name
                
        return board
    
    def is_goal_state(self):
        """
        Check if this is a goal state (target vehicle X reaches the exit)
        
        Returns:
            bool: True if target vehicle can exit
        """
        target_vehicle = self.get_target_vehicle()
        if not target_vehicle:
            return False
            
        # Target vehicle needs to be in row 2 and able to move right to exit
        if target_vehicle.row == 2:
            # Check if path to exit is clear
            rightmost_col = target_vehicle.col + target_vehicle.length
            return rightmost_col == self.board_size
        
        return False
    
    def get_target_vehicle(self):
        """
        Get the target vehicle (vehicle 'X')
        
        Returns:
            RushHourVehicle: The target vehicle or None if not found
        """
        for vehicle in self.vehicles:
            if vehicle.is_target:
                return vehicle
        return None
    
    def get_possible_moves(self):
        """
        Get all possible moves from current state
        
        Returns:
            list: List of (vehicle_name, direction) tuples for valid moves
        """
        possible_moves = []
        
        for vehicle in self.vehicles:
            directions = []
            if vehicle.orientation == 'H':
                directions = ['left', 'right']
            else:  # 'V'
                directions = ['up', 'down']
                
            for direction in directions:
                if self._can_vehicle_move(vehicle, direction):
                    possible_moves.append((vehicle.name, direction))
                    
        return possible_moves
    
    def _can_vehicle_move(self, vehicle, direction):
        """
        Check if a specific vehicle can move in a direction
        
        Args:
            vehicle (RushHourVehicle): Vehicle to check
            direction (str): Direction to move
            
        Returns:
            bool: True if move is valid
        """
        # Check board boundaries
        if not vehicle.can_move(direction, self.board_size):
            return False
            
        # Check for collisions with other vehicles
        moved_vehicle = vehicle.move(direction)
        moved_cells = moved_vehicle.get_occupied_cells()
        
        for row, col in moved_cells:
            if self.board[row][col] is not None and self.board[row][col] != vehicle.name:
                return False
                
        return True
    
    def make_move(self, vehicle_name, direction):
        """
        Create a new state by moving a vehicle
        
        Args:
            vehicle_name (str): Name of vehicle to move
            direction (str): Direction to move
            
        Returns:
            RushHourState: New state after the move
        """
        new_vehicles = []
        
        for vehicle in self.vehicles:
            if vehicle.name == vehicle_name:
                new_vehicles.append(vehicle.move(direction))
            else:
                new_vehicles.append(RushHourVehicle(
                    vehicle.name, vehicle.row, vehicle.col, 
                    vehicle.length, vehicle.orientation
                ))
                
        return RushHourState(new_vehicles, self.board_size)
    
    def get_state_hash(self):
        """
        Get a hash representation of the state for duplicate detection
        
        Returns:
            str: String representation of vehicle positions
        """
        vehicle_positions = []
        for vehicle in sorted(self.vehicles, key=lambda v: v.name):
            vehicle_positions.append(f"{vehicle.name}:{vehicle.row},{vehicle.col}")
        return "|".join(vehicle_positions)
    
    def __eq__(self, other):
        """Check if two states are equal"""
        if not isinstance(other, RushHourState):
            return False
        return self.get_state_hash() == other.get_state_hash()
    
    def __hash__(self):
        """Make state hashable"""
        return hash(self.get_state_hash())
    
    def display_board(self):
        """
        Display the board in a readable format
        
        Returns:
            str: String representation of the board
        """
        display = []
        for row in self.board:
            row_str = " ".join([cell if cell else "." for cell in row])
            display.append(row_str)
        return "\n".join(display)
    
    def __repr__(self):
        """String representation for debugging"""
        return f"RushHourState(hash={self.get_state_hash()})"
