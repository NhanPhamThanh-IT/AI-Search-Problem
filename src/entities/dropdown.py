from anyio import value
import pygame

class Dropdown:
    def __init__(self, x, y, width, height, options, font_size=24):
        self.rect = pygame.Rect(x, y, width, height)
        self.options = options
        self.selected_index = 0
        self.expanded = False
        self.font = pygame.font.Font(None, font_size)

    def handle_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            if self.rect.collidepoint(event.pos):
                self.expanded = not self.expanded
            elif self.expanded:
                for i, option in enumerate(self.options):
                    item_rect = pygame.Rect(self.rect.x, self.rect.y + (i + 1) * self.rect.height,
                                            self.rect.width, self.rect.height)
                    if item_rect.collidepoint(event.pos):
                        self.selected_index = i
                        self.expanded = False
                        break
                else:
                    self.expanded = False

    def draw(self, screen):
        pygame.draw.rect(screen, (60, 60, 60), self.rect)
        text = self.font.render(self.options[self.selected_index], True, (255, 255, 255))
        screen.blit(text, (self.rect.x + 5, self.rect.y + 5))
        pygame.draw.rect(screen, (255, 255, 255), self.rect, 2)

        if self.expanded:
            for i, option in enumerate(self.options):
                item_rect = pygame.Rect(self.rect.x, self.rect.y + (i + 1) * self.rect.height,
                                        self.rect.width, self.rect.height)
                pygame.draw.rect(screen, (80, 80, 80), item_rect)
                text = self.font.render(option, True, (255, 255, 255))
                screen.blit(text, (item_rect.x + 5, item_rect.y + 5))
                pygame.draw.rect(screen, (255, 255, 255), item_rect, 1)

    def get_selected(self):
        return self.options[self.selected_index]
    
    def set_selected(self, value):
        if value in self.options:
            self.selected_index = self.options.index(value)
