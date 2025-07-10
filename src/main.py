import pygame
from config import SETTINGS
from scenes import run_menu, PlayingScreen

def run_game():
    pygame.init()
    screen = pygame.display.set_mode(SETTINGS["WINDOW_SIZE"])
    pygame.display.set_caption(SETTINGS["TITLE"])
    clock = pygame.time.Clock()

    state = SETTINGS["SCENES"]["MENU"]
    play_data = {}
    playing_screen = None

    running = True
    while running:
        if state == SETTINGS["SCENES"]["MENU"]:
            state, play_data = run_menu(screen, clock)
            if state == SETTINGS["SCENES"]["PLAY"]:
                playing_screen = PlayingScreen(screen, clock, play_data)
        elif state == SETTINGS["SCENES"]["PLAY"]:
            result = playing_screen.run()
            if result == "menu":
                state = SETTINGS["SCENES"]["MENU"]
            elif result == "quit":
                state = SETTINGS["SCENES"]["QUIT"]
        elif state == SETTINGS["SCENES"]["QUIT"]:
            running = False

    pygame.quit()

if __name__ == "__main__":
    run_game()
