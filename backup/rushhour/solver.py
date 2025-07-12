"""
Abstract base class for Rush Hour solvers
Provides interface for different search algorithms
"""

from abc import ABC, abstractmethod
from collections import deque
import heapq
import time

class RushHourSolver(ABC):
    def __init__(self):
        self.solution_path = []
        self.nodes_explored = 0
        self.execution_time = 0
        self.max_queue_size = 0
    
    @abstractmethod
    def solve(self, initial_state):
        """
        Solve the Rush Hour puzzle
        
        Args:
            initial_state (RushHourState): Initial puzzle state
            
        Returns:
            tuple: (solution_path, stats_dict)
        """
        pass
    
    def get_statistics(self):
        """
        Get solving statistics
        
        Returns:
            dict: Dictionary containing solving statistics
        """
        return {
            'nodes_explored': self.nodes_explored,
            'execution_time': self.execution_time,
            'max_queue_size': self.max_queue_size,
            'solution_length': len(self.solution_path)
        }


class BFSSolver(RushHourSolver):
    """Breadth-First Search solver for Rush Hour puzzle"""
    
    def solve(self, initial_state):
        """
        Solve using BFS algorithm
        
        Args:
            initial_state (RushHourState): Initial puzzle state
            
        Returns:
            tuple: (solution_path, stats_dict) where solution_path is list of moves
        """
        start_time = time.time()
        
        if initial_state.is_goal_state():
            self.execution_time = time.time() - start_time
            return [], self.get_statistics()
        
        queue = deque([(initial_state, [])])
        visited = {initial_state.get_state_hash()}
        self.nodes_explored = 0
        self.max_queue_size = 1
        
        while queue:
            self.max_queue_size = max(self.max_queue_size, len(queue))
            current_state, path = queue.popleft()
            self.nodes_explored += 1
            
            # Get all possible moves from current state
            possible_moves = current_state.get_possible_moves()
            
            for vehicle_name, direction in possible_moves:
                new_state = current_state.make_move(vehicle_name, direction)
                state_hash = new_state.get_state_hash()
                
                if state_hash not in visited:
                    visited.add(state_hash)
                    new_path = path + [(vehicle_name, direction)]
                    
                    if new_state.is_goal_state():
                        self.solution_path = new_path
                        self.execution_time = time.time() - start_time
                        return new_path, self.get_statistics()
                    
                    queue.append((new_state, new_path))
        
        # No solution found
        self.execution_time = time.time() - start_time
        return None, self.get_statistics()


class DFSSolver(RushHourSolver):
    """Depth-First Search solver for Rush Hour puzzle"""
    
    def __init__(self, max_depth=50):
        super().__init__()
        self.max_depth = max_depth
    
    def solve(self, initial_state):
        """
        Solve using DFS algorithm with depth limit
        
        Args:
            initial_state (RushHourState): Initial puzzle state
            
        Returns:
            tuple: (solution_path, stats_dict)
        """
        start_time = time.time()
        
        if initial_state.is_goal_state():
            self.execution_time = time.time() - start_time
            return [], self.get_statistics()
        
        stack = [(initial_state, [], 0)]  # (state, path, depth)
        visited = {initial_state.get_state_hash()}
        self.nodes_explored = 0
        self.max_queue_size = 1
        
        while stack:
            self.max_queue_size = max(self.max_queue_size, len(stack))
            current_state, path, depth = stack.pop()
            self.nodes_explored += 1
            
            if depth >= self.max_depth:
                continue
            
            possible_moves = current_state.get_possible_moves()
            
            for vehicle_name, direction in possible_moves:
                new_state = current_state.make_move(vehicle_name, direction)
                state_hash = new_state.get_state_hash()
                
                if state_hash not in visited:
                    visited.add(state_hash)
                    new_path = path + [(vehicle_name, direction)]
                    
                    if new_state.is_goal_state():
                        self.solution_path = new_path
                        self.execution_time = time.time() - start_time
                        return new_path, self.get_statistics()
                    
                    stack.append((new_state, new_path, depth + 1))
        
        self.execution_time = time.time() - start_time
        return None, self.get_statistics()


