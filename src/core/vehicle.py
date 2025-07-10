import pygame

class Vehicle:
    def __init__(self, name, row, col, length, orientation):
        self.name = name
        self.row = row
        self.col = col
        self.length = length
        self.orientation = orientation

    def get_rect(self, pos, cell_size):
        x = pos[0] + self.col * cell_size
        y = pos[1] + self.row * cell_size
        width = cell_size * self.length if self.orientation == 'H' else cell_size
        height = cell_size * self.length if self.orientation == 'V' else cell_size
        return pygame.Rect(x, y, width, height)
