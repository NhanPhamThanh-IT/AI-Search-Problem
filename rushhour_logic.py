import heapq
from copy import deepcopy

class RushHourVehicle:
    def __init__(self, name, positions):
        self.name = name
        self.positions = sorted(positions)
        self.length = len(positions)
        self.orientation = self.get_orientation()

    def get_orientation(self):
        if all(i == self.positions[0][0] for i, _ in self.positions):
            return 'H'
        else:
            return 'V'

class RushHourState:
    def __init__(self, board):
        self.board = [row[:] for row in board]
        self.vehicles = self._extract_vehicles()

    def _extract_vehicles(self):
        cars = {}
        for i, row in enumerate(self.board):
            for j, cell in enumerate(row):
                if cell != '.' and cell != ' ':
                    if cell not in cars:
                        cars[cell] = []
                    cars[cell].append((i, j))
        return {name: RushHourVehicle(name, pos) for name, pos in cars.items()}

    def is_goal(self):
        if 'X' not in self.vehicles:
            return False
        vehicle = self.vehicles['X']
        if vehicle.orientation == 'H':
            return any(j == len(self.board[0]) - 1 for i, j in vehicle.positions)
        else:
            return any(i == len(self.board) - 1 for i, j in vehicle.positions)

    def successors(self):
        succs = []
        for car, vehicle in self.vehicles.items():
            if vehicle.orientation == 'H':
                min_i, min_j = min(vehicle.positions)
                if min_j > 0 and self.board[min_i][min_j-1] == '.':
                    new_board = deepcopy(self.board)
                    for i, j in vehicle.positions:
                        new_board[i][j-1] = car
                        new_board[i][j] = '.'
                    succs.append((RushHourState(new_board), f"{car} left", vehicle.length))
                max_i, max_j = max(vehicle.positions)
                if max_j < len(self.board[0])-1 and self.board[max_i][max_j+1] == '.':
                    new_board = deepcopy(self.board)
                    for i, j in reversed(vehicle.positions):
                        new_board[i][j+1] = car
                        new_board[i][j] = '.'
                    succs.append((RushHourState(new_board), f"{car} right", vehicle.length))
            else:
                min_i, min_j = min(vehicle.positions)
                if min_i > 0 and self.board[min_i-1][min_j] == '.':
                    new_board = deepcopy(self.board)
                    for i, j in vehicle.positions:
                        new_board[i-1][j] = car
                        new_board[i][j] = '.'
                    succs.append((RushHourState(new_board), f"{car} up", vehicle.length))
                max_i, max_j = max(vehicle.positions)
                if max_i < len(self.board)-1 and self.board[max_i+1][max_j] == '.':
                    new_board = deepcopy(self.board)
                    for i, j in reversed(vehicle.positions):
                        new_board[i+1][j] = car
                        new_board[i][j] = '.'
                    succs.append((RushHourState(new_board), f"{car} down", vehicle.length))
        return succs

    def __hash__(self):
        return hash(tuple(tuple(row) for row in self.board))

    def __eq__(self, other):
        return self.board == other.board

    def __str__(self):
        return '\n'.join(' '.join(row) for row in self.board)

class RushHourSolver:
    def __init__(self, map_file):
        self.initial_state = self._read_map(map_file)

    def _read_map(self, filename):
        with open(filename, 'r') as f:
            lines = [line.strip().split() for line in f.readlines()]
        return RushHourState(lines)

    def solve_ucs(self):
        heap = []
        counter = 0
        heapq.heappush(heap, (0, counter, self.initial_state, []))
        visited = set()
        while heap:
            cost, _, state, path = heapq.heappop(heap)
            if state in visited:
                continue
            visited.add(state)
            if state.is_goal():
                return path + [(state, None, 0)], cost
            for next_state, action, move_cost in state.successors():
                counter += 1
                heapq.heappush(heap, (cost+move_cost, counter, next_state, path + [(state, action, move_cost)]))
        return None, None 
    
    # [HHLoc] BFSs solution
    def solve_bfs(self):                    # Output: path + the last state, cost
        queue = [(self.initial_state, [])]  # A list that stores tuples: (current_state, path)
        visited = set()                     # A set that stores explored states

        while queue:
            state, path = queue.pop(0)      # Take the fist state and path from queue
            if state in visited:            # Continue if the current state is visited
                continue
            visited.add(state)              # Add the current state to visited
            if state.is_goal():             # Return if the current state is goal
                return path + [(state, None, 0)], len(path)
                                            # Add the current state's successors to queue
            for next_state, action, _ in state.successors():
                queue.append((next_state, path + [(state, action, 1)])) 
        return None, None                   # Return if no goal is found
    
    # [HHLoc] DFSs solution
    def solve_dfs(self):                    # Output: path + the last state, cost
        stack = [(self.initial_state, [])]  # A stack that stores tuples: (current_state, path)
        visited = set()                     # A set that stores explored states
        while stack:
            state, path = stack.pop()       # Take the last state and path from stack
            if state in visited:            # Continue if the current state is visited
                continue
            visited.add(state)              # Add the current state to visited
            if state.is_goal():             # Return if the current state is goal
                return path + [(state, None, 0)], len(path)
                                            # Add the current state's successors to stack
            for next_state, action, _ in reversed(state.successors()):
                stack.append((next_state, path + [(state, action, 1)]))
        return None, None                   # Return if no goal is found
    
    def heuristic(self, state):
        # Heuristic: count the number of blocking vehicles in front of 'X' to the exit
        if 'X' not in state.vehicles:
            return 0
        vehicle = state.vehicles['X']
        if vehicle.orientation != 'H':
            return 0  # Only handle horizontal 'X'
        row = vehicle.positions[0][0]
        max_j = max(j for i, j in vehicle.positions)
        count = 0
        for j in range(max_j + 1, len(state.board[0])):
            cell = state.board[row][j]
            if cell != '.' and cell != ' ':
                count += 1
        return count

    def solve_AStar(self):
        heap = []
        counter = 0
        start_h = self.heuristic(self.initial_state)
        heapq.heappush(heap, (start_h, 0, counter, self.initial_state, []))  # (f, g, counter, state, path)
        visited = set()
        while heap:
            f, g, _, state, path = heapq.heappop(heap)
            if state in visited:
                continue
            visited.add(state)
            if state.is_goal():
                return path + [(state, None, 0)], g
            for next_state, action, move_cost in state.successors():
                if next_state in visited:
                    continue
                counter += 1
                new_g = g + move_cost
                h = self.heuristic(next_state)
                heapq.heappush(heap, (new_g + h, new_g, counter, next_state, path + [(state, action, move_cost)]))
        return None, None


