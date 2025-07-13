from solvers.base_solver import BaseSolver
from collections import deque
import time

class BFSSolver(BaseSolver):
    def solve(self):
        start = time.time()
        queue = deque([(self.initial_state, [])])
        visited = set()
        expanded = 0
        max_space = 0

        while queue:
            state, path = queue.popleft()
            key = tuple(state)
            if key in visited:
                continue
            visited.add(key)

            max_space = max(max_space, len(queue) + len(visited))

            if self.is_goal(state):
                return {
                    "time": time.time() - start,
                    "space": max_space,
                    "expanded": expanded,
                    "path": path + [state]
                }

            for neighbor in self.expand(state):
                queue.append((neighbor, path + [state]))
            expanded += 1

        return {
            "time": time.time() - start,
            "space": max_space,
            "expanded": expanded,
            "path": []
        }
