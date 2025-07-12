import pygame
from entities import Dropdown, Button
from core.map_loader import load_map_from_json
from solvers import get_solver_class
from config import SETTINGS

class PlayingScreen:
    def __init__(self, screen, clock):
        self.screen = screen
        self.clock = clock
        self.running = True

        self.board = None
        self.solver = None
        self.stats = {}
        
        self.is_playing = False
        self.current_step = 0
        self.solution_path = []
        self.animation_timer = 0
        self.animation_speed = 500  # milliseconds between steps

        self.init_ui()

        self.prev_selected_map = "map1.json"
        self.prev_selected_algo = "BFS"
        
        self.load_game()

    def init_ui(self):
        self.map_dropdown = Dropdown(
            SETTINGS["WINDOW_SIZE"][0] - 250, 10, 110, 30,
            ["map1.json", "map2.json"]
        )
        self.algo_dropdown = Dropdown(
            SETTINGS["WINDOW_SIZE"][0] - 100, 10, 50, 30,
            ["BFS", "DFS", "UCS", "A*"]
        )

        # Thêm nút Play
        self.play_button = Button(
            450, 250, 80, 40, "Play", 
            bg_color=(70, 130, 180), 
            text_color=(255, 255, 255)
        )
        
        # Thêm nút Reset
        self.reset_button = Button(
            540, 250, 80, 40, "Reset",
            bg_color=(180, 70, 70),
            text_color=(255, 255, 255)
        )

        self.map_dropdown.set_selected("map1.json")
        self.algo_dropdown.set_selected("BFS")

    def load_game(self):
        selected_map_text = self.map_dropdown.get_selected()
        selected_algo_text = self.algo_dropdown.get_selected()

        board_data = load_map_from_json(f"maps/{selected_map_text}")
        self.board = board_data
        solver_class = get_solver_class(selected_algo_text)
        self.solver = solver_class(self.board)
        self.stats = self.solver.solve()
        
        # Reset animation state
        self.is_playing = False
        self.current_step = 0
        self.solution_path = self.stats.get('path', [])
        self.animation_timer = 0

    def run(self):
        while self.running:
            dt = self.clock.get_time()
            
            for event in pygame.event.get():
                result = self.handle_event(event)
                if result == "menu":
                    return "menu"
                elif result == "quit":
                    return "quit"

            current_map = self.map_dropdown.get_selected()
            current_algo = self.algo_dropdown.get_selected()

            if current_map != self.prev_selected_map or current_algo != self.prev_selected_algo:
                self.load_game()
                self.prev_selected_map = current_map
                self.prev_selected_algo = current_algo

            # Update animation
            self.update_animation(dt)

            self.render()
            self.clock.tick(60)

    def handle_event(self, event):
        if event.type == pygame.QUIT:
            return "quit"

        self.map_dropdown.handle_event(event)
        self.algo_dropdown.handle_event(event)
        
        # Handle button clicks
        if self.play_button.handle_event(event):
            self.toggle_play()
        
        if self.reset_button.handle_event(event):
            self.reset_animation()

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                return "menu"
            elif event.key == pygame.K_SPACE:  # Space để toggle play
                self.toggle_play()
            elif event.key == pygame.K_r:  # R để reset
                self.reset_animation()
                
        return None

    def toggle_play(self):
        if self.solution_path:
            self.is_playing = not self.is_playing
            self.play_button.text = "Pause" if self.is_playing else "Play"

    def reset_animation(self):
        self.is_playing = False
        self.current_step = 0
        self.animation_timer = 0
        self.play_button.text = "Play"
        # Reset board to initial state
        if self.board:
            self.board.reset_to_initial_state()

    def update_animation(self, dt):
        if self.is_playing and self.solution_path:
            self.animation_timer += dt
            
            if self.animation_timer >= self.animation_speed:
                if self.current_step < len(self.solution_path):
                    # Apply current step to board
                    if self.board:
                        self.board.apply_move(self.solution_path[self.current_step])
                    self.current_step += 1
                    self.animation_timer = 0
                else:
                    # Animation finished
                    self.is_playing = False
                    self.play_button.text = "Play"

    def render(self):
        self.screen.fill((30, 30, 30))
        self.draw_header()
        self.draw_main()
        self.draw_footer()
        pygame.display.flip()

    def draw_header(self):
        font = pygame.font.Font(None, 40)
        title = font.render("Rush Hour Solver", True, (255, 255, 255))
        self.screen.blit(title, (50, 10))
        self.map_dropdown.draw(self.screen)
        self.algo_dropdown.draw(self.screen)

    def draw_main(self):
        if self.board:
            self.board.draw(self.screen, pos=(50, 80))
        self.draw_stats()
        self.draw_controls()

    def draw_stats(self):
        if not self.stats:
            return
        font = pygame.font.Font(None, 30)
        
        algo_text = self.algo_dropdown.get_selected()

        labels = [
            f"Algorithm: {algo_text}",
            f"Time: {self.stats['time']:.2f}s",
            f"Space Used: {self.stats['space']}",
            f"Expanded Nodes: {self.stats['expanded']}"
        ]
        for i, text in enumerate(labels):
            txt = font.render(text, True, (200, 200, 200))
            self.screen.blit(txt, (450, 100 + i * 40))

    def draw_controls(self):
        # Draw buttons
        self.play_button.draw(self.screen)
        self.reset_button.draw(self.screen)
        
        # Draw progress info
        if self.solution_path:
            font = pygame.font.Font(None, 24)
            progress_text = f"Step: {self.current_step}/{len(self.solution_path)}"
            txt = font.render(progress_text, True, (200, 200, 200))
            self.screen.blit(txt, (450, 300))

    def draw_footer(self):
        font = pygame.font.Font(None, 26)
        msg = font.render("Press ESC to return to menu", True, (180, 180, 180))
        self.screen.blit(
            msg,
            (
                SETTINGS["WINDOW_SIZE"][0] // 2 - msg.get_width() // 2,
                SETTINGS["WINDOW_SIZE"][1] - 40
            )
        )
