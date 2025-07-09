import time
from collections import deque
from .base_solver import BaseSolver

class BFSSolver(BaseSolver):
    def solve(self):
        start_time = time.time()
        visited = set()
        queue = deque()
        queue.append((self.initial_board, []))

        while queue:
            current_board, path = queue.popleft()
            state_key = current_board.get_state_key()
            if state_key in visited:
                continue
            visited.add(state_key)

            self.expanded_nodes += 1

            if current_board.is_goal():
                self.solution = path
                break

            for neighbor, move in current_board.get_neighbors():
                queue.append((neighbor, path + [move]))

        self.time_taken = time.time() - start_time
