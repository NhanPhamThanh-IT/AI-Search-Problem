import time
import heapq
from .base_solver import BaseSolver

def manhattan_heuristic(board):
    red = board.vehicles["X"]
    right_edge = board.cols - 1
    red_end = red.col + red.length - 1
    return right_edge - red_end

class AStarSolver(BaseSolver):
    def solve(self):
        start_time = time.time()
        counter = 0
        heap = []
        g_costs = {}
        start_key = self.initial_board.get_state_key()
        g_costs[start_key] = 0
        f = manhattan_heuristic(self.initial_board)

        heapq.heappush(heap, (f, counter, self.initial_board, []))
        visited = set()

        while heap:
            f_score, _, current_board, path = heapq.heappop(heap)
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
                g = g_costs[state_key] + move_cost
                h = manhattan_heuristic(neighbor)
                f = g + h
                counter += 1
                neighbor_key = neighbor.get_state_key()

                if neighbor_key not in g_costs or g < g_costs[neighbor_key]:
                    g_costs[neighbor_key] = g
                    heapq.heappush(heap, (f, counter, neighbor, path + [move]))

        self.time_taken = time.time() - start_time
