import pygame
from config import SETTINGS
from scenes import HomeScreen, PlayingScreen

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
            home_screen = HomeScreen(screen, clock)
            state = home_screen.run()
            if state == SETTINGS["SCENES"]["PLAY"]:
                playing_screen = PlayingScreen(screen, clock)
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
