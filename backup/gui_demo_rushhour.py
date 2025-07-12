"""
GUI Demo for Rush Hour Puzzle Solver
Provides a graphical interface to test the solver with the provided puzzle data
"""

import sys
import os
import pygame
import threading
import time
from typing import List, Tuple, Optional

sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from rushhour import RushHourGame
from entities.button import Button

class RushHourGUIDemo:
    def __init__(self):
        pygame.init()
        pygame.font.init()
        
        # Screen settings
        self.WINDOW_WIDTH = 1200
        self.WINDOW_HEIGHT = 800
        self.BOARD_SIZE = 400
        self.CELL_SIZE = self.BOARD_SIZE // 6
        
        # Colors
        self.COLORS = {
            'background': (40, 40, 50),
            'board': (60, 60, 70),
            'grid_line': (100, 100, 110),
            'empty_cell': (80, 80, 90),
            'target_car': (255, 100, 100),  # Red car (X)
            'vehicle_colors': {
                'A': (100, 150, 255),
                'B': (100, 255, 150),
                'C': (255, 255, 100),
                'D': (255, 150, 100),
                'E': (150, 100, 255),
                'F': (255, 100, 255),
                'G': (100, 255, 255),
                'X': (255, 100, 100)  # Target car
            },
            'button': (70, 70, 80),
            'button_hover': (90, 90, 100),
            'button_active': (50, 150, 50),
            'text': (255, 255, 255),
            'success': (100, 255, 100),
            'error': (255, 100, 100)
        }
        
        # Initialize display
        self.screen = pygame.display.set_mode((self.WINDOW_WIDTH, self.WINDOW_HEIGHT))
        pygame.display.set_caption("Rush Hour Puzzle Solver - GUI Demo")
        
        # Fonts
        self.font_small = pygame.font.Font(None, 24)
        self.font_medium = pygame.font.Font(None, 36)
        self.font_large = pygame.font.Font(None, 48)
        
        # Game components
        self.game = RushHourGame()
        self.current_algorithm = None
        self.solving = False
        self.solution_found = False
        self.solution_moves = []
        self.current_stats = {}
        self.animation_index = 0
        self.animation_states = []
        self.auto_play = False
        self.animation_speed = 1.0
        
        # UI elements
        self.buttons = []
        self.create_ui_elements()
        
        # Load the puzzle
        self.load_demo_puzzle()
        
        # Clock for controlling frame rate
        self.clock = pygame.time.Clock()
        
    def create_ui_elements(self):
        """Create all UI buttons and elements"""
        button_width = 120
        button_height = 40
        start_x = self.BOARD_SIZE + 50
        start_y = 50
        y_spacing = 60
        
        # Algorithm buttons
        algorithms = ['BFS', 'DFS', 'UCS', 'A*']
        for i, algo in enumerate(algorithms):
            button = Button(
                (start_x, start_y + i * y_spacing, button_width, button_height),
                f"Solve {algo}",
                self.font_small,
                lambda a=algo: self.solve_with_algorithm(a)
            )
            self.buttons.append(button)
        
        # Control buttons
        control_y = start_y + len(algorithms) * y_spacing + 30
        
        reset_button = Button(
            (start_x, control_y, button_width, button_height),
            "Reset Puzzle",
            self.font_small,
            self.reset_puzzle
        )
        self.buttons.append(reset_button)
        
        animate_button = Button(
            (start_x, control_y + y_spacing, button_width, button_height),
            "Animate Solution",
            self.font_small,
            self.start_animation
        )
        self.buttons.append(animate_button)
        
        # Speed control buttons
        speed_y = control_y + y_spacing * 2 + 20
        speed_up_button = Button(
            (start_x, speed_y, 50, button_height),
            "Speed+",
            self.font_small,
            self.increase_speed
        )
        self.buttons.append(speed_up_button)
        
        speed_down_button = Button(
            (start_x + 60, speed_y, 50, button_height),
            "Speed-",
            self.font_small,
            self.decrease_speed
        )
        self.buttons.append(speed_down_button)
        
    def load_demo_puzzle(self):
        """Load the demo puzzle data"""
        puzzle_data = {
            "size": [6, 6],
            "vehicles": [
                {"name": "A", "row": 0, "col": 2, "length": 2, "orientation": "H"},
                {"name": "B", "row": 1, "col": 1, "length": 2, "orientation": "H"},
                {"name": "C", "row": 1, "col": 4, "length": 2, "orientation": "V"},
                {"name": "D", "row": 1, "col": 5, "length": 2, "orientation": "V"},
                {"name": "E", "row": 4, "col": 0, "length": 2, "orientation": "H"},
                {"name": "F", "row": 4, "col": 2, "length": 2, "orientation": "V"},
                {"name": "G", "row": 4, "col": 4, "length": 2, "orientation": "H"},
                {"name": "X", "row": 2, "col": 1, "length": 2, "orientation": "H"}
            ]
        }
        
        self.game.load_puzzle(puzzle_data)
        
    def solve_with_algorithm(self, algorithm):
        """Solve puzzle with specified algorithm in a separate thread"""
        if self.solving:
            return
            
        self.current_algorithm = algorithm
        self.solving = True
        self.solution_found = False
        self.solution_moves = []
        self.current_stats = {}
        
        # Run solver in background thread
        thread = threading.Thread(target=self._solve_thread, args=(algorithm,))
        thread.daemon = True
        thread.start()
        
    def _solve_thread(self, algorithm):
        """Background thread for solving puzzle"""
        try:
            solution, stats = self.game.solve_puzzle(algorithm)
            
            self.solution_found = solution is not None
            if solution:
                self.solution_moves = solution
                # Generate animation states
                self.game.reset_puzzle()
                self.animation_states = [self.game.current_state.copy()]
                for vehicle, direction in solution:
                    self.game.make_move(vehicle, direction)
                    self.animation_states.append(self.game.current_state.copy())
                self.game.reset_puzzle()
                
            self.current_stats = stats
            
        except Exception as e:
            print(f"Error solving with {algorithm}: {e}")
            self.solution_found = False
            self.current_stats = {'error': str(e)}
            
        finally:
            self.solving = False
            
    def reset_puzzle(self):
        """Reset puzzle to initial state"""
        self.game.reset_puzzle()
        self.solution_found = False
        self.solution_moves = []
        self.animation_index = 0
        self.auto_play = False
        
    def start_animation(self):
        """Start animating the solution"""
        if self.solution_found and self.animation_states:
            self.animation_index = 0
            self.auto_play = True
            
    def increase_speed(self):
        """Increase animation speed"""
        self.animation_speed = min(self.animation_speed * 1.5, 10.0)
        
    def decrease_speed(self):
        """Decrease animation speed"""
        self.animation_speed = max(self.animation_speed / 1.5, 0.1)
        
    def draw_board(self, state=None):
        """Draw the Rush Hour board"""
        if state is None:
            state = self.game.current_state
            
        board_x = 50
        board_y = 50
        
        # Draw board background
        board_rect = pygame.Rect(board_x, board_y, self.BOARD_SIZE, self.BOARD_SIZE)
        pygame.draw.rect(self.screen, self.COLORS['board'], board_rect)
        
        # Draw grid lines
        for i in range(7):  # 0 to 6 for a 6x6 grid
            # Vertical lines
            x = board_x + i * self.CELL_SIZE
            pygame.draw.line(self.screen, self.COLORS['grid_line'], 
                           (x, board_y), (x, board_y + self.BOARD_SIZE))
            # Horizontal lines
            y = board_y + i * self.CELL_SIZE
            pygame.draw.line(self.screen, self.COLORS['grid_line'],
                           (board_x, y), (board_x + self.BOARD_SIZE, y))
        
        # Draw exit
        exit_y = board_y + 2 * self.CELL_SIZE
        pygame.draw.rect(self.screen, self.COLORS['success'],
                        (board_x + self.BOARD_SIZE, exit_y, 10, self.CELL_SIZE))
        
        # Draw vehicles
        for vehicle in state.vehicles:
            self.draw_vehicle(vehicle, board_x, board_y)
            
    def draw_vehicle(self, vehicle, board_x, board_y):
        """Draw a single vehicle on the board"""
        color = self.COLORS['vehicle_colors'].get(vehicle.name, (150, 150, 150))
        
        x = board_x + vehicle.col * self.CELL_SIZE + 2
        y = board_y + vehicle.row * self.CELL_SIZE + 2
        
        if vehicle.orientation == 'H':
            width = vehicle.length * self.CELL_SIZE - 4
            height = self.CELL_SIZE - 4
        else:
            width = self.CELL_SIZE - 4
            height = vehicle.length * self.CELL_SIZE - 4
            
        pygame.draw.rect(self.screen, color, (x, y, width, height), border_radius=5)
        
        # Draw vehicle name
        text = self.font_medium.render(vehicle.name, True, (255, 255, 255))
        text_rect = text.get_rect(center=(x + width//2, y + height//2))
        self.screen.blit(text, text_rect)
        
    def draw_info_panel(self):
        """Draw the information panel"""
        panel_x = self.BOARD_SIZE + 50
        panel_y = 350
        
        info_lines = []
        
        if self.solving:
            info_lines.append(f"Solving with {self.current_algorithm}...")
        elif self.solution_found:
            info_lines.extend([
                f"✅ Solution found with {self.current_algorithm}!",
                f"Moves: {len(self.solution_moves)}",
                f"Nodes explored: {self.current_stats.get('nodes_explored', 'N/A')}",
                f"Time: {self.current_stats.get('execution_time', 0):.4f}s",
                f"Max queue: {self.current_stats.get('max_queue_size', 'N/A')}"
            ])
            
            if self.auto_play and self.animation_states:
                step = min(self.animation_index, len(self.animation_states) - 1)
                info_lines.append(f"Animation step: {step}/{len(self.animation_states)-1}")
                
        elif self.current_stats:
            if 'error' in self.current_stats:
                info_lines.append(f"❌ Error: {self.current_stats['error']}")
            else:
                info_lines.extend([
                    f"❌ No solution found with {self.current_algorithm}",
                    f"Nodes explored: {self.current_stats.get('nodes_explored', 'N/A')}",
                    f"Time: {self.current_stats.get('execution_time', 0):.4f}s"
                ])
        else:
            info_lines.extend([
                "Rush Hour Puzzle Solver",
                "",
                "Click a 'Solve' button to find solution",
                "Use 'Animate Solution' to see moves",
                "Use Speed+/- to control animation",
                "",
                f"Animation Speed: {self.animation_speed:.1f}x"
            ])
            
        for i, line in enumerate(info_lines):
            color = self.COLORS['success'] if line.startswith('✅') else \
                   self.COLORS['error'] if line.startswith('❌') else \
                   self.COLORS['text']
            text = self.font_small.render(line, True, color)
            self.screen.blit(text, (panel_x, panel_y + i * 25))
            
    def draw_solution_moves(self):
        """Draw the solution moves list"""
        if not self.solution_moves:
            return
            
        panel_x = self.BOARD_SIZE + 50
        panel_y = 600
        
        title = self.font_medium.render("Solution Moves:", True, self.COLORS['text'])
        self.screen.blit(title, (panel_x, panel_y))
        
        # Show first 8 moves
        for i, (vehicle, direction) in enumerate(self.solution_moves[:8]):
            if panel_y + 30 + i * 20 > self.WINDOW_HEIGHT - 50:
                break
            text = f"{i+1:2d}. Move {vehicle} {direction}"
            color = self.COLORS['success'] if i < self.animation_index else self.COLORS['text']
            move_text = self.font_small.render(text, True, color)
            self.screen.blit(move_text, (panel_x, panel_y + 30 + i * 20))
            
        if len(self.solution_moves) > 8:
            more_text = self.font_small.render(f"... and {len(self.solution_moves) - 8} more", 
                                             True, self.COLORS['text'])
            self.screen.blit(more_text, (panel_x, panel_y + 30 + 8 * 20))
            
    def update_animation(self):
        """Update animation state"""
        if self.auto_play and self.animation_states:
            # Update animation based on speed
            if hasattr(self, '_last_animation_time'):
                current_time = time.time()
                if current_time - self._last_animation_time > (1.0 / self.animation_speed):
                    self.animation_index += 1
                    self._last_animation_time = current_time
                    
                    if self.animation_index >= len(self.animation_states):
                        self.auto_play = False
                        self.animation_index = len(self.animation_states) - 1
            else:
                self._last_animation_time = time.time()
                
    def run(self):
        """Main game loop"""
        running = True
        
        while running:
            mouse_pos = pygame.mouse.get_pos()
            
            # Handle events
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                    
                # Handle button events
                for button in self.buttons:
                    button.handle_event(event, mouse_pos)
                    
                # Handle keyboard controls
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_SPACE:
                        self.start_animation()
                    elif event.key == pygame.K_r:
                        self.reset_puzzle()
                    elif event.key == pygame.K_LEFT and self.animation_states:
                        self.animation_index = max(0, self.animation_index - 1)
                        self.auto_play = False
                    elif event.key == pygame.K_RIGHT and self.animation_states:
                        self.animation_index = min(len(self.animation_states) - 1, 
                                                 self.animation_index + 1)
                        self.auto_play = False
            
            # Update animation
            self.update_animation()
            
            # Update button hover states
            for button in self.buttons:
                button.hover = button.rect.collidepoint(mouse_pos)
            
            # Draw everything
            self.screen.fill(self.COLORS['background'])
            
            # Draw board with current animation state
            current_state = self.game.current_state
            if self.animation_states and 0 <= self.animation_index < len(self.animation_states):
                current_state = self.animation_states[self.animation_index]
            
            self.draw_board(current_state)
            
            # Draw UI elements
            for button in self.buttons:
                button.draw(self.screen)
                
            self.draw_info_panel()
            self.draw_solution_moves()
            
            # Draw title
            title = self.font_large.render("Rush Hour Puzzle Solver", True, self.COLORS['text'])
            title_rect = title.get_rect(center=(self.WINDOW_WIDTH // 2, 20))
            self.screen.blit(title, title_rect)
            
            # Draw controls hint
            hint_text = "Controls: SPACE=Animate, R=Reset, ←/→=Step through solution"
            hint = self.font_small.render(hint_text, True, self.COLORS['text'])
            self.screen.blit(hint, (10, self.WINDOW_HEIGHT - 25))
            
            pygame.display.flip()
            self.clock.tick(60)
            
        pygame.quit()

def main():
    """Run the GUI demo"""
    try:
        demo = RushHourGUIDemo()
        demo.run()
    except Exception as e:
        print(f"Error running GUI demo: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    main()
