class Vehicle:
    def __init__(self, name, row, col, length, orientation):
        self.name = name
        self.row = row
        self.col = col
        self.length = length
        self.orientation = orientation.upper()

    def clone(self):
        return Vehicle(self.name, self.row, self.col, self.length, self.orientation)

    def get_cells(self):
        cells = []
        for i in range(self.length):
            if self.orientation == 'H':
                cells.append((self.row, self.col + i))
            else:
                cells.append((self.row + i, self.col))
        return cells
