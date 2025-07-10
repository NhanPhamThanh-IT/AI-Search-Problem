from typing import Literal

Orientation = Literal["H", "V"]

class Vehicle:
    def __init__(self, name: str, row: int, col: int, length: int, orientation: Orientation):
        self.name = name
        self.row = row
        self.col = col
        self.length = length
        self.orientation = orientation.upper()

        if self.orientation not in ("H", "V"):
            raise ValueError(f"Invalid orientation '{self.orientation}' for vehicle '{self.name}'")

    def get_coordinates(self) -> list[tuple[int, int]]:
        """Trả về danh sách các tọa độ mà xe chiếm trên lưới."""
        if self.orientation == "H":
            return [(self.row, self.col + i) for i in range(self.length)]
        else:
            return [(self.row + i, self.col) for i in range(self.length)]

    def __repr__(self):
        return f"Vehicle({self.name}, row={self.row}, col={self.col}, len={self.length}, ori={self.orientation})"