class AStarSolver(RushHourSolver):
    """A* Search solver for Rush Hour puzzle"""
    
    def solve(self, initial_state):
        """
        Solve using A* algorithm
        
        Args:
            initial_state (RushHourState): Initial puzzle state
            
        Returns:
            tuple: (solution_path, stats_dict)
        """
        start_time = time.time()
        
        if initial_state.is_goal_state():
            self.execution_time = time.time() - start_time
            return [], self.get_statistics()
        
        # Priority queue: (f_score, g_score, state, path)
        heap = [(self._heuristic(initial_state), 0, initial_state, [])]
        visited = {initial_state.get_state_hash(): 0}
        self.nodes_explored = 0
        self.max_queue_size = 1
        
        while heap:
            self.max_queue_size = max(self.max_queue_size, len(heap))
            f_score, g_score, current_state, path = heapq.heappop(heap)
            self.nodes_explored += 1
            
            state_hash = current_state.get_state_hash()
            if state_hash in visited and visited[state_hash] < g_score:
                continue
            
            possible_moves = current_state.get_possible_moves()
            
            for vehicle_name, direction in possible_moves:
                new_state = current_state.make_move(vehicle_name, direction)
                new_state_hash = new_state.get_state_hash()
                new_g_score = g_score + 1
                new_path = path + [(vehicle_name, direction)]
                
                if new_state.is_goal_state():
                    self.solution_path = new_path
                    self.execution_time = time.time() - start_time
                    return new_path, self.get_statistics()
                
                if new_state_hash not in visited or visited[new_state_hash] > new_g_score:
                    visited[new_state_hash] = new_g_score
                    h_score = self._heuristic(new_state)
                    f_score = new_g_score + h_score
                    heapq.heappush(heap, (f_score, new_g_score, new_state, new_path))
        
        self.execution_time = time.time() - start_time
        return None, self.get_statistics()
    
    def _heuristic(self, state):
        """
        Heuristic function for A* - distance to goal for target vehicle
        
        Args:
            state (RushHourState): Current state
            
        Returns:
            int: Heuristic value
        """
        target_vehicle = state.get_target_vehicle()
        if not target_vehicle:
            return float('inf')
        
        # Distance from target vehicle to exit
        exit_col = state.board_size
        current_rightmost = target_vehicle.col + target_vehicle.length
        
        # If target is not in row 2, add penalty
        if target_vehicle.row != 2:
            return abs(target_vehicle.row - 2) + (exit_col - current_rightmost)
        
        return max(0, exit_col - current_rightmost)


class UCSolver(RushHourSolver):
    """Uniform Cost Search solver for Rush Hour puzzle"""
    
    def solve(self, initial_state):
        """
        Solve using Uniform Cost Search algorithm
        
        Args:
            initial_state (RushHourState): Initial puzzle state
            
        Returns:
            tuple: (solution_path, stats_dict)
        """
        start_time = time.time()
        
        if initial_state.is_goal_state():
            self.execution_time = time.time() - start_time
            return [], self.get_statistics()
        
        # Priority queue: (cost, state, path)
        heap = [(0, initial_state, [])]
        visited = {initial_state.get_state_hash(): 0}
        self.nodes_explored = 0
        self.max_queue_size = 1
        
        while heap:
            self.max_queue_size = max(self.max_queue_size, len(heap))
            cost, current_state, path = heapq.heappop(heap)
            self.nodes_explored += 1
            
            state_hash = current_state.get_state_hash()
            if state_hash in visited and visited[state_hash] < cost:
                continue
            
            possible_moves = current_state.get_possible_moves()
            
            for vehicle_name, direction in possible_moves:
                new_state = current_state.make_move(vehicle_name, direction)
                new_state_hash = new_state.get_state_hash()
                new_cost = cost + 1
                new_path = path + [(vehicle_name, direction)]
                
                if new_state.is_goal_state():
                    self.solution_path = new_path
                    self.execution_time = time.time() - start_time
                    return new_path, self.get_statistics()
                
                if new_state_hash not in visited or visited[new_state_hash] > new_cost:
                    visited[new_state_hash] = new_cost
                    heapq.heappush(heap, (new_cost, new_state, new_path))
        
        self.execution_time = time.time() - start_time
        return None, self.get_statistics()


def get_solver(algorithm_name):
    """
    Factory function to get solver instance
    
    Args:
        algorithm_name (str): Name of the algorithm ('BFS', 'DFS', 'UCS', 'A*')
        
    Returns:
        RushHourSolver: Solver instance
    """
    solvers = {
        'BFS': BFSSolver,
        'DFS': DFSSolver,
        'UCS': UCSolver,
        'A*': AStarSolver
    }
    
    if algorithm_name not in solvers:
        raise ValueError(f"Unknown algorithm: {algorithm_name}")
    
    return solvers[algorithm_name]()
