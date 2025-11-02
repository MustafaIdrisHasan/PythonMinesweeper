#!/usr/bin/env python3
"""
Minesweeper - Professional Edition
A feature-rich Minesweeper game implementation with AI solver.

Run this file to start the game.
"""

from src.gui import MinesweeperGUI


def main():
    """Main entry point for the Minesweeper game."""
    app = MinesweeperGUI()
    app.run()


if __name__ == "__main__":
    main()

