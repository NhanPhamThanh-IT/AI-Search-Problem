"""Rush Hour puzzle logic and solver algorithms."""

import heapq
from copy import deepcopy
from typing import List, Tuple, Optional, Set, Dict


class RushHourVehicle:
    """Represents a vehicle in the Rush Hour puzzle."""
    
    def __init__(self, name: str, positions: List[Tuple[int, int]]):
        """Initialize a vehicle with name and positions."""
        self.name = name
        self.positions = sorted(positions)
        self.length = len(positions)
        self.orientation = self._get_orientation()

    def _get_orientation(self) -> str:
        """Determine if vehicle is horizontal ('H') or vertical ('V')."""
        if all(i == self.positions[0][0] for i, _ in self.positions):
            return 'H'
        else:
            return 'V'


class RushHourState:
    """Represents a state in the Rush Hour puzzle."""
    
    def __init__(self, board: List[List[str]]):
        """Initialize state with board configuration."""
        self.board = [row[:] for row in board]
        self.vehicles = self._extract_vehicles()

    def _extract_vehicles(self) -> Dict[str, RushHourVehicle]:
        """Extract vehicle information from the board."""
        vehicle_positions = {}
        
        for i, row in enumerate(self.board):
            for j, cell in enumerate(row):
                if cell != '.' and cell != ' ':
                    if cell not in vehicle_positions:
                        vehicle_positions[cell] = []
                    vehicle_positions[cell].append((i, j))
        
        return {
            name: RushHourVehicle(name, positions) 
            for name, positions in vehicle_positions.items()
        }

    def is_goal(self) -> bool:
        """Check if the target vehicle 'X' has reached the goal."""
        if 'X' not in self.vehicles:
            return False
        
        vehicle = self.vehicles['X']
        
        if vehicle.orientation == 'H':
            # Check if any part of X is at the rightmost column
            return any(j == len(self.board[0]) - 1 for i, j in vehicle.positions)
        else:
            # Check if any part of X is at the bottom row
            return any(i == len(self.board) - 1 for i, j in vehicle.positions)

    def get_successors(self) -> List[Tuple['RushHourState', str, int]]:
        """Get all possible successor states."""
        successors = []
        
        for vehicle_name, vehicle in self.vehicles.items():
            successors.extend(self._get_vehicle_moves(vehicle_name, vehicle))
        
        return successors
    
    def _get_vehicle_moves(self, vehicle_name: str, vehicle: RushHourVehicle) -> List[Tuple['RushHourState', str, int]]:
        """Get all possible moves for a specific vehicle."""
        moves = []
        
        if vehicle.orientation == 'H':
            moves.extend(self._get_horizontal_moves(vehicle_name, vehicle))
        else:
            moves.extend(self._get_vertical_moves(vehicle_name, vehicle))
        
        return moves
    
    def _get_horizontal_moves(self, vehicle_name: str, vehicle: RushHourVehicle) -> List[Tuple['RushHourState', str, int]]:
        """Get horizontal moves (left/right) for a vehicle."""
        moves = []
        
        # Move left
        min_i, min_j = min(vehicle.positions)
        if min_j > 0 and self.board[min_i][min_j - 1] == '.':
            new_state = self._create_moved_state(vehicle, (-1, 0), vehicle_name)
            moves.append((new_state, f"{vehicle_name} left", vehicle.length))
        
        # Move right
        max_i, max_j = max(vehicle.positions)
        if max_j < len(self.board[0]) - 1 and self.board[max_i][max_j + 1] == '.':
            new_state = self._create_moved_state(vehicle, (1, 0), vehicle_name)
            moves.append((new_state, f"{vehicle_name} right", vehicle.length))
        
        return moves
    
    def _get_vertical_moves(self, vehicle_name: str, vehicle: RushHourVehicle) -> List[Tuple['RushHourState', str, int]]:
        """Get vertical moves (up/down) for a vehicle."""
        moves = []
        
        # Move up
        min_i, min_j = min(vehicle.positions)
        if min_i > 0 and self.board[min_i - 1][min_j] == '.':
            new_state = self._create_moved_state(vehicle, (0, -1), vehicle_name)
            moves.append((new_state, f"{vehicle_name} up", vehicle.length))
        
        # Move down
        max_i, max_j = max(vehicle.positions)
        if max_i < len(self.board) - 1 and self.board[max_i + 1][max_j] == '.':
            new_state = self._create_moved_state(vehicle, (0, 1), vehicle_name)
            moves.append((new_state, f"{vehicle_name} down", vehicle.length))
        
        return moves
    
    def _create_moved_state(self, vehicle: RushHourVehicle, direction: Tuple[int, int], vehicle_name: str) -> 'RushHourState':
        """Create a new state with a vehicle moved in the specified direction."""
        new_board = deepcopy(self.board)
        
        # Clear old positions
        for i, j in vehicle.positions:
            new_board[i][j] = '.'
        
        # Set new positions
        if vehicle.orientation == 'H':
            # For horizontal movement, move column-wise
            if direction[0] == -1:  # Moving left
                for i, j in vehicle.positions:
                    new_board[i][j - 1] = vehicle_name
            else:  # Moving right
                for i, j in reversed(vehicle.positions):
                    new_board[i][j + 1] = vehicle_name
        else:
            # For vertical movement, move row-wise
            if direction[1] == -1:  # Moving up
                for i, j in vehicle.positions:
                    new_board[i - 1][j] = vehicle_name
            else:  # Moving down
                for i, j in reversed(vehicle.positions):
                    new_board[i + 1][j] = vehicle_name
        
        return RushHourState(new_board)

    def __hash__(self) -> int:
        """Hash function for state comparison."""
        return hash(tuple(tuple(row) for row in self.board))

    def __eq__(self, other) -> bool:
        """Equality comparison for states."""
        return self.board == other.board

    def __str__(self) -> str:
        """String representation of the state."""
        return '\n'.join(' '.join(row) for row in self.board)


