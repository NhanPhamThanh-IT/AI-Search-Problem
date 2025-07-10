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
                if v[1] + v[2] == self.board.size[1]:  # col + length == width
                    return True
        return False

    def expand(self, state):
        # Giả lập đơn giản: không sinh các state thật, placeholder
        return []

    def solve(self):
        raise NotImplementedError
