import pygame
import os
from config import SETTINGS
from entities import Button

class HomeScreen:
    def __init__(self, screen, clock):
        self.screen = screen
        self.clock = clock
        self.font = pygame.font.Font(None, 36)
        self.title_font = pygame.font.Font(None, 48)
        self.screen_width, self.screen_height = SETTINGS["WINDOW_SIZE"]

        try:
            logo_path = os.path.join("assets", "logo.png")
            self.logo = pygame.image.load(logo_path)
            self.logo = pygame.transform.scale(self.logo, (300, 300))
        except:
            self.logo = None

        button_width, button_height = 160, 60
        button_x = self.screen_width // 2 - button_width // 2
        button_y = int(self.screen_height * 0.75)
        self.play_button = Button(
            rect=pygame.Rect(button_x, button_y, button_width, button_height),
            text="Play",
        )

    def draw(self):
        self.screen.fill(SETTINGS["BG_COLOR"])

        title_surf = self.title_font.render("Rush Hour Solver", True, (255, 255, 255))
        title_rect = title_surf.get_rect(center=(self.screen_width // 2, int(self.screen_height * 0.1)))
        self.screen.blit(title_surf, title_rect)

        if self.logo:
            logo_x = self.screen_width // 2 - self.logo.get_width() // 2
            logo_y = int(self.screen_height * 0.2)
            self.screen.blit(self.logo, (logo_x, logo_y))

        self.play_button.draw(self.screen)

    def handle_events(self):
        mouse_pos = pygame.mouse.get_pos()
        self.play_button.hover = self.play_button.rect.collidepoint(mouse_pos)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return SETTINGS["SCENES"]["QUIT"], {}

            if self.play_button.hover and event.type == pygame.MOUSEBUTTONDOWN:
                return SETTINGS["SCENES"]["PLAY"]

        return None

    def run(self):
        while True:
            self.draw()
            result = self.handle_events()
            if result:
                return result

            pygame.display.flip()
            self.clock.tick(60)
