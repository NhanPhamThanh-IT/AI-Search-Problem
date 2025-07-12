import pygame

class Button:
    def __init__(self, x=None, y=None, width=None, height=None, text="", 
                 bg_color=(100, 100, 100), text_color=(255, 255, 255), 
                 font_size=24, rect=None):
        
        # Nếu có rect, sử dụng rect
        if rect is not None:
            self.rect = rect
        # Nếu có x, y, width, height thì tạo rect mới
        elif x is not None and y is not None and width is not None and height is not None:
            self.rect = pygame.Rect(x, y, width, height)
        else:
            raise ValueError("Phải cung cấp hoặc rect hoặc (x, y, width, height)")
            
        self.text = text
        self.bg_color = bg_color
        self.text_color = text_color
        self.font = pygame.font.Font(None, font_size)
        self.is_hovered = False

    def handle_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1 and self.rect.collidepoint(event.pos):
                return True
        elif event.type == pygame.MOUSEMOTION:
            self.is_hovered = self.rect.collidepoint(event.pos)
        return False

    def draw(self, screen):
        # Change color when hovered
        color = tuple(min(255, c + 20) for c in self.bg_color) if self.is_hovered else self.bg_color
        
        pygame.draw.rect(screen, color, self.rect)
        pygame.draw.rect(screen, (200, 200, 200), self.rect, 2)
        
        # Draw text
        text_surface = self.font.render(self.text, True, self.text_color)
        text_rect = text_surface.get_rect(center=self.rect.center)
        screen.blit(text_surface, text_rect)