class RushHourSolver:
    """Solver for Rush Hour puzzle using various search algorithms."""
    
    def __init__(self, map_file: str):
        """Initialize solver with map file."""
        self.initial_state = self._read_map(map_file)

    def _read_map(self, filename: str) -> RushHourState:
        """Read and parse the map file."""
        with open(filename, 'r') as f:
            lines = [line.strip().split() for line in f.readlines()]
        return RushHourState(lines)
    
    def solve_bfs(self) -> Tuple[Optional[List], Optional[int], List]:
        """Solve using Breadth-First Search."""
        queue = [(self.initial_state, [])]
        visited = set()
        expanded_nodes = []

        while queue:
            state, path = queue.pop(0)
            
            if state in visited:
                continue
                
            visited.add(state)
            expanded_nodes.append((state, len(path)))
            
            if state.is_goal():
                return path + [(state, None, 0)], len(path), expanded_nodes
            
            for next_state, action, cost in state.get_successors():
                if next_state not in visited:
                    queue.append((next_state, path + [(state, action, cost)]))
        
        return None, None, expanded_nodes
    
    def solve_dfs(self) -> Tuple[Optional[List], Optional[int], List]:
        """Solve using Depth-First Search."""
        stack = [(self.initial_state, [])]
        visited = set()
        expanded_nodes = []
        
        while stack:
            state, path = stack.pop()
            
            if state in visited:
                continue
                
            visited.add(state)
            expanded_nodes.append((state, len(path)))
            
            if state.is_goal():
                return path + [(state, None, 0)], len(path), expanded_nodes
            
            for next_state, action, cost in reversed(state.get_successors()):
                if next_state not in visited:
                    stack.append((next_state, path + [(state, action, cost)]))
        
        return None, None, expanded_nodes
    
    def solve_ucs(self) -> Tuple[Optional[List], Optional[int], List]:
        """Solve using Uniform Cost Search."""
        heap = []
        counter = 0
        heapq.heappush(heap, (0, counter, self.initial_state, []))
        visited = set()
        expanded_nodes = []
        
        while heap:
            cost, _, state, path = heapq.heappop(heap)
            
            if state in visited:
                continue
                
            visited.add(state)
            expanded_nodes.append((state, cost))
            
            if state.is_goal():
                return path + [(state, None, 0)], cost, expanded_nodes
            
            for next_state, action, move_cost in state.get_successors():
                if next_state not in visited:
                    counter += 1
                    new_cost = cost + move_cost
                    heapq.heappush(heap, (new_cost, counter, next_state, path + [(state, action, move_cost)]))
        
        return None, None, expanded_nodes 

    def _calculate_heuristic(self, state: RushHourState) -> int:
        """Calculate heuristic for A* search (number of blocking vehicles)."""
        if 'X' not in state.vehicles:
            return 0
        
        vehicle = state.vehicles['X']
        
        # Only works for horizontal target vehicle
        if vehicle.orientation != 'H':
            return 0
        
        # Count blocking vehicles in the path to exit
        row = vehicle.positions[0][0]
        max_j = max(j for i, j in vehicle.positions)
        
        blocking_count = 0
        for j in range(max_j + 1, len(state.board[0])):
            cell = state.board[row][j]
            if cell != '.' and cell != ' ':
                blocking_count += 1
        
        return blocking_count

    def solve_astar(self) -> Tuple[Optional[List], Optional[int], List]:
        """Solve using A* Search."""
        heap = []
        counter = 0
        start_h = self._calculate_heuristic(self.initial_state)
        heapq.heappush(heap, (start_h, 0, counter, self.initial_state, []))
        visited = set()
        expanded_nodes = []
        
        while heap:
            f_cost, g_cost, _, state, path = heapq.heappop(heap)
            
            if state in visited:
                continue
                
            visited.add(state)
            expanded_nodes.append((state, g_cost, f_cost))
            
            if state.is_goal():
                return path + [(state, None, 0)], g_cost, expanded_nodes
            
            for next_state, action, move_cost in state.get_successors():
                if next_state not in visited:
                    counter += 1
                    new_g = g_cost + move_cost
                    h_cost = self._calculate_heuristic(next_state)
                    f_cost = new_g + h_cost
                    heapq.heappush(heap, (f_cost, new_g, counter, next_state, path + [(state, action, move_cost)]))
        
        return None, None, expanded_nodes


