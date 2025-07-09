"""Configuration constants for Rush Hour game display."""

# Display configuration
CELL_SIZE = 80
MARGIN = 10
FONT_SIZE = 36
ANIMATION_DELAY = 0.3  # Seconds between steps (faster animation)
PAUSE_DURATION = 2.0  # Seconds to pause on final step

# Color palette for vehicles
VEHICLE_COLORS = {
    'A': (255, 200, 0),   # Yellow
    'B': (0, 200, 255),   # Light Blue
    'C': (0, 255, 100),   # Light Green
    'D': (200, 0, 255),   # Purple
    'E': (255, 100, 100), # Light Red
    'F': (100, 100, 255), # Light Blue
    'G': (255, 0, 200),   # Pink
    'X': (255, 0, 0)      # Red (target vehicle)
}

# UI Colors
BG_COLOR = (240, 248, 255)      # Alice blue background
EMPTY_COLOR = (245, 245, 245)   # White smoke for empty cells
GRID_COLOR = (70, 130, 180)     # Steel blue for grid lines
TEXT_COLOR = (25, 25, 112)      # Midnight blue text
PAUSE_COLOR = (255, 215, 0)     # Gold for pause message
FINAL_COLOR = (220, 20, 60)     # Crimson for final cost

# Menu Colors
MENU_BG_COLOR = (240, 248, 255) # Alice blue
BUTTON_COLOR = (70, 130, 180)   # Steel blue
BUTTON_HOVER_COLOR = (100, 149, 237)  # Cornflower blue
SELECTED_COLOR = (255, 140, 0)  # Dark orange

# Game settings
DEFAULT_MAP_FILE = './map.txt'

# Window settings
MIN_WINDOW_WIDTH = 800
MIN_WINDOW_HEIGHT = 600
