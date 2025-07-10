from solvers.base_solver import BaseSolver
import heapq
import time

class UCSSolver(BaseSolver):
    def solve(self):
        start = time.time()
        heap = []
        counter = 0
        heapq.heappush(heap, (0, counter, self.initial_state, []))
        visited = set()
        expanded = 0

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
                    "expanded": expanded
                }

            for neighbor in self.expand(state):
                counter += 1
                heapq.heappush(heap, (cost + 1, counter, neighbor, path + [state]))
            expanded += 1

        return {
            "time": time.time() - start,
            "space": len(visited),
            "expanded": expanded
        }
