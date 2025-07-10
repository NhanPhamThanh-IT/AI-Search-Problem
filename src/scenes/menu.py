import pygame
from config import SETTINGS
from entities import Button
from utils import random_map


def run_menu(screen, clock):
    pygame.font.init()
    font = pygame.font.Font(None, 36)
    title_font = pygame.font.Font(None, 42)

    selected_map = None
    buttons = []

    def select_map(name):
        nonlocal selected_map
        selected_map = name
        for btn in buttons:
            btn.selected = (btn.text == name)

    maps = SETTINGS["MAPS"]
    screen_width, screen_height = SETTINGS["WINDOW_SIZE"]
    x_start = screen_width // 2 - (len(maps) * 110 - 10) // 2
    y_buttons = screen_height // 2.5

    for i, name in enumerate(maps):
        rect = (x_start + i * 110, y_buttons, 100, 50)
        button = Button(rect, name, font, lambda name=name: select_map(name))
        buttons.append(button)

    play_button = Button((screen_width // 2 - 60, int(screen_height * 0.75), 120, 60), "Play", font)

    while True:
        screen.fill(SETTINGS["BG_COLOR"])
        mouse_pos = pygame.mouse.get_pos()

        title_surf = title_font.render("Select Map", True, (255, 255, 255))
        screen.blit(title_surf, title_surf.get_rect(center=(screen_width // 2, y_buttons - 40)))

        for btn in buttons:
            btn.draw(screen)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return SETTINGS["SCENES"]["QUIT"], {}

            for btn in buttons:
                btn.handle_event(event, mouse_pos)

            play_button.hover = play_button.rect.collidepoint(mouse_pos)
            if play_button.hover and event.type == pygame.MOUSEBUTTONDOWN and selected_map:
                chosen_map = random_map() if selected_map == "Random" else selected_map
                return SETTINGS["SCENES"]["PLAY"], {"map": chosen_map}

        if selected_map:
            play_button.draw(screen)

        pygame.display.flip()
        clock.tick(60)
