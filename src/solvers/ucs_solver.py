from solvers.base_solver import BaseSolver
import heapq
import time

class UCSSolver(BaseSolver):
    def get_move_cost(self, from_state, to_state):
        """Calculate cost based on the length of the vehicle that moved"""
        for i, (from_vehicle, to_vehicle) in enumerate(zip(from_state, to_state)):
            if from_vehicle != to_vehicle:
                _, _, length, _, _ = to_vehicle
                return length
        return 1
    
    def solve(self):
        start = time.time()
        heap = [(0, 0, self.initial_state, [])]
        visited = set()
        expanded = 0
        counter = 0
        max_space = 0

        while heap:
            cost, _, state, path = heapq.heappop(heap)
            key = tuple(state)
            if key in visited:
                continue
            visited.add(key)

            max_space = max(max_space, len(heap) + len(visited))

            if self.is_goal(state):
                return {
                    "time": time.time() - start,
                    "space": max_space,
                    "expanded": expanded,
                    "path": path + [state]
                }

            for neighbor in self.expand(state):
                counter += 1
                move_cost = self.get_move_cost(state, neighbor)
                new_cost = cost + move_cost
                heapq.heappush(heap, (new_cost, counter, neighbor, path + [state]))
            expanded += 1

        return {
            "time": time.time() - start,
            "space": max_space,
            "expanded": expanded,
            "path": []
        }
