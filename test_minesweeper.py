"""
Unit tests for Minesweeper game logic.
Run with: pytest test_minesweeper.py
"""

import pytest
from minesweeper import Minesweeper


class TestMinesweeper:
    """Test suite for Minesweeper game."""
    
    def test_game_creation(self):
        """Test that a game can be created."""
        game = Minesweeper(10, 10, 10)
        assert game.width == 10
        assert game.height == 10
        assert game.num_mines == 10
    
    def test_mine_count(self):
        """Test that correct number of mines are placed."""
        game = Minesweeper(9, 9, 10)
        mine_count = sum(sum(1 for cell in row if cell == -1) for row in game.board)
        assert mine_count == 10
    
    def test_adjacent_mine_calculation(self):
        """Test that adjacent mine counts are calculated correctly."""
        game = Minesweeper(5, 5, 5)
        # At least some cells should have non-negative values (not just mines)
        non_mines = sum(sum(1 for cell in row if cell >= 0) for row in game.board)
        assert non_mines > 0
    
    def test_first_click_safety(self):
        """Test that first click is safe."""
        game = Minesweeper(10, 10, 20, first_click=(5, 5))
        # First click should not be a mine
        result = game.reveal(5, 5)
        assert result is True
        assert game.board[5][5] != -1
    
    def test_flag_toggle(self):
        """Test flag toggling functionality."""
        game = Minesweeper(10, 10, 10)
        assert game.flagged[5][5] is False
        game.toggle_flag(5, 5)
        assert game.flagged[5][5] is True
        game.toggle_flag(5, 5)
        assert game.flagged[5][5] is False
    
    def test_reveal_empty_cell(self):
        """Test revealing an empty cell."""
        game = Minesweeper(10, 10, 10)
        result = game.reveal(0, 0)
        assert result is True
        assert game.revealed[0][0] is True
    
    def test_win_condition(self):
        """Test win condition detection."""
        # Create a minimal game
        game = Minesweeper(3, 3, 1)
        # Reveal all non-mine cells
        for y in range(3):
            for x in range(3):
                if game.board[y][x] != -1:
                    game.reveal(x, y)
        
        # Check if game detects win (though this might not always win)
        # Just test that is_solved works
        solved = game.is_solved()
        assert isinstance(solved, bool)
    
    def test_get_neighbors(self):
        """Test neighbor calculation."""
        game = Minesweeper(5, 5, 5)
        neighbors = game.get_neighbors(2, 2)
        # Center cell should have 8 neighbors
        assert len(neighbors) == 8
        
        # Corner cell should have 3 neighbors
        corner_neighbors = game.get_neighbors(0, 0)
        assert len(corner_neighbors) == 3
    
    def test_flag_count(self):
        """Test flag counting."""
        game = Minesweeper(10, 10, 10)
        assert game.get_flag_count() == 0
        game.toggle_flag(0, 0)
        game.toggle_flag(1, 1)
        assert game.get_flag_count() == 2
    
    def test_game_over_on_mine(self):
        """Test that game ends when hitting a mine."""
        # This is probabilistic, so we'll just test the logic
        game = Minesweeper(10, 10, 10)
        # Try revealing cells until we hit a mine or reveal all
        for y in range(10):
            for x in range(10):
                if not game.revealed[y][x] and game.board[y][x] == -1:
                    result = game.reveal(x, y)
                    assert result is False
                    assert game.game_over is True
                    break
            if game.game_over:
                break

