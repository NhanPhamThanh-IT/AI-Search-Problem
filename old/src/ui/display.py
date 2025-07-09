"""Enhanced display module for Rush Hour game visualization."""

import pygame
import sys
from typing import List, Tuple
from config.config import *


class GameDisplay:
    def __init__(self, width: int, height: int):
        """Initialize the game display with enhanced UI."""
        self.width = width
        self.height = height
        self.board_width = width
        self.board_height = height
        
        # Calculate window dimensions
        self.window_width = width * CELL_SIZE + 2 * MARGIN + 300  # Extra space for info panel
        self.window_height = height * CELL_SIZE + 2 * MARGIN + 100  # Extra space for title
        
        pygame.init()
        self.screen = pygame.display.set_mode((self.window_width, self.window_height))
        pygame.display.set_caption("Rush Hour Solver - Đang giải...")
        
        # Fonts
        self.title_font = pygame.font.Font(None, 48)
        self.info_font = pygame.font.Font(None, 32)
        self.small_font = pygame.font.Font(None, 24)
        
        # Board position
        self.board_x = MARGIN
        self.board_y = MARGIN + 60
        
        # Info panel position
        self.info_x = self.board_x + width * CELL_SIZE + 20
        self.info_y = self.board_y
    
    def clear_screen(self):
        """Clear the screen with background color."""
        self.screen.fill(BG_COLOR)
    
    def draw_board(self, board: List[List[str]]):
        """Draw the game board with enhanced graphics."""
        # Draw title
        title_text = self.title_font.render("RUSH HOUR SOLVER", True, TEXT_COLOR)
        title_rect = title_text.get_rect(center=(self.window_width // 2, 30))
        self.screen.blit(title_text, title_rect)
        
        # Draw board background
        board_rect = pygame.Rect(
            self.board_x - 5, self.board_y - 5,
            self.board_width * CELL_SIZE + 10,
            self.board_height * CELL_SIZE + 10
        )
        pygame.draw.rect(self.screen, (200, 200, 200), board_rect)
        pygame.draw.rect(self.screen, GRID_COLOR, board_rect, 3)
        
        # Draw cells
        for row in range(self.board_height):
            for col in range(self.board_width):
                cell_x = self.board_x + col * CELL_SIZE
                cell_y = self.board_y + row * CELL_SIZE
                
                # Cell background
                cell_rect = pygame.Rect(cell_x, cell_y, CELL_SIZE, CELL_SIZE)
                
                vehicle = board[row][col]
                if vehicle == '.':
                    pygame.draw.rect(self.screen, EMPTY_COLOR, cell_rect)
                else:
                    # Vehicle color
                    color = VEHICLE_COLORS.get(vehicle, (128, 128, 128))
                    pygame.draw.rect(self.screen, color, cell_rect)
                    
                    # Add gradient effect
                    overlay = pygame.Surface((CELL_SIZE, CELL_SIZE))
                    overlay.set_alpha(50)
                    overlay.fill((255, 255, 255))
                    self.screen.blit(overlay, (cell_x, cell_y))
                    
                    # Vehicle label
                    if vehicle != '.':
                        text_surface = self.info_font.render(vehicle, True, (0, 0, 0))
                        text_rect = text_surface.get_rect(center=cell_rect.center)
                        self.screen.blit(text_surface, text_rect)
                
                # Cell border
                pygame.draw.rect(self.screen, GRID_COLOR, cell_rect, 1)
        
        # Draw exit indicator
        exit_y = self.board_y + 2 * CELL_SIZE  # Assuming exit is at row 2
        exit_x = self.board_x + self.board_width * CELL_SIZE
        
        # Draw arrow pointing to exit
        arrow_points = [
            (exit_x + 5, exit_y + CELL_SIZE // 2 - 10),
            (exit_x + 5, exit_y + CELL_SIZE // 2 + 10),
            (exit_x + 20, exit_y + CELL_SIZE // 2)
        ]
        pygame.draw.polygon(self.screen, (255, 0, 0), arrow_points)
        
        # Exit label
        exit_text = self.small_font.render("EXIT", True, (255, 0, 0))
        self.screen.blit(exit_text, (exit_x + 25, exit_y + CELL_SIZE // 2 - 10))
    
    def draw_info_panel(self, step: int = 0, total_steps: int = 0, 
                       cost: int = 0, expanded_nodes: int = 0,
                       current_move: str = ""):
        """Draw information panel."""
        panel_x = self.info_x
        panel_y = self.info_y
        
        # Panel background
        panel_width = 250
        panel_height = 200
        panel_rect = pygame.Rect(panel_x, panel_y, panel_width, panel_height)
        pygame.draw.rect(self.screen, (240, 240, 240), panel_rect)
        pygame.draw.rect(self.screen, GRID_COLOR, panel_rect, 2)
        
        # Panel title
        title_text = self.info_font.render("THÔNG TIN", True, TEXT_COLOR)
        self.screen.blit(title_text, (panel_x + 10, panel_y + 10))
        
        y_offset = 50
        line_height = 25
        
        # Information lines
        info_lines = [
            f"Bước: {step}/{total_steps}",
            f"Chi phí: {cost}",
            f"Nodes mở rộng: {expanded_nodes}",
            f"Nước đi: {current_move}" if current_move else ""
        ]
        
        for i, line in enumerate(info_lines):
            if line:  # Only draw non-empty lines
                text_surface = self.small_font.render(line, True, TEXT_COLOR)
                self.screen.blit(text_surface, (panel_x + 10, panel_y + y_offset + i * line_height))
        
        # Progress bar
        if total_steps > 0:
            progress_y = panel_y + panel_height - 40
            progress_width = panel_width - 20
            progress_height = 20
            
            # Progress background
            progress_bg = pygame.Rect(panel_x + 10, progress_y, progress_width, progress_height)
            pygame.draw.rect(self.screen, (200, 200, 200), progress_bg)
            
            # Progress fill
            progress_fill_width = int((step / total_steps) * progress_width)
            if progress_fill_width > 0:
                progress_fill = pygame.Rect(panel_x + 10, progress_y, progress_fill_width, progress_height)
                pygame.draw.rect(self.screen, (0, 200, 0), progress_fill)
            
            pygame.draw.rect(self.screen, GRID_COLOR, progress_bg, 2)
    
    def display_solution(self, board: List[List[str]], step: int = 0, 
                        total_steps: int = 0, cost: int = 0, 
                        expanded_nodes: int = 0, current_move: str = ""):
        """Display the current state with enhanced UI."""
        self.clear_screen()
        self.draw_board(board)
        self.draw_info_panel(step, total_steps, cost, expanded_nodes, current_move)
        pygame.display.flip()
    
    def display_message(self, message: str, color: Tuple[int, int, int] = TEXT_COLOR):
        """Display a message overlay."""
        # Semi-transparent overlay
        overlay = pygame.Surface((self.window_width, self.window_height))
        overlay.set_alpha(128)
        overlay.fill((0, 0, 0))
        self.screen.blit(overlay, (0, 0))
        
        # Message box
        box_width = 400
        box_height = 100
        box_x = (self.window_width - box_width) // 2
        box_y = (self.window_height - box_height) // 2
        
        pygame.draw.rect(self.screen, (255, 255, 255), 
                        pygame.Rect(box_x, box_y, box_width, box_height))
        pygame.draw.rect(self.screen, color, 
                        pygame.Rect(box_x, box_y, box_width, box_height), 3)
        
        # Message text
        text_surface = self.info_font.render(message, True, color)
        text_rect = text_surface.get_rect(center=(box_x + box_width // 2, box_y + box_height // 2))
        self.screen.blit(text_surface, text_rect)
        
        pygame.display.flip()
    
    def handle_events(self) -> bool:
        """Handle pygame events. Returns False if quit event is detected."""
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    return False
        return True
    
    def refresh(self):
        """Refresh the display."""
        pygame.display.flip()
    
    def quit(self):
        """Clean up pygame resources."""
        pygame.quit()
