import pygame
import time
from config import SETTINGS
from core.map_loader import load_map_from_json
from solvers.bfs_solver import BFSSolver

CELL_SIZE = SETTINGS["CELL_SIZE"]
MARGIN = SETTINGS["MARGIN"]

def draw_board(screen, board):
    for v in board.vehicles.values():
        color = (200, 0, 0) if v.name == 'X' else (100, 100, 255)
        x = MARGIN + v.col * CELL_SIZE
        y = MARGIN + v.row * CELL_SIZE
        width = CELL_SIZE * v.length if v.orientation == 'H' else CELL_SIZE
        height = CELL_SIZE if v.orientation == 'H' else CELL_SIZE * v.length
        pygame.draw.rect(screen, color, (x, y, width, height), border_radius=10)
        font = pygame.font.Font(None, 36)
        text = font.render(v.name, True, (255, 255, 255))
        screen.blit(text, (x + width // 2 - 10, y + height // 2 - 10))

def run_playing(screen, clock, play_data):
    FONT = pygame.font.Font(None, 36)
    screen_width, screen_height = screen.get_size()

    # ---------- Load map and solve ----------
    map_name = play_data.get('map', 'map1')
    map_path = f'maps/map{map_name}.json'
    board = load_map_from_json(map_path)

    solver = BFSSolver(board.clone())
    solver.solve()
    solution = solver.solution

    play_data["solution_length"] = len(solution)
    play_data["expanded_nodes"] = solver.expanded_nodes
    play_data["time_taken"] = round(solver.time_taken, 3)

    move_index = 0
    paused = False
    running = True

    while running:
        screen.fill((0, 0, 50))

        # ---------- Render play_data in one horizontal line with space-between ----------
        num_items = len(play_data)
        padding = 100
        usable_width = screen_width - 2 * padding
        gap = usable_width // (num_items - 1) if num_items > 1 else 0
        y = 20

        for i, (key, value) in enumerate(play_data.items()):
            line = f"{key.capitalize()}: {value}"
            text_surface = FONT.render(line, True, (255, 255, 255))
            text_rect = text_surface.get_rect()
            x = padding + i * gap - text_rect.width // 2
            screen.blit(text_surface, (x, y))

        # ---------- Draw board ----------
        draw_board(screen, board)

        # ---------- Bottom hint ----------
        hint = FONT.render("[ESC] Menu | [SPACE] Pause/Continue", True, (255, 255, 255))
        hint_rect = hint.get_rect(center=(screen_width // 2, screen_height - 40))
        screen.blit(hint, hint_rect)

        # ---------- Event handling ----------
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return SETTINGS["SCENES"]["QUIT"]
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    return SETTINGS["SCENES"]["MENU"]
                elif event.key == pygame.K_SPACE:
                    paused = not paused

        if not paused and move_index < len(solution):
            vname, delta = solution[move_index]
            v = board.vehicles[vname]
            if v.orientation == 'H':
                v.col += delta
            else:
                v.row += delta
            move_index += 1
            time.sleep(0.3)

        pygame.display.flip()
        clock.tick(SETTINGS["FPS"])

    return SETTINGS["SCENES"]["MENU"]
