# Rush Hour Puzzle Solver 🚗

Dự án cài đặt trò chơi Rush Hour và các thuật toán tìm kiếm để giải puzzle với giao diện đồ họa và console tương tác.

## ✨ Tính năng mới

### 🖼️ Giao diện đồ họa (GUI)

- Hiển thị bảng puzzle trực quan với màu sắc
- Các nút tương tác cho từng thuật toán
- Animation giải pháp theo thời gian thực
- Thống kê hiệu suất chi tiết
- Điều khiển tốc độ animation

### 🎮 Giao diện console tương tác

- Menu hệ thống tương tác
- Chế độ giải puzzle thủ công
- Animation từng bước giải pháp
- So sánh hiệu suất thuật toán
- Gợi ý nước đi tiếp theo

### 📊 Thuật toán được hỗ trợ

- **BFS (Breadth-First Search)** - Tìm giải pháp tối ưu
- **DFS (Depth-First Search)** - Tìm kiếm theo chiều sâu
- **UCS (Uniform Cost Search)** - Tìm kiếm chi phí đồng nhất
- **A\*** - Tìm kiếm với heuristic

## 🚀 Chạy nhanh

```bash
# Cài đặt dependencies
pip install -r requirements.txt

# Chạy launcher (khuyến nghị)
cd src
python demo_launcher.py
```

## 📁 Cấu trúc dự án

```
src/
├── rushhour/              # Core game logic
│   ├── game.py           # Main game class
│   ├── state.py          # Game state representation
│   ├── vehicle.py        # Vehicle objects
│   └── solver.py         # Search algorithms
├── gui_demo_rushhour.py  # 🖼️ GUI Demo với pygame
├── interactive_demo_rushhour.py  # 🎮 Interactive Console Demo
├── demo_rushhour.py      # 📊 Original Console Demo
├── demo_launcher.py      # 🚀 Main Launcher
├── DEMO_README.md        # Chi tiết hướng dẫn demo
└── [original files...]   # Các file gốc
```

## 🎯 Các cách chạy demo

### 1. Launcher (Khuyến nghị)

```bash
cd src
python demo_launcher.py
```

### 2. GUI Demo riêng lẻ

```bash
cd src
python gui_demo_rushhour.py
```

### 3. Interactive Console Demo

```bash
cd src
python interactive_demo_rushhour.py
```

### 4. Original Console Demo

```bash
cd src
python demo_rushhour.py
```

## 🎮 Hướng dẫn sử dụng

### GUI Demo

- Click các nút "Solve BFS/DFS/UCS/A\*" để tìm giải pháp
- "Animate Solution" để xem animation
- "Speed+/-" để điều chỉnh tốc độ
- **Phím tắt:** SPACE (animate), R (reset), ←/→ (step through)

### Interactive Console

- Chọn các tùy chọn từ menu
- Chế độ solving thủ công: `move X right`, `hint`, `reset`
- Xem so sánh hiệu suất tất cả thuật toán

## 📦 Requirements

- Python 3.7+
- pygame 2.0+ (cho GUI demo)

```bash
pip install pygame
```

## 🎯 Puzzle mẫu

Demo sử dụng puzzle 6x6 với:

- **Vehicle X** (đỏ) - Xe cần đưa ra exit
- **Vehicles A-G** - Các xe cản đường
- **Mục tiêu** - Di chuyển xe X đến biên phải

---

## 📖 Code Structure (Original)

### Key Classes

#### `RushHourVehicle`

- Represents a vehicle with position and orientation
- Handles vehicle properties and movement validation

#### `RushHourState`

- Represents the current state of the puzzle board
- Handles state transitions and goal checking
- Generates successor states for search algorithms

#### `RushHourSolver`

- Implements multiple search algorithms:
  - BFS (Breadth-First Search)
  - DFS (Depth-First Search)
  - UCS (Uniform Cost Search)
  - A\* (A-Star Search)

#### `GameDisplay`

- Handles all pygame visualization
- Draws board, vehicles, and status information
- Manages colors and UI elements

#### `GameController`

- Controls animation timing and user interaction
- Handles pause/resume functionality
- Manages game state transitions

## Features

- **Multiple Search Algorithms**: Compare different solving approaches
- **Visual Animation**: Watch the solution step-by-step
- **Pause/Resume**: Press SPACE to pause/resume animation
- **Clean Architecture**: Modular design for easy maintenance
- **Type Hints**: Full type annotations for better code clarity
- **Documentation**: Comprehensive docstrings

## Usage

```python
python main.py
```

## Key Improvements

1. **Separation of Concerns**: Each module has a single responsibility
2. **Type Safety**: Full type hints throughout the codebase
3. **Documentation**: Clear docstrings for all classes and methods
4. **Configuration**: Centralized configuration management
5. **Error Handling**: Improved error handling and validation
6. **Code Reusability**: Modular components that can be easily extended
7. **Clean Naming**: Clear, descriptive variable and method names

## Configuration

Edit `config.py` to customize:

- Display settings (cell size, colors, fonts)
- Animation timing
- Color schemes for different vehicles
- Default map file location

## Map Format

Maps are stored in text files with:

- `.` for empty spaces
- Letters (A-Z) for vehicles
- `X` for the target vehicle that needs to reach the exit
