import copy

class Board:
    def __init__(self, size, vehicles):
        self.rows, self.cols = size
        self.vehicles = {v.name: v for v in vehicles}

    def clone(self):
        return Board((self.rows, self.cols), [v.clone() for v in self.vehicles.values()])

    def get_state_key(self):
        return tuple((v.name, v.row, v.col) for v in sorted(self.vehicles.values(), key=lambda x: x.name))

    def is_goal(self):
        x = self.vehicles['X']
        return x.col + x.length == self.cols

    def get_grid(self):
        grid = [['.' for _ in range(self.cols)] for _ in range(self.rows)]
        for v in self.vehicles.values():
            for r, c in v.get_cells():
                grid[r][c] = v.name
        return grid

    def get_neighbors(self):
        neighbors = []
        grid = self.get_grid()
        for v in self.vehicles.values():
            for delta in [-1, 1]:
                new_board = self.clone()
                new_v = new_board.vehicles[v.name]
                if v.orientation == 'H':
                    new_col = new_v.col + delta
                    tail_col = new_col + new_v.length - 1
                    if 0 <= new_col and tail_col < self.cols:
                        check_col = new_col if delta == -1 else tail_col
                        if grid[new_v.row][check_col] == '.':
                            new_v.col = new_col
                            neighbors.append((new_board, (v.name, delta)))
                else:
                    new_row = new_v.row + delta
                    tail_row = new_row + new_v.length - 1
                    if 0 <= new_row and tail_row < self.rows:
                        check_row = new_row if delta == -1 else tail_row
                        if grid[check_row][new_v.col] == '.':
                            new_v.row = new_row
                            neighbors.append((new_board, (v.name, delta)))
        return neighbors