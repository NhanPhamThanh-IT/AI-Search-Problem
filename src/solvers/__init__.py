from solvers.bfs_solver import BFSSolver
from solvers.dfs_solver import DFSSolver
from solvers.ucs_solver import UCSSolver
from solvers.astar_solver import AStarSolver

def get_solver_class(name):
    name = name.upper()
    if name == "BFS":
        return BFSSolver
    elif name == "DFS":
        return DFSSolver
    elif name == "UCS":
        return UCSSolver
    elif name in ["A*", "ASTAR"]:
        return AStarSolver
    else:
        raise ValueError(f"Unknown algorithm: {name}")
