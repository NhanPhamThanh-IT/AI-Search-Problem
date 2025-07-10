import pygame
from config import SETTINGS
from utils import load_map_from_json

CELL_SIZE = SETTINGS["CELL_SIZE"]
MARGIN = SETTINGS["MARGIN"]

def draw_board(screen, board):
    # Vẽ grid (lưới)
    grid_color = (50, 50, 50)  # Màu xám đậm cho đường grid
    
    # Vẽ các đường dọc
    for i in range(7):  # 6x6 grid cần 7 đường dọc
        x = MARGIN + i * CELL_SIZE
        pygame.draw.line(screen, grid_color, (x, MARGIN), (x, MARGIN + 6 * CELL_SIZE), 1)
    
    # Vẽ các đường ngang
    for i in range(7):  # 6x6 grid cần 7 đường ngang
        y = MARGIN + i * CELL_SIZE
        pygame.draw.line(screen, grid_color, (MARGIN, y), (MARGIN + 6 * CELL_SIZE, y), 1)
    
    # Vẽ các vehicles
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
    # ---------- Load map JSON ----------
    map_name = play_data.get('map', '1')
    map_path = f'maps/map{map_name}.json'

    # Load JSON from file
    with open(map_path, 'r') as f:
        json_str = f.read()
    board = load_map_from_json(json_str)

    running = True
    while running:
        screen.fill((0, 0, 50))

        # Xử lý sự kiện quit
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        # Vẽ board
        draw_board(screen, board)

        pygame.display.flip()
        clock.tick(60)
