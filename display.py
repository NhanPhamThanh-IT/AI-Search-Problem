"""Display utilities for Rush Hour game visualization."""

import pygame
from typing import List, Tuple, Optional
from config import *


class GameDisplay:
    """Handles all pygame display operations for the Rush Hour game."""
    
    def __init__(self, board_width: int, board_height: int):
        """Initialize pygame display with calculated dimensions."""
        pygame.init()
        
        self.width = board_width * CELL_SIZE + 2 * MARGIN
        self.height = board_height * CELL_SIZE + 2 * MARGIN + 180
        
        self.screen = pygame.display.set_mode((self.width, self.height))
        pygame.display.set_caption("Rush Hour Auto Solver")
        self.font = pygame.font.SysFont(None, FONT_SIZE)
        
    def draw_board(self, board: List[List[str]]) -> None:
        """Draw the game board with vehicles."""
        for i, row in enumerate(board):
            for j, cell in enumerate(row):
                color = self._get_cell_color(cell)
                rect = pygame.Rect(
                    MARGIN + j * CELL_SIZE,
                    MARGIN + i * CELL_SIZE,
                    CELL_SIZE,
                    CELL_SIZE
                )
                
                # Draw cell background and border
                pygame.draw.rect(self.screen, color, rect)
                pygame.draw.rect(self.screen, GRID_COLOR, rect, 2)
                
                # Draw vehicle letter
                if cell not in ['.', ' ']:
                    self._draw_vehicle_label(cell, rect)
    
    def draw_status_info(self, step: int, total_steps: int, move: Optional[str], 
                        cost: int, total_cost: int, expanded_count: int, 
                        board_height: int, paused: bool = False) -> None:
        """Draw status information below the board."""
        y_pos = board_height + MARGIN
        
        status_lines = [
            f"Step {step}/{total_steps}",
            f"Move: {move or 'Start'} (cost {cost})",
            f"Expanded nodes: {expanded_count}",
            f"Total cost: {total_cost}" if step == total_steps else "",
            f"{'PAUSED - Press SPACE to continue' if paused else 'Press SPACE to pause'}"
        ]
        
        for i, line in enumerate(status_lines):
            if line:
                color = self._get_text_color(line, step, total_steps)
                text = self.font.render(line, True, color)
                self.screen.blit(text, (MARGIN, y_pos + i * FONT_SIZE))
    
    def clear_screen(self) -> None:
        """Clear the screen with background color."""
        self.screen.fill(BG_COLOR)
    
    def update_display(self) -> None:
        """Update the pygame display."""
        pygame.display.flip()
    
    def _get_cell_color(self, cell: str) -> Tuple[int, int, int]:
        """Get color for a cell based on its content."""
        if cell == '.' or cell == ' ':
            return EMPTY_COLOR
        return VEHICLE_COLORS.get(cell, EMPTY_COLOR)
    
    def _draw_vehicle_label(self, vehicle: str, rect: pygame.Rect) -> None:
        """Draw vehicle letter in the center of a cell."""
        text = self.font.render(vehicle, True, TEXT_COLOR)
        text_rect = text.get_rect(center=rect.center)
        self.screen.blit(text, text_rect)
    
    def _get_text_color(self, text: str, step: int, total_steps: int) -> Tuple[int, int, int]:
        """Get appropriate color for status text."""
        if "PAUSED" in text:
            return PAUSE_COLOR
        elif "Total cost" in text and step == total_steps:
            return FINAL_COLOR
        else:
            return TEXT_COLOR
    
    def quit(self) -> None:
        """Quit pygame."""
        pygame.quit()
