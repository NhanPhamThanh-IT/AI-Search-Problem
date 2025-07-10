from core.vehicle import Vehicle
import pygame
from config import SETTINGS

class Board:
    def __init__(self, size, vehicles):
        self.size = size
        self.vehicles = {v.name: v for v in vehicles}

    @classmethod
    def from_dict(cls, data):
        vehicles = [Vehicle(**v) for v in data["vehicles"]]
        return cls(data["size"], vehicles)

    def draw(self, screen, pos=(0, 0)):
        cell_size = SETTINGS["CELL_SIZE"]
        for i in range(self.size[0]):
            for j in range(self.size[1]):
                pygame.draw.rect(screen, (80, 80, 80), (
                    pos[0] + j * cell_size, pos[1] + i * cell_size, cell_size, cell_size), 1)

        for v in self.vehicles.values():
            color = (200, 0, 0) if v.name == 'X' else (100, 100, 255)
            rect = v.get_rect(pos, cell_size)
            pygame.draw.rect(screen, color, rect)
