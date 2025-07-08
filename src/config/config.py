"""Configuration constants for Rush Hour game display."""

# Display configuration
CELL_SIZE = 80
MARGIN = 10
FONT_SIZE = 36
ANIMATION_DELAY = 0.5  # Seconds between steps
PAUSE_DURATION = 3.0  # Seconds to pause on final step

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
BG_COLOR = (230, 230, 230)      # Light gray background
EMPTY_COLOR = (240, 240, 240)   # Empty cell color
GRID_COLOR = (100, 100, 100)    # Grid lines color
TEXT_COLOR = (0, 0, 0)          # Black text
PAUSE_COLOR = (255, 255, 0)     # Yellow for pause message
FINAL_COLOR = (255, 0, 0)       # Red for final cost

# Game settings
DEFAULT_MAP_FILE = './map.txt'
