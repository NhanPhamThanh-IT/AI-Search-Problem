from solvers.base_solver import BaseSolver
import heapq
import time

class AStarSolver(BaseSolver):
    def solve(self):
        start = time.time()
        heap = []
        counter = 0
        heapq.heappush(heap, (0 + self.heuristic(self.initial_state), counter, self.initial_state, []))
        visited = set()
        expanded = 0

        while heap:
            _, _, state, path = heapq.heappop(heap)
            key = tuple(state)
            if key in visited:
                continue
            visited.add(key)

            if self.is_goal(state):
                return {
                    "time": time.time() - start,
                    "space": len(visited),
                    "expanded": expanded
                }

            for neighbor in self.expand(state):
                counter += 1
                cost = len(path) + 1
                heapq.heappush(heap, (cost + self.heuristic(neighbor), counter, neighbor, path + [state]))
            expanded += 1

        return {
            "time": time.time() - start,
            "space": len(visited),
            "expanded": expanded
        }

    def heuristic(self, state):
        # Ước lượng đơn giản: đếm số lượng xe chắn đường xe X
        for v in state:
            if v[4] == "X":
                x_row = v[0]
                x_end_col = v[1] + v[2]
                break
        count = 0
        for v in state:
            if v[0] == x_row and v[1] > x_end_col - 1:
                count += 1
        return count
