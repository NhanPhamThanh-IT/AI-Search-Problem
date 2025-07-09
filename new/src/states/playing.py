from ..config import SETTINGS
import pygame

def run_playing(screen, clock, play_data):
    FONT = pygame.font.Font(None, 36)
    screen_width, screen_height = screen.get_size()

    running = True

    while running:
        screen.fill((0, 0, 50))

        # ---------- Render play_data in one horizontal line with space-between ----------
        num_items = len(play_data)
        padding = 100  # Left and right margin
        usable_width = screen_width - 2 * padding
        gap = usable_width // (num_items - 1) if num_items > 1 else 0
        y = 20  # Y position for horizontal text line

        for i, (key, value) in enumerate(play_data.items()):
            line = f"{key.capitalize()}: {value}"
            text_surface = FONT.render(line, True, (255, 255, 255))
            text_rect = text_surface.get_rect()
            x = padding + i * gap - text_rect.width // 2
            screen.blit(text_surface, (x, y))

        # ---------- Render bottom centered hint ----------
        hint = FONT.render("Press ESC to return to Menu", True, (255, 255, 255))
        hint_rect = hint.get_rect(center=(screen_width // 2, screen_height - 40))
        screen.blit(hint, hint_rect)

        # ---------- Event handling ----------
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return SETTINGS["SCENES"]["QUIT"]
            elif event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                return SETTINGS["SCENES"]["MENU"]

        pygame.display.flip()
        clock.tick(60)
