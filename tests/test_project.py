#!/usr/bin/env python3
"""
Comprehensive project validation test.
Run this to check if everything works correctly.
"""

import sys
from typing import List, Tuple
from pathlib import Path

# Add src to path
sys.path.insert(0, str(Path(__file__).parent.parent))


def test_imports() -> Tuple[bool, str]:
    """Test that all modules can be imported."""
    try:
        from src.minesweeper import Minesweeper
        from src.ai import MinesweeperAI
        from src.stats import GameStats
        from src.gui import MinesweeperGUI
        return True, "[PASS] All modules imported successfully"
    except Exception as e:
        return False, f"[FAIL] Import failed: {e}"


def test_game_creation() -> Tuple[bool, str]:
    """Test basic game creation."""
    try:
        from src.minesweeper import Minesweeper
        game = Minesweeper(9, 9, 10)
        assert game.width == 9 and game.height == 9 and game.num_mines == 10
        return True, "[PASS] Game creation works correctly"
    except Exception as e:
        return False, f"[FAIL] Game creation failed: {e}"


def test_game_logic() -> Tuple[bool, str]:
    """Test core game logic."""
    try:
        from src.minesweeper import Minesweeper
        game = Minesweeper(10, 10, 10)
        
        # Test reveal
        result = game.reveal(0, 0)
        assert result is True
        assert game.revealed[0][0] is True
        
        # Test flag toggle
        flag_result = game.toggle_flag(5, 5)
        assert flag_result is True
        assert game.flagged[5][5] is True
        game.toggle_flag(5, 5)
        assert game.flagged[5][5] is False
        
        return True, "[PASS] Game logic (reveal, flag) works correctly"
    except Exception as e:
        return False, f"[FAIL] Game logic failed: {e}"


def test_neighbors() -> Tuple[bool, str]:
    """Test neighbor calculation."""
    try:
        from src.minesweeper import Minesweeper
        game = Minesweeper(5, 5, 5)
        
        # Center cell should have 8 neighbors
        neighbors = game.get_neighbors(2, 2)
        assert len(neighbors) == 8
        
        # Corner cell should have 3 neighbors
        corner_neighbors = game.get_neighbors(0, 0)
        assert len(corner_neighbors) == 3
        
        return True, "[PASS] Neighbor calculation works correctly"
    except Exception as e:
        return False, f"[FAIL] Neighbor calculation failed: {e}"


def test_first_click_safety() -> Tuple[bool, str]:
    """Test first-click safety."""
    try:
        from src.minesweeper import Minesweeper
        # First click should be safe
        game = Minesweeper(10, 10, 20)
        result = game.reveal(5, 5)
        assert result is True
        assert game.board[5][5] != -1
        return True, "[PASS] First-click safety works"
    except Exception as e:
        return False, f"[FAIL] First-click safety failed: {e}"


def test_statistics() -> Tuple[bool, str]:
    """Test statistics tracking."""
    try:
        from src.stats import GameStats
        stats = GameStats()
        
        # Record a game
        stats.record_game(True, 120.5, 'beginner')
        win_rate = stats.get_win_rate()
        best_time = stats.get_best_time('beginner')
        
        assert best_time == 120.5
        assert win_rate > 0
        
        return True, "[PASS] Statistics tracking works correctly"
    except Exception as e:
        return False, f"[FAIL] Statistics failed: {e}"


def test_ai() -> Tuple[bool, str]:
    """Test AI solver."""
    try:
        from src.minesweeper import Minesweeper
        from src.ai import MinesweeperAI
        
        game = Minesweeper(10, 10, 10)
        ai = MinesweeperAI(game)
        
        # AI should be able to make a move
        move = ai.make_move()
        assert isinstance(move, bool)
        
        return True, "[PASS] AI solver works correctly"
    except Exception as e:
        return False, f"[FAIL] AI solver failed: {e}"


def test_flag_count() -> Tuple[bool, str]:
    """Test flag counting."""
    try:
        from src.minesweeper import Minesweeper
        game = Minesweeper(10, 10, 10)
        
        assert game.get_flag_count() == 0
        game.toggle_flag(0, 0)
        game.toggle_flag(1, 1)
        assert game.get_flag_count() == 2
        
        return True, "[PASS] Flag counting works correctly"
    except Exception as e:
        return False, f"[FAIL] Flag counting failed: {e}"


def test_chording() -> Tuple[bool, str]:
    """Test chording functionality."""
    try:
        from src.minesweeper import Minesweeper
        # This is a probabilistic test, just verify method exists and runs
        game = Minesweeper(5, 5, 5)
        game.reveal(2, 2)  # Reveal a cell first
        
        # Chord should return bool (may return False if conditions not met)
        result = game.chord(2, 2)
        assert isinstance(result, bool)
        
        return True, "[PASS] Chording method works"
    except Exception as e:
        return False, f"[FAIL] Chording failed: {e}"


def run_all_tests() -> Tuple[int, int]:
    """Run all tests and return (passed, total)."""
    tests = [
        test_imports,
        test_game_creation,
        test_game_logic,
        test_neighbors,
        test_first_click_safety,
        test_statistics,
        test_ai,
        test_flag_count,
        test_chording,
    ]
    
    passed = 0
    total = len(tests)
    results: List[str] = []
    
    print("=" * 60)
    print("PROJECT VALIDATION TEST SUITE")
    print("=" * 60)
    print()
    
    for test_func in tests:
        success, message = test_func()
        results.append(message)
        if success:
            passed += 1
        print(message)
    
    print()
    print("=" * 60)
    print(f"RESULTS: {passed}/{total} tests passed")
    print("=" * 60)
    
    if passed == total:
        print("\n[SUCCESS] ALL TESTS PASSED! Project is working correctly.")
        return passed, total
    else:
        print(f"\n[WARNING] {total - passed} test(s) failed. Please review the errors above.")
        return passed, total


if __name__ == "__main__":
    try:
        passed, total = run_all_tests()
        sys.exit(0 if passed == total else 1)
    except KeyboardInterrupt:
        print("\n\nTest interrupted by user.")
        sys.exit(1)
    except Exception as e:
        print(f"\n\n[ERROR] Unexpected error: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)

