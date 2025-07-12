from solvers.base_solver import BaseSolver
import heapq
import time

class UCSSolver(BaseSolver):
    def solve(self):
        start = time.time()
        heap = [(0, 0, self.initial_state, [])]
        visited = set()
        expanded = 0
        counter = 0

        while heap:
            cost, _, state, path = heapq.heappop(heap)
            key = tuple(state)
            if key in visited:
                continue
            visited.add(key)

            if self.is_goal(state):
                return {
                    "time": time.time() - start,
                    "space": len(visited),
                    "expanded": expanded,
                    "path": path
                }

            for neighbor in self.expand(state):
                counter += 1
                new_cost = cost + 1
                heapq.heappush(heap, (new_cost, counter, neighbor, path + [state]))
            expanded += 1

        return {
            "time": time.time() - start,
            "space": len(visited),
            "expanded": expanded,
            "path": []
        }