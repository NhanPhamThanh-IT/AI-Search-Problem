class BaseSolver:
    def __init__(self, board):
        self.board = board
        self.initial_state = self.serialize_board(board)

    def serialize_board(self, board):
        return tuple(
            (v.row, v.col, v.length, v.orientation, v.name)
            for v in board.vehicles.values()
        )

    def is_goal(self, state):
        for v in state:
            if v[4] == "X":
                if v[1] + v[2] == self.board.size[1]:
                    return True
        return False

    def expand(self, state):
        next_states = []
        
        board_grid = [[None for _ in range(self.board.size[1])] for _ in range(self.board.size[0])]
        
        for vehicle in state:
            row, col, length, orientation, name = vehicle
            if orientation == 'H':
                for c in range(col, col + length):
                    if 0 <= row < self.board.size[0] and 0 <= c < self.board.size[1]:
                        board_grid[row][c] = name
            else:
                for r in range(row, row + length):
                    if 0 <= r < self.board.size[0] and 0 <= col < self.board.size[1]:
                        board_grid[r][col] = name
        
        for i, vehicle in enumerate(state):
            row, col, length, orientation, name = vehicle
            
            if orientation == 'H':
                new_col = col - 1
                if new_col >= 0 and board_grid[row][new_col] is None:
                    new_state = list(state)
                    new_state[i] = (row, new_col, length, orientation, name)
                    next_states.append(tuple(new_state))
                
                new_col = col + length
                if new_col < self.board.size[1] and board_grid[row][new_col] is None:
                    new_state = list(state)
                    new_state[i] = (row, col + 1, length, orientation, name)
                    next_states.append(tuple(new_state))
            
            else:
                new_row = row - 1
                if new_row >= 0 and board_grid[new_row][col] is None:
                    new_state = list(state)
                    new_state[i] = (new_row, col, length, orientation, name)
                    next_states.append(tuple(new_state))
                
                new_row = row + length
                if new_row < self.board.size[0] and board_grid[new_row][col] is None:
                    new_state = list(state)
                    new_state[i] = (row + 1, col, length, orientation, name)
                    next_states.append(tuple(new_state))
        
        return next_states

    def solve(self):
        raise NotImplementedError
