from core.vehicle import Vehicle
import pygame
from config import SETTINGS

class Board:
    def __init__(self, size, vehicles):
        self.size = size
        self.vehicles = {v.name: v for v in vehicles}
        self.initial_state = {}
        for name, vehicle in self.vehicles.items():
            self.initial_state[name] = {
                'row': vehicle.row,
                'col': vehicle.col,
                'length': vehicle.length,
                'orientation': vehicle.orientation,
                'name': vehicle.name
            }

    @classmethod
    def from_dict(cls, data):
        # Reset màu trước khi tạo vehicles mới để đảm bảo màu không trùng lặp
        Vehicle.reset_colors()
        vehicles = [Vehicle(**v) for v in data["vehicles"]]
        return cls(data["size"], vehicles)

    def reset_to_initial_state(self):
        for name, initial_data in self.initial_state.items():
            if name in self.vehicles:
                vehicle = self.vehicles[name]
                vehicle.row = initial_data['row']
                vehicle.col = initial_data['col']
                vehicle.length = initial_data['length']
                vehicle.orientation = initial_data['orientation']
                vehicle.name = initial_data['name']

    def apply_move(self, state):
        if not state:
            return
            
        for vehicle_data in state:
            row, col, length, orientation, name = vehicle_data
            if name in self.vehicles:
                vehicle = self.vehicles[name]
                vehicle.row = row
                vehicle.col = col
                vehicle.length = length
                vehicle.orientation = orientation

    def draw(self, screen, pos=(0, 0)):
        cell_size = SETTINGS["CELL_SIZE"]
        # Tạo font cho việc hiển thị tên vehicle
        font = pygame.font.Font(None, max(16, cell_size // 3))
        
        # Độ dày border của grid (có thể điều chỉnh theo ý muốn)
        border_width = max(1, cell_size // 30)  # Tối thiểu 1px, mỏng hơn
        
        for i in range(self.size[0]):
            for j in range(self.size[1]):
                pygame.draw.rect(screen, (255, 255, 255), (
                    pos[0] + j * cell_size, pos[1] + i * cell_size, cell_size, cell_size), border_width)

        for v in self.vehicles.values():
            color = v.get_color()  # Sử dụng màu riêng của từng vehicle
            rect = v.get_rect(pos, cell_size)
            pygame.draw.rect(screen, color, rect)
            
            # Vẽ tên vehicle lên màn hình
            v.draw_name(screen, pos, cell_size, font)
