"""Game controller for Rush Hour auto-solver animation."""

import pygame
import time
from typing import List, Tuple, Optional
from display import GameDisplay
from config import ANIMATION_DELAY, PAUSE_DURATION


class GameController:
    """Handles game logic and animation control."""
    
    def __init__(self, display: GameDisplay):
        """Initialize game controller with display."""
        self.display = display
        self.clock = pygame.time.Clock()
        self.paused = False
        
    def run_solution_animation(self, solution: List[Tuple], expanded_count: int) -> bool:
        """Run the solution animation with pause/resume functionality."""
        step_start_time = time.time()
        
        for step, (state, move, cost) in enumerate(solution):
            if not self._handle_step(step, state, move, cost, solution, expanded_count, step_start_time):
                return False
            
            # Update timer for next step
            step_start_time = time.time()
            
        return True
    
    def _handle_step(self, step: int, state, move: Optional[str], cost: int, 
                    solution: List[Tuple], expanded_count: int, 
                    step_start_time: float) -> bool:
        """Handle a single step in the animation."""
        while True:  # Loop to handle pause state
            if not self._handle_events():
                return False
            
            self._draw_current_state(step, state, move, cost, solution, expanded_count)
            self.clock.tick(60)
            
            if not self.paused:
                if self._should_advance_step(step, len(solution), step_start_time):
                    break
            
        return True
    
    def _handle_events(self) -> bool:
        """Handle pygame events. Returns False if should quit."""
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    self.paused = not self.paused
        return True
    
    def _draw_current_state(self, step: int, state, move: Optional[str], cost: int,
                           solution: List[Tuple], expanded_count: int) -> None:
        """Draw the current game state."""
        self.display.clear_screen()
        self.display.draw_board(state.board)
        
        total_cost = sum(s[2] for s in solution)
        self.display.draw_status_info(
            step=step,
            total_steps=len(solution) - 1,
            move=move,
            cost=cost,
            total_cost=total_cost,
            expanded_count=expanded_count,
            board_height=len(state.board) * 80,  # CELL_SIZE from config
            paused=self.paused
        )
        
        self.display.update_display()
    
    def _should_advance_step(self, step: int, total_steps: int, step_start_time: float) -> bool:
        """Check if enough time has passed to advance to the next step."""
        current_time = time.time()
        elapsed_time = current_time - step_start_time
        
        # Different wait times for different steps
        if step == total_steps - 1:
            wait_time = PAUSE_DURATION  # Last step waits longer
        else:
            wait_time = ANIMATION_DELAY  # Normal delay between steps
        
        return elapsed_time >= wait_time
