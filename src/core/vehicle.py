import pygame
import random

class Vehicle:
    _used_colors = set()
    
    def __init__(self, name, row, col, length, orientation):
        self.name = name
        self.row = row
        self.col = col
        self.length = length
        self.orientation = orientation
        self.color = self._generate_unique_color()

    @classmethod
    def _generate_unique_color(cls):
        max_attempts = 1000
        attempts = 0
        
        while attempts < max_attempts:
            r = random.randint(50, 255)
            g = random.randint(50, 255) 
            b = random.randint(50, 255)
            color = (r, g, b)
            
            if color not in cls._used_colors:
                cls._used_colors.add(color)
                return color
                
            attempts += 1
        
        default_color = (100, 100, 255)
        cls._used_colors.add(default_color)
        return default_color

    @classmethod
    def reset_colors(cls):
        cls._used_colors.clear()

    def get_rect(self, pos, cell_size):
        x = pos[0] + self.col * cell_size
        y = pos[1] + self.row * cell_size
        width = cell_size * self.length if self.orientation == 'H' else cell_size
        height = cell_size * self.length if self.orientation == 'V' else cell_size
        return pygame.Rect(x, y, width, height)

    def draw_name(self, screen, pos, cell_size, font=None):
        if font is None:
            font = pygame.font.Font(None, cell_size // 2)

        rect = self.get_rect(pos, cell_size)
        center_x = rect.centerx
        center_y = rect.centery

        text_surface = font.render(self.name, True, (255, 255, 255))
        text_rect = text_surface.get_rect(center=(center_x, center_y))

        screen.blit(text_surface, text_rect)

    def get_color(self):
        if self.name == 'X':
            return (200, 0, 0)
        return self.color
