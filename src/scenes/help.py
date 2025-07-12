import pygame
from config import SETTINGS
from entities import Button

class HelpScreen:
    def __init__(self, screen, clock):
        self.screen = screen
        self.clock = clock
        self.screen_width, self.screen_height = SETTINGS["WINDOW_SIZE"]
        self.title_font = pygame.font.Font(None, 48)
        self.text_font = pygame.font.Font(None, 32)

        button_width, button_height = 160, 60
        button_x = self.screen_width // 2 - button_width // 2
        button_y = int(self.screen_height * 0.85)

        self.back_button = Button(
            rect=pygame.Rect(button_x, button_y, button_width, button_height),
            text="Back",
        )

        self.instructions = [
            "How to use:",
            "- Click the Play button to start solving the puzzle.",
            "- Select the appropriate map and algorithm.",
            "- Watch the solving process and the result.",
            "- Return to the main menu via ESC or the Back button.",
        ]

    def draw(self):
        self.screen.fill(SETTINGS["BG_COLOR"])

        title_surf = self.title_font.render("Help", True, (255, 255, 255))
        title_rect = title_surf.get_rect(center=(self.screen_width // 2, 60))
        self.screen.blit(title_surf, title_rect)

        start_y = 140
        line_spacing = 40
        left_margin = 80

        for idx, line in enumerate(self.instructions):
            line_surf = self.text_font.render(line, True, (220, 220, 220))
            line_rect = line_surf.get_rect(topleft=(left_margin, start_y + idx * line_spacing))
            self.screen.blit(line_surf, line_rect)

        self.back_button.draw(self.screen)

    def handle_events(self):
        mouse_pos = pygame.mouse.get_pos()
        self.back_button.hover = self.back_button.rect.collidepoint(mouse_pos)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return SETTINGS["SCENES"]["QUIT"]

            if event.type == pygame.MOUSEBUTTONDOWN and self.back_button.hover:
                return SETTINGS["SCENES"]["MENU"]

        return None

    def run(self):
        while True:
            self.draw()
            result = self.handle_events()
            if result:
                return result

            pygame.display.flip()
            self.clock.tick(60)
