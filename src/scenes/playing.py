import pygame
from entities import Dropdown, Button
from core import load_map_from_json
from solvers import get_solver_class
from config import SETTINGS
from utils import get_list_maps

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
        self.animation_speed = 500
        self.is_solved = False
        self.solving = False
        self.no_solution = False

        self.init_ui()

        self.prev_selected_map = "map1.json"
        self.prev_selected_algo = "BFS"
        
        self.load_game()

    def init_ui(self):
        self.map_dropdown = Dropdown(
            SETTINGS["WINDOW_SIZE"][0] - 250, 10, 110, 30,
            get_list_maps("maps")
        )
        self.algo_dropdown = Dropdown(
            SETTINGS["WINDOW_SIZE"][0] - 100, 10, 50, 30,
            ["BFS", "DFS", "UCS", "A*"]
        )

        self.play_button = Button(
            450, 250, 80, 40, "Play", 
            bg_color=(70, 130, 180), 
            text_color=(255, 255, 255)
        )
        
        self.reset_button = Button(
            540, 250, 80, 40, "Reset",
            bg_color=(180, 70, 70),
            text_color=(255, 255, 255)
        )

        self.map_dropdown.set_selected("map1.json")
        self.algo_dropdown.set_selected("BFS")

    def load_game(self):
        selected_map_text = self.map_dropdown.get_selected()

        board_data = load_map_from_json(f"maps/{selected_map_text}")
        self.board = board_data
        
        self.solver = None
        self.stats = {}
        self.is_playing = False
        self.current_step = 0
        self.solution_path = []
        self.animation_timer = 0
        self.is_solved = False
        self.solving = False
        self.no_solution = False
        self.play_button.text = "Play"

    def solve_puzzle(self):
        if not self.board or self.is_solved or self.solving:
            return
            
        self.solving = True
        self.no_solution = False
        self.play_button.text = "Solving..."
            
        selected_algo_text = self.algo_dropdown.get_selected()
        solver_class = get_solver_class(selected_algo_text)
        self.solver = solver_class(self.board)
        
        try:
            self.stats = self.solver.solve()
            self.solution_path = self.stats.get('path', [])
            
            if self.solution_path:
                self.is_solved = True
                self.play_button.text = "Play"
            else:
                self.no_solution = True
                self.play_button.text = "No Solution"
                
        except Exception as e:
            self.no_solution = True
            self.play_button.text = "Error"
            
        finally:
            self.solving = False

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

            self.update_animation(dt)

            self.render()
            self.clock.tick(60)

    def handle_event(self, event):
        if event.type == pygame.QUIT:
            return "quit"

        self.map_dropdown.handle_event(event)
        self.algo_dropdown.handle_event(event)
        
        if self.play_button.handle_event(event):
            self.toggle_play()
        
        if self.reset_button.handle_event(event):
            self.reset_animation()

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                return "menu"
            elif event.key == pygame.K_SPACE:
                self.toggle_play()
            elif event.key == pygame.K_r:
                self.reset_animation()
                
        return None

    def toggle_play(self):
        if self.solving:
            return
            
        if self.no_solution:
            return
            
        if not self.is_solved:
            self.solve_puzzle()
            return
            
        if self.solution_path:
            self.is_playing = not self.is_playing
            self.play_button.text = "Pause" if self.is_playing else "Play"

    def reset_animation(self):
        self.is_playing = False
        self.current_step = 0
        self.animation_timer = 0
        self.is_solved = False
        self.solving = False
        self.no_solution = False
        self.play_button.text = "Play"
        if self.board:
            self.board.reset_to_initial_state()
        
    def update_animation(self, dt):
        if self.is_playing and self.solution_path:
            self.animation_timer += dt
            
            if self.animation_timer >= self.animation_speed:
                if self.current_step < len(self.solution_path):
                    if self.board:
                        self.board.apply_move(self.solution_path[self.current_step])
                    self.current_step += 1
                    self.animation_timer = 0
                else:
                    self.is_playing = False
                    self.play_button.text = "Replay"

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
        font = pygame.font.Font(None, 30)
        
        algo_text = self.algo_dropdown.get_selected()

        if self.solving:
            labels = [
                f"Algorithm: {algo_text}",
                "🔄 Solving puzzle...",
                "Please wait...",
                ""
            ]
        elif self.no_solution:
            labels = [
                f"Algorithm: {algo_text}",
                "No solution found!",
                "Try different algorithm",
                "or check map validity"
            ]
        elif self.is_solved and self.stats:
            labels = [
                f"Algorithm: {algo_text}",
                f"Time: {self.stats['time']:.2f}s",
                f"Space Used: {self.stats['space']}",
                f"Expanded Nodes: {self.stats['expanded']}"
            ]
        else:
            labels = [
                f"Algorithm: {algo_text}",
                "Press Play to solve",
                "",
                ""
            ]
            
        for i, text in enumerate(labels):
            if text:
                color = (200, 200, 200)
                txt = font.render(text, True, color)
                self.screen.blit(txt, (450, 100 + i * 40))

    def draw_controls(self):
        if self.solving:
            self.play_button.bg_color = (150, 150, 50)
        elif self.no_solution:
            self.play_button.bg_color = (180, 70, 70)
        elif self.is_playing:
            self.play_button.bg_color = (180, 100, 70)
        elif self.is_solved:
            self.play_button.bg_color = (70, 180, 70)
        else:
            self.play_button.bg_color = (70, 130, 180)
        
        self.play_button.draw(self.screen)
        self.reset_button.draw(self.screen)
        
        if self.solution_path and not self.no_solution:
            font = pygame.font.Font(None, 24)
            progress_text = f"Step: {self.current_step}/{len(self.solution_path)}"
            txt = font.render(progress_text, True, (200, 200, 200))
            self.screen.blit(txt, (450, 300))
            
            if self.current_step >= len(self.solution_path) and not self.is_playing:
                completion_font = pygame.font.Font(None, 28)
                completion_text = "Result: Puzzle Solved!"
                completion_txt = completion_font.render(completion_text, True, (100, 255, 100))
                self.screen.blit(completion_txt, (450, 350))
            
            if len(self.solution_path) > 0:
                progress = self.current_step / len(self.solution_path)
                bar_width = 200
                bar_height = 10
                bar_x = 450
                bar_y = 320
                
                pygame.draw.rect(self.screen, (60, 60, 60), 
                               (bar_x, bar_y, bar_width, bar_height))
                
                progress_width = int(bar_width * progress)
                color = (100, 255, 100) if progress >= 1.0 else (100, 150, 255)
                pygame.draw.rect(self.screen, color, 
                               (bar_x, bar_y, progress_width, bar_height))
                
                pygame.draw.rect(self.screen, (150, 150, 150), 
                               (bar_x, bar_y, bar_width, bar_height), 2)
        
        elif self.no_solution:
            font = pygame.font.Font(None, 24)
            txt = font.render("No moves to display", True, (255, 100, 100))
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
