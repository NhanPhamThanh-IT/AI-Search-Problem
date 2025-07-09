from abc import ABC, abstractmethod

class BaseSolver(ABC):
    def __init__(self, initial_board):
        self.initial_board = initial_board
        self.solution = []
        self.expanded_nodes = 0
        self.time_taken = 0
        self.memory_usage = 0

    @abstractmethod
    def solve(self):
        """
        Must set self.solution to a list of (vehicle_name, direction) steps.
        Also should track expanded_nodes, time_taken, etc.
        """
        pass
