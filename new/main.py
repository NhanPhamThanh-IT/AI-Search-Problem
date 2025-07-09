import pygame
from config import SETTINGS
from scenes import run_menu, run_playing

def run_game():
    pygame.init()
    screen = pygame.display.set_mode((SETTINGS["WINDOW_SIZE"][0], SETTINGS["WINDOW_SIZE"][1]))
    pygame.display.set_caption(SETTINGS["TITLE"])
    clock = pygame.time.Clock()

    state = SETTINGS["SCENES"]["MENU"]
    play_data = {}

    running = True
    while running:
        if state == SETTINGS["SCENES"]["MENU"]:
            state, play_data = run_menu(screen, clock)
        elif state == SETTINGS["SCENES"]["PLAY"]:
            state = run_playing(screen, clock, play_data)
        elif state == SETTINGS["SCENES"]["QUIT"]:
            running = False

    pygame.quit()

if __name__ == "__main__":
    run_game()