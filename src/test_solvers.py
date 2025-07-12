#!/usr/bin/env python3

import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from core.map_loader import load_map_from_json
from solvers import get_solver_class

def test_solver(algo_name, map_file):
    print(f"\n=== Testing {algo_name} with {map_file} ===")
    
    try:
        board = load_map_from_json(f"maps/{map_file}")
        print(f"Board size: {board.size}")
        print(f"Number of vehicles: {len(board.vehicles)}")
        
        if 'X' not in board.vehicles:
            print("ERROR: Xe X không tồn tại trong map!")
            return False
            
        x_vehicle = board.vehicles['X']
        print(f"X vehicle position: ({x_vehicle.row}, {x_vehicle.col}), length: {x_vehicle.length}, orientation: {x_vehicle.orientation}")
        
        solver_class = get_solver_class(algo_name)
        solver = solver_class(board)
        
        print(f"Initial state: {solver.initial_state}")
        
        is_initial_goal = solver.is_goal(solver.initial_state)
        print(f"Is initial state goal? {is_initial_goal}")
        
        neighbors = solver.expand(solver.initial_state)
        print(f"Number of possible moves from initial state: {len(neighbors)}")
        
        if len(neighbors) > 0:
            print("Sample neighbor state:", neighbors[0])
        else:
            print("WARNING: Không có move nào có thể từ trạng thái ban đầu!")
            return False
        
        print("Solving...")
        result = solver.solve()
        
        print(f"Solve results:")
        print(f"  Time: {result['time']:.4f}s")
        print(f"  Space used: {result['space']}")
        print(f"  Nodes expanded: {result['expanded']}")
        print(f"  Solution length: {len(result['path'])}")
        
        if result['path']:
            print("✅ Solution found!")
            return True
        else:
            print("❌ No solution found!")
            return False
            
    except Exception as e:
        print(f"❌ Error: {e}")
        import traceback
        traceback.print_exc()
        return False

def main():
    algorithms = ["BFS", "DFS", "UCS", "A*"]
    maps = ["map1.json", "map2.json"]
    
    success_count = 0
    total_tests = 0
    
    for map_file in maps:
        for algo in algorithms:
            total_tests += 1
            if test_solver(algo, map_file):
                success_count += 1
    
    print(f"\n{'='*50}")
    print(f"Test Summary: {success_count}/{total_tests} tests passed")
    
    if success_count == total_tests:
        print("🎉 Tất cả các thuật toán hoạt động tốt!")
    else:
        print("⚠️  Một số thuật toán có vấn đề, cần kiểm tra lại.")

if __name__ == "__main__":
    main()
