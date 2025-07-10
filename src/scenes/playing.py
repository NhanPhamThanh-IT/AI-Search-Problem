import pygame
from entities.dropdown import Dropdown
from core.map_loader import load_map_from_json
from solvers import get_solver_class
from config import SETTINGS

class PlayingScreen:
    def __init__(self, screen, clock, play_data):
        self.screen = screen
        self.clock = clock
        self.running = True

        # Từ play_data lấy thông tin map và thuật toán
        self.selected_map = play_data.get("map", "map1.json")
        self.selected_algo = play_data.get("algorithm", "BFS")

        self.board = None
        self.solver = None
        self.stats = {}

        self.init_ui()
        self.load_game()

    def init_ui(self):
        self.map_dropdown = Dropdown(100, 10, 150, 30, ["map1.json", "map2.json"])
        self.algo_dropdown = Dropdown(300, 10, 150, 30, ["BFS", "DFS", "UCS", "A*"])
        self.map_dropdown.set_selected(self.selected_map)
        self.algo_dropdown.set_selected(self.selected_algo)

    def load_game(self):
        board_data = load_map_from_json(f"maps/{self.selected_map}")
        self.board = board_data
        solver_class = get_solver_class(self.selected_algo)
        self.solver = solver_class(self.board)
        self.stats = self.solver.solve()

    def run(self):
        while self.running:
            for event in pygame.event.get():
                result = self.handle_event(event)
                if result == "menu":
                    return "menu"
                elif result == "quit":
                    return "quit"

            self.render()
            self.clock.tick(60)

    def handle_event(self, event):
        if event.type == pygame.QUIT:
            return "quit"

        self.map_dropdown.handle_event(event)
        self.algo_dropdown.handle_event(event)

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_RETURN:
                self.selected_map = self.map_dropdown.get_selected()
                self.selected_algo = self.algo_dropdown.get_selected()
                self.load_game()
            elif event.key == pygame.K_ESCAPE:
                return "menu"
        return None

    def render(self):
        self.screen.fill((30, 30, 30))
        self.draw_header()
        self.draw_main()
        self.draw_footer()
        pygame.display.flip()

    def draw_header(self):
        font = pygame.font.Font(None, 40)
        title = font.render("Rush Hour Solver", True, (255, 255, 255))
        self.screen.blit(title, (SETTINGS["WINDOW_SIZE"][0] // 2 - title.get_width() // 2, 10))
        self.map_dropdown.draw(self.screen)
        self.algo_dropdown.draw(self.screen)

    def draw_main(self):
        if self.board:
            self.board.draw(self.screen, pos=(50, 80))
        self.draw_stats()

    def draw_stats(self):
        if not self.stats:
            return
        font = pygame.font.Font(None, 30)
        labels = [
            f"Algorithm: {self.selected_algo}",
            f"Time: {self.stats['time']:.2f}s",
            f"Space Used: {self.stats['space']}",
            f"Expanded Nodes: {self.stats['expanded']}"
        ]
        for i, text in enumerate(labels):
            txt = font.render(text, True, (200, 200, 200))
            self.screen.blit(txt, (450, 100 + i * 40))

    def draw_footer(self):
        font = pygame.font.Font(None, 26)
        msg = font.render("Press ESC to return to menu", True, (180, 180, 180))
        self.screen.blit(msg, (SETTINGS["WINDOW_SIZE"][0] // 2 - msg.get_width() // 2, SETTINGS["WINDOW_SIZE"][1] - 40))
