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
                    "expanded": expanded,
                    "path": path + [state]
                }

            for neighbor in self.expand(state):
                counter += 1
                cost = len(path) + 1
                heapq.heappush(heap, (cost + self.heuristic(neighbor), counter, neighbor, path + [state]))
            expanded += 1

        return {
            "time": time.time() - start,
            "space": len(visited),
            "expanded": expanded,
            "path": []
        }

    def heuristic(self, state):
        x_vehicle = None
        for v in state:
            if v[4] == "X":
                x_vehicle = v
                break
        
        if x_vehicle is None:
            return 0
            
        x_row, x_col, x_length, x_orientation, _ = x_vehicle
        
        if x_orientation != 'H':
            return float('inf')
        
        x_end_col = x_col + x_length
        exit_col = self.board.size[1]
        
        if x_end_col >= exit_col:
            return 0
        
        blocking_count = 0
        for v in state:
            if v[4] != "X":
                v_row, v_col, v_length, v_orientation, _ = v
                
                if v_orientation == 'V':
                    if (v_col > x_end_col - 1 and v_col < exit_col and 
                        v_row <= x_row < v_row + v_length):
                        blocking_count += 1
                elif v_orientation == 'H':
                    if (v_row == x_row and 
                        v_col > x_end_col - 1 and v_col < exit_col):
                        blocking_count += 1
        
        return blocking_count
