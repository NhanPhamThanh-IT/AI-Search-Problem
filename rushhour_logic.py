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