import pygame
from config import SETTINGS
from entities import Button


def run_menu(screen, clock):
    pygame.font.init()
    font = pygame.font.Font(None, 36)
    title_font = pygame.font.Font(None, 42)

    screen_width, screen_height = SETTINGS["WINDOW_SIZE"]

    play_button = Button(
        (screen_width // 2 - 60, int(screen_height * 0.6), 120, 60),
        "Play",
        font
    )

    while True:
        screen.fill(SETTINGS["BG_COLOR"])
        mouse_pos = pygame.mouse.get_pos()

        title_surf = title_font.render("Rush Hour Solver", True, (255, 255, 255))
        screen.blit(title_surf, title_surf.get_rect(center=(screen_width // 2, screen_height // 3)))

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return SETTINGS["SCENES"]["QUIT"], {}

            play_button.hover = play_button.rect.collidepoint(mouse_pos)
            if play_button.hover and event.type == pygame.MOUSEBUTTONDOWN:
                return SETTINGS["SCENES"]["PLAY"], {}

        play_button.draw(screen)

        pygame.display.flip()
        clock.tick(60)
