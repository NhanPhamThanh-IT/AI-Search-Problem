import pygame
import sys
from rushhour_logic import RushHourSolver

CELL_SIZE = 80
MARGIN = 10
FONT_SIZE = 36
COLORS = {
    'A': (255, 200, 0),
    'B': (0, 200, 255),
    'C': (0, 255, 100),
    'D': (200, 0, 255),
    'E': (255, 100, 100),
    'F': (100, 100, 255),
    'G': (255, 0, 200),
    'X': (255, 0, 0),
}
BG_COLOR = (230, 230, 230)
EMPTY_COLOR = (240, 240, 240)
GRID_COLOR = (100, 100, 100)
TEXT_COLOR = (0, 0, 0)
MAP_FILE = './map.txt'

def draw_board(screen, board, font):
    rows = len(board)
    cols = len(board[0])
    for i in range(rows):
        for j in range(cols):
            cell = board[i][j]
            color = COLORS.get(cell, EMPTY_COLOR) if cell != '.' else EMPTY_COLOR
            rect = pygame.Rect(MARGIN + j*CELL_SIZE, MARGIN + i*CELL_SIZE, CELL_SIZE, CELL_SIZE)
            pygame.draw.rect(screen, color, rect)
            pygame.draw.rect(screen, GRID_COLOR, rect, 2)
            if cell != '.' and cell != ' ':
                text = font.render(cell, True, TEXT_COLOR)
                text_rect = text.get_rect(center=rect.center)
                screen.blit(text, text_rect)

def main():
    solver = RushHourSolver(MAP_FILE)
    solution, total_cost = solver.solve_ucs()
    if not solution:
        print("No solution found.")
        return
    pygame.init()
    board = solution[0][0].board
    rows, cols = len(board), len(board[0])
    width = cols * CELL_SIZE + 2*MARGIN
    height = rows * CELL_SIZE + 2*MARGIN + 60
    screen = pygame.display.set_mode((width, height))
    pygame.display.set_caption("Rush Hour Visualizer")
    font = pygame.font.SysFont(None, FONT_SIZE)
    step = 0
    clock = pygame.time.Clock()
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    if step < len(solution)-1:
                        step += 1
                elif event.key == pygame.K_LEFT:
                    if step > 0:
                        step -= 1
        screen.fill(BG_COLOR)
        draw_board(screen, solution[step][0].board, font)
        info = f"Step {step}/{len(solution)-1}"
        info2 = f"Move: {solution[step][1] if solution[step][1] else 'Start'} (cost {solution[step][2]})"
        info3 = f"Total cost: {total_cost}" if step == len(solution)-1 else ""
        info_text = font.render(info, True, (0,0,0))
        info2_text = font.render(info2, True, (0,0,0))
        screen.blit(info_text, (MARGIN, rows*CELL_SIZE + MARGIN))
        screen.blit(info2_text, (MARGIN, rows*CELL_SIZE + MARGIN + FONT_SIZE))
        if info3:
            info3_text = font.render(info3, True, (255,0,0))
            screen.blit(info3_text, (MARGIN+300, rows*CELL_SIZE + MARGIN))
        pygame.display.flip()
        clock.tick(30)
    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    main() 