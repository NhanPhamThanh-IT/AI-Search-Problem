from core.vehicle import Vehicle
from typing import Dict, Tuple

class Board:
    def __init__(self, size: Tuple[int, int], vehicles: Dict[str, Vehicle]):
        self.rows, self.cols = size
        self.vehicles = vehicles  # key: vehicle name, value: Vehicle object

    def is_within_bounds(self, row: int, col: int) -> bool:
        return 0 <= row < self.rows and 0 <= col < self.cols

    def get_occupied_cells(self) -> set[tuple[int, int]]:
        """Trả về tập hợp tất cả các ô đang bị chiếm bởi các xe."""
        occupied = set()
        for v in self.vehicles.values():
            occupied.update(v.get_coordinates())
        return occupied

    def display(self):
        """In ra ma trận trò chơi dưới dạng văn bản."""
        grid = [["." for _ in range(self.cols)] for _ in range(self.rows)]
        for v in self.vehicles.values():
            for r, c in v.get_coordinates():
                grid[r][c] = v.name
        for row in grid:
            print(" ".join(row))

    def __repr__(self):
        return f"Board({self.rows}x{self.cols}, Vehicles={len(self.vehicles)})"
