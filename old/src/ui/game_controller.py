"""Enhanced game controller for Rush Hour solver animation."""

import pygame
import time
from typing import List, Tuple
from config.config import ANIMATION_DELAY, PAUSE_DURATION, PAUSE_COLOR, FINAL_COLOR


class GameController:
    def __init__(self, display):
        """Initialize the game controller."""
        self.display = display
        self.running = True
    
    def run_solution_animation(self, solution: List[Tuple], expanded_nodes: int):
        """Run the solution animation with enhanced UI."""
        if not solution:
            self.display.display_message("Không tìm thấy lời giải!", FINAL_COLOR)
            time.sleep(PAUSE_DURATION)
            return
        
        total_steps = len(solution)
        total_cost = 0
        
        for step_num, step_data in enumerate(solution):
            # Check for quit events
            if not self.display.handle_events():
                self.running = False
                break
            
            # Handle different step data formats
            if isinstance(step_data, tuple):
                if len(step_data) == 3:
                    state, move, cost = step_data
                elif len(step_data) == 2:
                    state, move = step_data
                    cost = 1  # Default cost
                else:
                    state = step_data[0]
                    move = None
                    cost = 1
            else:
                state = step_data
                move = None
                cost = 1
            
            total_cost += cost
            
            # Prepare move description
            current_move = "Trạng thái ban đầu"
            if move:
                try:
                    # Try different move formats
                    if isinstance(move, tuple) and len(move) >= 3:
                        vehicle, direction, distance = move[:3]
                        direction_text = {
                            'up': 'lên',
                            'down': 'xuống', 
                            'left': 'trái',
                            'right': 'phải'
                        }.get(direction, str(direction))
                        current_move = f"{vehicle} đi {direction_text} {distance}"
                    elif isinstance(move, str):
                        current_move = move
                    else:
                        current_move = str(move)
                except Exception as e:
                    print(f"Error parsing move: {move}, Error: {e}")
                    current_move = f"Move: {str(move)}"
            
            # Display current state
            self.display.display_solution(
                state.board,
                step=step_num + 1,
                total_steps=total_steps,
                cost=total_cost,
                expanded_nodes=expanded_nodes,
                current_move=current_move
            )
            
            # Pause on final step
            if step_num == total_steps - 1:
                self.display.display_message(
                    f"Hoàn thành! Chi phí: {total_cost}", 
                    FINAL_COLOR
                )
                time.sleep(PAUSE_DURATION)
            else:
                time.sleep(ANIMATION_DELAY)
        
        # Wait for user input before closing
        print(f"\nGiải pháp hoàn thành!")
        print(f"Tổng số bước: {total_steps}")
        print(f"Tổng chi phí: {total_cost}")
        print(f"Số nodes đã mở rộng: {expanded_nodes}")
        print("Nhấn ESC hoặc đóng cửa sổ để thoát...")
        
        # Keep window open until user closes it
        clock = pygame.time.Clock()
        while self.running:
            if not self.display.handle_events():
                break
            clock.tick(60)
