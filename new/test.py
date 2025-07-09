import pygame
from core import load_map_from_json
from solvers import BFSSolver, DFSSolver, UCSSolver, AStarSolver

pygame.init()
screen = pygame.display.set_mode((800, 600))
clock = pygame.time.Clock()

board = load_map_from_json("maps/map1.json")
solver = BFSSolver(board)
solver.solve()
print("Solution:", solver.solution)
print("Nodes Expanded:", solver.expanded_nodes)
print("Time Taken:", solver.time_taken)

solver = DFSSolver(board)
solver.solve()
print("Solution:", solver.solution)
print("Nodes Expanded:", solver.expanded_nodes)
print("Time Taken:", solver.time_taken)

solver = UCSSolver(board)
solver.solve()
print("Solution:", solver.solution)
print("Nodes Expanded:", solver.expanded_nodes)
print("Time Taken:", solver.time_taken)

solver = AStarSolver(board)
solver.solve()
print("Solution:", solver.solution)
print("Nodes Expanded:", solver.expanded_nodes)
print("Time Taken:", solver.time_taken)
