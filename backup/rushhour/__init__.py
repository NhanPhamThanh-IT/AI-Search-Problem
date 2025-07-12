"""
Rush Hour Puzzle Module
A modular, extensible implementation of the Rush Hour puzzle solver
"""

from .vehicle import RushHourVehicle
from .state import RushHourState
from .solver import RushHourSolver, BFSSolver, DFSSolver, AStarSolver, UCSolver, get_solver
from .game import RushHourGame

__all__ = [
    'RushHourVehicle',
    'RushHourState', 
    'RushHourSolver',
    'BFSSolver',
    'DFSSolver', 
    'AStarSolver',
    'UCSolver',
    'RushHourGame',
    'get_solver'
]

__version__ = "1.0.0"
