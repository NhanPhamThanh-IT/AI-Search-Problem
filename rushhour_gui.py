import pygame
import sys
import time
from rushhour_logic import RushHourSolver

# Display configuration
CELL_SIZE = 80
MARGIN = 10
FONT_SIZE = 36
ANIMATION_DELAY = 0.5  # Seconds between steps

# Color palette for vehicles
COLORS = {
    'A': (255, 200, 0), 'B': (0, 200, 255), 'C': (0, 255, 100),
    'D': (200, 0, 255), 'E': (255, 100, 100), 'F': (100, 100, 255),
    'G': (255, 0, 200), 'X': (255, 0, 0)
}

BG_COLOR = (230, 230, 230)
EMPTY_COLOR = (240, 240, 240)
GRID_COLOR = (100, 100, 100)
TEXT_COLOR = (0, 0, 0)
MAP_FILE = './map.txt'

def draw_board(screen, board, font):
    """Draw the game board on screen"""
    for i, row in enumerate(board):
        for j, cell in enumerate(row):
            color = COLORS.get(cell, EMPTY_COLOR) if cell != '.' else EMPTY_COLOR
            rect = pygame.Rect(MARGIN + j*CELL_SIZE, MARGIN + i*CELL_SIZE, CELL_SIZE, CELL_SIZE)
            
            pygame.draw.rect(screen, color, rect)
            pygame.draw.rect(screen, GRID_COLOR, rect, 2)
            
            if cell not in ['.', ' ']:
                text = font.render(cell, True, TEXT_COLOR)
                text_rect = text.get_rect(center=rect.center)
                screen.blit(text, text_rect)

def draw_info(screen, font, step, total_steps, move, cost, total_cost, expanded_count, board_height, paused=False):
    """Draw status information on screen"""
    y_pos = board_height + MARGIN
    
    info_lines = [
        f"Step {step}/{total_steps}",
        f"Move: {move or 'Start'} (cost {cost})",
        f"Expanded nodes: {expanded_count}",
        f"Total cost: {total_cost}" if step == total_steps else "",
        f"{'PAUSED - Press SPACE to continue' if paused else 'Press SPACE to pause'}"
    ]
    
    for i, line in enumerate(info_lines):
        if line:
            if "PAUSED" in line:
                color = (255, 255, 0)  # Yellow for pause message
            elif "Total cost" in line:
                color = (255, 0, 0)    # Red for total cost
            else:
                color = (0, 0, 0)      # Black for normal text
            text = font.render(line, True, color)
            screen.blit(text, (MARGIN, y_pos + i * FONT_SIZE))

def auto_play_solution(screen, font, solution, expanded_count):
    """Automatically play back the solution"""
    clock = pygame.time.Clock()
    paused = False
    step_start_time = time.time()
    
    for step, (state, move, cost) in enumerate(solution):
        while True:  # Loop to handle pause state
            # Check for events
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    return False
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_SPACE:
                        paused = not paused
                        if not paused:  # When unpausing, reset the step timer
                            step_start_time = time.time()
            
            # Draw screen
            screen.fill(BG_COLOR)
            draw_board(screen, state.board, font)
            
            total_cost = sum(s[2] for s in solution)
            draw_info(screen, font, step, len(solution)-1, move, cost, 
                     total_cost, expanded_count, len(state.board) * CELL_SIZE, paused)
            
            pygame.display.flip()
            clock.tick(60)
            
            # Handle timing and pause
            if not paused:
                current_time = time.time()
                elapsed_time = current_time - step_start_time
                
                # Determine wait time for current step
                if step == len(solution) - 1:
                    wait_time = 3.0  # Last step waits 3 seconds
                else:
                    wait_time = ANIMATION_DELAY  # Normal delay between steps
                
                if elapsed_time >= wait_time:
                    step_start_time = time.time()  # Reset timer for next step
                    break  # Move to next step
            
    return True

def main():
    """Main function - initialize and run the game"""
    # Solve the problem
    solver = RushHourSolver(MAP_FILE)
    solution, total_cost, expanded_nodes = solver.solve_bfs()
    
    if not solution:
        print("No solution found!")
        return
    
    # Initialize Pygame
    pygame.init()
    
    # Calculate window size
    board = solution[0][0].board
    width = len(board[0]) * CELL_SIZE + 2 * MARGIN
    height = len(board) * CELL_SIZE + 2 * MARGIN + 180  # Extra space for information including pause message
    
    screen = pygame.display.set_mode((width, height))
    pygame.display.set_caption("Rush Hour Auto Solver")
    font = pygame.font.SysFont(None, FONT_SIZE)
    
    # Automatically play back the solution
    auto_play_solution(screen, font, solution, len(expanded_nodes))
    
    # Exit
    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    main() 