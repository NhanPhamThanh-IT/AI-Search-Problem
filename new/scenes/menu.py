import pygame
from config import SETTINGS
from entities import Button
from utils import random_map


def run_menu(screen, clock):
    pygame.font.init()
    font = pygame.font.Font(None, 36)
    title_font = pygame.font.Font(None, 42)

    selected = {"map": None, "algorithm": None}
    buttons = []

    def select_item(category, value):
        selected[category] = value
        for b in buttons:
            if b.group == category:
                b.selected = (b.text == value)

    section_spacing = SETTINGS["WINDOW_SIZE"][1] // 5
    section_y_positions = {
        "map": section_spacing * 2,
        "algorithm": section_spacing * 3.2,
    }

    for category, values in [("map", SETTINGS["MAPS"]), ("algorithm", SETTINGS["ALGORITHMS"])]:
        y_button = section_y_positions[category]
        x_start = SETTINGS["WINDOW_SIZE"][0] // 2 - (len(values) * 110 - 10) // 2
        for i, val in enumerate(values):
            rect = (x_start + i * 110, y_button, 100, 50)
            btn = Button(rect, val, font, lambda c=category, v=val: select_item(c, v))
            btn.group = category
            buttons.append(btn)

    play_button = Button((SETTINGS["WINDOW_SIZE"][0] // 2 - 60, section_spacing * 4.4, 120, 60), "Play", font)

    while True:
        mouse_pos = pygame.mouse.get_pos()
        screen.fill(SETTINGS["BG_COLOR"])

        for category in ["map", "algorithm"]:
            y_label = section_y_positions[category] - 40
            label = title_font.render(f"Select {category.title()}", True, (255, 255, 255))
            screen.blit(label, label.get_rect(center=(SETTINGS["WINDOW_SIZE"][0] // 2, y_label)))

        for button in buttons:
            button.draw(screen)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return SETTINGS["SCENES"]["QUIT"], {}

            for button in buttons:
                button.handle_event(event, mouse_pos)

            if play_button.rect.collidepoint(mouse_pos):
                play_button.hover = True
                if event.type == pygame.MOUSEBUTTONDOWN:
                    return SETTINGS["SCENES"]["PLAY"], {
                        "map": random_map() if selected["map"] == "Random" else selected["map"],
                        "algorithm": selected["algorithm"]
                    }
            else:
                play_button.hover = False

        if all(selected.values()):
            play_button.draw(screen)

        pygame.display.flip()
        clock.tick(60)
