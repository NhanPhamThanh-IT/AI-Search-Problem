"""Menu interface for Rush Hour game level selection."""

import pygame
import os
import sys
from typing import Tuple, List, Optional
from config.config import *

class GameMenu:
    def __init__(self, width: int = 800, height: int = 600):
        """Initialize the game menu."""
        pygame.init()
        self.width = width
        self.height = height
        self.screen = pygame.display.set_mode((width, height))
        pygame.display.set_caption("Rush Hour - Chọn màn chơi")
        
        # Fonts
        self.title_font = pygame.font.Font(None, 64)
        self.button_font = pygame.font.Font(None, 36)
        self.small_font = pygame.font.Font(None, 24)
        
        # Menu state
        self.selected_difficulty = None
        self.selected_level = None
        
        # Button dimensions
        self.button_width = 200
        self.button_height = 60
        self.level_button_size = 50
        
        # Colors
        self.button_color = (70, 130, 180)
        self.button_hover_color = (100, 160, 210)
        self.selected_color = (255, 165, 0)
        self.text_color = (255, 255, 255)
        
    def get_levels_for_difficulty(self, difficulty: str) -> List[str]:
        """Get available levels for a difficulty."""
        problem_path = f"problem/{difficulty}"
        if os.path.exists(problem_path):
            files = [f for f in os.listdir(problem_path) if f.endswith('.txt')]
            return sorted(files)
        return []
    
    def draw_button(self, text: str, x: int, y: int, width: int, height: int, 
                   is_hovered: bool = False, is_selected: bool = False) -> pygame.Rect:
        """Draw a button and return its rect."""
        color = self.selected_color if is_selected else (
            self.button_hover_color if is_hovered else self.button_color
        )
        
        button_rect = pygame.Rect(x, y, width, height)
        pygame.draw.rect(self.screen, color, button_rect)
        pygame.draw.rect(self.screen, (0, 0, 0), button_rect, 2)
        
        text_surface = self.button_font.render(text, True, self.text_color)
        text_rect = text_surface.get_rect(center=button_rect.center)
        self.screen.blit(text_surface, text_rect)
        
        return button_rect
    
    def draw_level_button(self, level_num: str, x: int, y: int, 
                         is_hovered: bool = False, is_selected: bool = False) -> pygame.Rect:
        """Draw a level selection button."""
        color = self.selected_color if is_selected else (
            self.button_hover_color if is_hovered else self.button_color
        )
        
        button_rect = pygame.Rect(x, y, self.level_button_size, self.level_button_size)
        pygame.draw.rect(self.screen, color, button_rect)
        pygame.draw.rect(self.screen, (0, 0, 0), button_rect, 2)
        
        text_surface = self.small_font.render(level_num, True, self.text_color)
        text_rect = text_surface.get_rect(center=button_rect.center)
        self.screen.blit(text_surface, text_rect)
        
        return button_rect
    
    def draw_menu(self, mouse_pos: Tuple[int, int]) -> dict:
        """Draw the main menu and return clickable areas."""
        self.screen.fill(BG_COLOR)
        clickable_areas = {}
        
        # Title
        title_text = self.title_font.render("RUSH HOUR", True, TEXT_COLOR)
        title_rect = title_text.get_rect(center=(self.width // 2, 80))
        self.screen.blit(title_text, title_rect)
        
        # Subtitle
        subtitle_text = self.button_font.render("Chọn độ khó:", True, TEXT_COLOR)
        subtitle_rect = subtitle_text.get_rect(center=(self.width // 2, 150))
        self.screen.blit(subtitle_text, subtitle_rect)
        
        # Difficulty buttons
        difficulties = ['easy', 'medium', 'hard']
        difficulty_labels = {'easy': 'Dễ', 'medium': 'Trung bình', 'hard': 'Khó'}
        
        start_x = (self.width - (len(difficulties) * (self.button_width + 20))) // 2
        
        for i, difficulty in enumerate(difficulties):
            x = start_x + i * (self.button_width + 20)
            y = 200
            
            is_hovered = pygame.Rect(x, y, self.button_width, self.button_height).collidepoint(mouse_pos)
            is_selected = self.selected_difficulty == difficulty
            
            button_rect = self.draw_button(
                difficulty_labels[difficulty], x, y, 
                self.button_width, self.button_height,
                is_hovered, is_selected
            )
            clickable_areas[f'difficulty_{difficulty}'] = button_rect
        
        # Level selection (if difficulty is selected)
        if self.selected_difficulty:
            levels = self.get_levels_for_difficulty(self.selected_difficulty)
            if levels:
                level_text = self.button_font.render("Chọn màn:", True, TEXT_COLOR)
                level_rect = level_text.get_rect(center=(self.width // 2, 320))
                self.screen.blit(level_text, level_rect)
                
                # Level grid
                cols = 5
                rows = (len(levels) + cols - 1) // cols
                grid_width = cols * (self.level_button_size + 10)
                grid_height = rows * (self.level_button_size + 10)
                
                start_x = (self.width - grid_width) // 2
                start_y = 360
                
                for i, level_file in enumerate(levels):
                    level_num = level_file.split('.')[0].replace('map', '')
                    row = i // cols
                    col = i % cols
                    
                    x = start_x + col * (self.level_button_size + 10)
                    y = start_y + row * (self.level_button_size + 10)
                    
                    is_hovered = pygame.Rect(x, y, self.level_button_size, self.level_button_size).collidepoint(mouse_pos)
                    is_selected = self.selected_level == level_file
                    
                    button_rect = self.draw_level_button(
                        level_num, x, y, is_hovered, is_selected
                    )
                    clickable_areas[f'level_{level_file}'] = button_rect
        
        # Start button (if both difficulty and level are selected)
        if self.selected_difficulty and self.selected_level:
            start_y = 520
            start_rect = self.draw_button(
                "BẮT ĐẦU CHƠI", 
                (self.width - self.button_width) // 2, start_y,
                self.button_width, self.button_height,
                pygame.Rect((self.width - self.button_width) // 2, start_y, 
                           self.button_width, self.button_height).collidepoint(mouse_pos)
            )
            clickable_areas['start_game'] = start_rect
        
        return clickable_areas
    
    def run(self) -> Optional[str]:
        """Run the menu and return selected map file path."""
        clock = pygame.time.Clock()
        running = True
        
        while running:
            mouse_pos = pygame.mouse.get_pos()
            clickable_areas = self.draw_menu(mouse_pos)
            
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    return None
                
                if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                    for area_name, area_rect in clickable_areas.items():
                        if area_rect.collidepoint(mouse_pos):
                            if area_name.startswith('difficulty_'):
                                self.selected_difficulty = area_name.split('_')[1]
                                self.selected_level = None  # Reset level selection
                            elif area_name.startswith('level_'):
                                self.selected_level = area_name.split('_')[1]
                            elif area_name == 'start_game':
                                map_path = f"problem/{self.selected_difficulty}/{self.selected_level}"
                                return map_path
            
            pygame.display.flip()
            clock.tick(60)
        
        return None
    
    def quit(self):
        """Clean up pygame resources."""
        pygame.quit()