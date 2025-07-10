import pygame

class Button:
    def __init__(self, rect, text, font, callback=None):
        self.rect = pygame.Rect(rect)
        self.text = text
        self.font = font
        self.callback = callback
        self.hover = False
        self.selected = False
        self.group = None  # <-- THÊM dòng này

    def draw(self, screen):
        base_color = (0, 200, 0) if self.selected else (80, 80, 80)
        hover_color = (120, 200, 120) if self.selected else (120, 120, 120)
        color = hover_color if self.hover else base_color

        pygame.draw.rect(screen, color, self.rect, border_radius=8)
        text_surf = self.font.render(self.text, True, (255, 255, 255))
        screen.blit(text_surf, (
            self.rect.centerx - text_surf.get_width() // 2,
            self.rect.centery - text_surf.get_height() // 2
        ))

    def handle_event(self, event, mouse_pos):
        self.hover = self.rect.collidepoint(mouse_pos)
        if event.type == pygame.MOUSEBUTTONDOWN and self.hover and self.callback:
            self.callback()
