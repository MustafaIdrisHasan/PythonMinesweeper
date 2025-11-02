# 🎮 Minesweeper - Professional Edition

A feature-rich, professional-grade Minesweeper game implementation in Python with an intelligent AI solver, beautiful GUI, statistics tracking, and comprehensive gameplay features.

![Python](https://img.shields.io/badge/python-3.7+-blue.svg)
![License](https://img.shields.io/badge/license-MIT-green.svg)

## ✨ Features

### Core Gameplay
- **Classic Minesweeper mechanics** - Full implementation of the traditional game
- **First-click safety** - Guaranteed safe first click (mines placed after first click)
- **Smart flagging** - Right-click to flag/unflag mines
- **Chording** - Click a revealed number with all mines flagged to reveal remaining neighbors
- **Iterative flood-fill** - Efficient queue-based algorithm (no recursion limits)

### User Interface
- **Modern GUI** - Clean, intuitive tkinter-based interface
- **Multiple difficulty levels** - Beginner (9×9, 10 mines), Intermediate (16×16, 40 mines), Expert (30×16, 99 mines), and Custom
- **Real-time timer** - Tracks game time with second precision
- **Mine counter** - Shows remaining unflagged mines
- **Visual feedback** - Color-coded numbers, flags, and mine indicators
- **Keyboard shortcuts** - F2 or Ctrl+R for new game

### AI Solver
- **Intelligent solver** - Rule-based logic with probability calculations
- **Step-by-step visualization** - Watch the AI solve the puzzle
- **Multiple strategies**:
  - Logic-based mine detection
  - Safe cell inference
  - Probability-based guessing
  - Random fallback for unsolvable positions

### Statistics & Tracking
- **Comprehensive stats** - Games played, wins, losses, win rate
- **Best times** - Track fastest completion times per difficulty
- **Win streaks** - Current and best win streaks
- **Persistent storage** - Statistics saved to JSON file
- **Statistics dialog** - View detailed performance metrics

### Advanced Features
- **Game state management** - Proper win/loss detection
- **Custom difficulty** - Configure your own board size and mine count
- **Type hints** - Full type annotations for better code quality
- **Clean architecture** - Separated game logic, AI, and GUI components

## 🚀 Quick Start

### Prerequisites
- Python 3.7 or higher
- tkinter (usually included with Python)

### Installation

1. **Clone or download this repository**

2. **Install dependencies** (optional - for testing):
```bash
pip install -r requirements.txt
```

### Running the Game

Simply run:
```bash
python main.py
```

Or directly:
```bash
python gui.py
```

## 🎯 How to Play

### Basic Controls
- **Left-click** - Reveal a cell
- **Right-click** - Flag/unflag a mine
- **Middle-click** - Chord (reveal all unflagged neighbors if all mines are flagged)
- **F2 or Ctrl+R** - Start a new game

### Game Rules
1. Click a cell to reveal it
2. Numbers indicate how many mines are adjacent (1-8)
3. Right-click to flag cells you think contain mines
4. Clear all non-mine cells to win!
5. Clicking a mine ends the game

### AI Solver
Click the "AI Solver" button to watch an AI solve the puzzle automatically. Click "Stop AI" to regain control.

## 📁 Project Structure

```
PYTHON TRIAL MINESWEEPER/
├── main.py              # Entry point
├── gui.py              # GUI implementation
├── minesweeper.py      # Core game logic
├── ai.py               # AI solver
├── stats.py            # Statistics tracking
├── requirements.txt    # Dependencies
└── README.md           # This file
```

## 🔧 Technical Details

### Architecture
- **Object-oriented design** - Clean separation of concerns
- **Type hints** - Full type annotations throughout
- **Error handling** - Robust error checking and validation
- **Queue-based flood-fill** - Avoids Python recursion limits

### Key Algorithms
- **Mine placement** - Random placement with first-click exclusion
- **Flood-fill** - Iterative BFS using `collections.deque`
- **AI inference** - Constraint-based logic with probability calculations
- **Statistics persistence** - JSON-based data storage

## 🎨 Features Showcase

### Difficulty Levels
- **Beginner**: 9×9 grid, 10 mines - Perfect for learning
- **Intermediate**: 16×16 grid, 40 mines - Balanced challenge
- **Expert**: 30×16 grid, 99 mines - Ultimate test
- **Custom**: Configure your own challenge

### Statistics Tracking
Track your progress with detailed statistics:
- Total games played
- Win/loss record
- Win percentage
- Best times per difficulty
- Current and best win streaks

## 🐛 Known Limitations

- Sound effects not yet implemented (planned feature)
- Some advanced AI techniques (constraint solving) could be further optimized
- No network multiplayer (single-player only)

## 🔮 Future Enhancements

Potential additions for even more impressive features:
- Sound effects for actions
- Additional visual themes
- Animation effects
- Online leaderboards
- Tutorial mode
- Hint system

## 📝 Code Quality

- **Type hints** - Full type annotations
- **Docstrings** - Comprehensive documentation
- **Clean code** - Readable and maintainable
- **Modular design** - Easy to extend

## 🤝 Contributing

This is a personal project, but suggestions and improvements are welcome!

## 📄 License

This project is open source and available for educational purposes.

## 👤 Author

Built as a professional portfolio project demonstrating:
- Python programming skills
- GUI development with tkinter
- Algorithm implementation
- Software architecture
- Game development concepts

## 🎓 Learning Resources

This project demonstrates:
- Object-oriented programming
- GUI event handling
- Game state management
- AI/algorithm implementation
- Data persistence
- User experience design

---

**Enjoy playing Minesweeper! 🎉**

For questions or issues, feel free to explore the code - it's well-documented and easy to understand.

