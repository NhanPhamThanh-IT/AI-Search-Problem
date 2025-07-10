import pygame
from config import SETTINGS
from entities import Button

class HomeScreen:
    def __init__(self, screen, clock):
        self.screen = screen
        self.clock = clock
        self.font = pygame.font.Font(None, 36)
        self.title_font = pygame.font.Font(None, 42)

        self.screen_width, self.screen_height = SETTINGS["WINDOW_SIZE"]

        self.play_button = Button(
            rect=(self.screen_width // 2 - 60, int(self.screen_height * 0.6), 120, 60),
            text="Play",
            font=self.font
        )

    def draw(self):
        self.screen.fill(SETTINGS["BG_COLOR"])
        mouse_pos = pygame.mouse.get_pos()

        title_surf = self.title_font.render("Rush Hour Solver", True, (255, 255, 255))
        title_rect = title_surf.get_rect(center=(self.screen_width // 2, self.screen_height // 3))
        self.screen.blit(title_surf, title_rect)

        self.play_button.hover = self.play_button.rect.collidepoint(mouse_pos)
        self.play_button.draw(self.screen)

    def handle_events(self):
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
