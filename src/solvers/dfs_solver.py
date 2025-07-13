from solvers.base_solver import BaseSolver
import time

class DFSSolver(BaseSolver):
    def solve(self):
        start = time.time()
        stack = [(self.initial_state, [])]
        visited = set()
        expanded = 0
        max_space = 0

        while stack:
            state, path = stack.pop()
            key = tuple(state)
            if key in visited:
                continue
            visited.add(key)

            max_space = max(max_space, len(stack) + len(visited))

            if self.is_goal(state):
                return {
                    "time": time.time() - start,
                    "space": max_space,
                    "expanded": expanded,
                    "path": path + [state]
                }

            for neighbor in self.expand(state):
                stack.append((neighbor, path + [state]))
            expanded += 1

        return {
            "time": time.time() - start,
            "space": max_space,
            "expanded": expanded,
            "path": []
        }
