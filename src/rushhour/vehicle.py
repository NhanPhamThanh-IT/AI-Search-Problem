"""
Rush Hour Vehicle Class
Represents a vehicle in the Rush Hour puzzle
"""

class RushHourVehicle:
    def __init__(self, name, row, col, length, orientation):
        """
        Initialize a vehicle
        
        Args:
            name (str): Vehicle identifier (e.g., 'A', 'B', 'X')
            row (int): Starting row position
            col (int): Starting column position  
            length (int): Length of the vehicle
            orientation (str): 'H' for horizontal, 'V' for vertical
        """
        self.name = name
        self.row = row
        self.col = col
        self.length = length
        self.orientation = orientation
        
        # Special vehicle 'X' is the target vehicle that needs to reach the exit
        self.is_target = (name == 'X')
    
    def get_occupied_cells(self):
        """
        Get all cells occupied by this vehicle
        
        Returns:
            list: List of (row, col) tuples representing occupied cells
        """
        cells = []
        if self.orientation == 'H':
            for i in range(self.length):
                cells.append((self.row, self.col + i))
        else:  # 'V'
            for i in range(self.length):
                cells.append((self.row + i, self.col))
        return cells
    
    def can_move(self, direction, board_size):
        """
        Check if vehicle can move in the given direction
        
        Args:
            direction (str): 'up', 'down', 'left', 'right'
            board_size (int): Size of the board
            
        Returns:
            bool: True if movement is possible within board bounds
        """
        if self.orientation == 'H':
            if direction == 'left':
                return self.col > 0
            elif direction == 'right':
                return self.col + self.length < board_size
            else:
                return False  # Horizontal vehicles can't move vertically
        else:  # 'V'
            if direction == 'up':
                return self.row > 0
            elif direction == 'down':
                return self.row + self.length < board_size
            else:
                return False  # Vertical vehicles can't move horizontally
    
    def move(self, direction):
        """
        Create a new vehicle instance moved in the given direction
        
        Args:
            direction (str): 'up', 'down', 'left', 'right'
            
        Returns:
            RushHourVehicle: New vehicle instance with updated position
        """
        new_row, new_col = self.row, self.col
        
        if direction == 'up':
            new_row -= 1
        elif direction == 'down':
            new_row += 1
        elif direction == 'left':
            new_col -= 1
        elif direction == 'right':
            new_col += 1
            
        return RushHourVehicle(self.name, new_row, new_col, self.length, self.orientation)
    
    def __eq__(self, other):
        """Check equality based on position and properties"""
        if not isinstance(other, RushHourVehicle):
            return False
        return (self.name == other.name and 
                self.row == other.row and 
                self.col == other.col and
                self.length == other.length and
                self.orientation == other.orientation)
    
    def __hash__(self):
        """Make vehicle hashable for use in sets and dictionaries"""
        return hash((self.name, self.row, self.col, self.length, self.orientation))
    
    def __repr__(self):
        """String representation for debugging"""
        return f"Vehicle({self.name}, {self.row}, {self.col}, {self.length}, {self.orientation})"
