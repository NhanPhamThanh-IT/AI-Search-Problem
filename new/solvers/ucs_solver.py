import time
import heapq
from .base_solver import BaseSolver

class UCSSolver(BaseSolver):
    def solve(self):
        start_time = time.time()
        counter = 0
        heap = []
        heapq.heappush(heap, (0, counter, self.initial_board, []))
        visited = set()

        while heap:
            cost, _, current_board, path = heapq.heappop(heap)
            state_key = current_board.get_state_key()
            if state_key in visited:
                continue
            visited.add(state_key)

            self.expanded_nodes += 1

            if current_board.is_goal():
                self.solution = path
                break

            for neighbor, move in current_board.get_neighbors():
                move_cost = neighbor.vehicles[move[0]].length
                counter += 1
                heapq.heappush(heap, (cost + move_cost, counter, neighbor, path + [move]))

        self.time_taken = time.time() - start_time
