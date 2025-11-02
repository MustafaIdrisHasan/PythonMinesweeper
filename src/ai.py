import random
import time
from typing import Tuple, List, Optional
from src.minesweeper import Minesweeper


class MinesweeperAI:
    """Enhanced AI solver with basic logic and probability-based guessing."""
    
    def __init__(self, game: Minesweeper, gui=None):
        self.game = game
        self.gui = gui
        self.difficulty = 0

    def make_move(self) -> bool:
        """Make a move using logic and probability. Returns True if move was made."""
        if self.game.game_over:
            return False
        
        # Try logical moves first
        if self.find_and_mark_mines():
            return True
        if self.find_and_reveal_safe_cells():
            return True
        
        # Try probability-based guessing
        best_move = self.find_best_probability_move()
        if best_move:
            x, y = best_move
            if self.gui:
                self.gui.update_info(f"AI: Probabilistic guess at ({x}, {y})")
            return self.game.reveal(x, y)
        
        # Fall back to random
        return self.find_random_move()

    def find_and_mark_mines(self) -> bool:
        """Find and flag cells that must be mines."""
        move_made = False
        for y in range(self.game.height):
            for x in range(self.game.width):
                if self.game.revealed[y][x] and self.game.board[y][x] > 0:
                    neighbors = self.game.get_neighbors(x, y)
                    hidden = [n for n in neighbors if not self.game.revealed[n[1]][n[0]] and not self.game.flagged[n[1]][n[0]]]
                    flagged = [n for n in neighbors if self.game.flagged[n[1]][n[0]]]
                    
                    # If hidden + flagged equals the number, all hidden must be mines
                    if len(hidden) + len(flagged) == self.game.board[y][x]:
                        for nx, ny in hidden:
                            if self.game.toggle_flag(nx, ny):
                                if self.gui:
                                    self.gui.update_info(f"AI: Flagging mine at ({nx}, {ny})")
                                    time.sleep(0.1)
                                move_made = True
        return move_made

    def find_and_reveal_safe_cells(self) -> bool:
        """Find and reveal cells that must be safe."""
        move_made = False
        for y in range(self.game.height):
            for x in range(self.game.width):
                if self.game.revealed[y][x] and self.game.board[y][x] > 0:
                    neighbors = self.game.get_neighbors(x, y)
                    flagged_count = sum(1 for nx, ny in neighbors if self.game.flagged[ny][nx])
                    
                    # If all mines are flagged, remaining neighbors are safe
                    if flagged_count == self.game.board[y][x]:
                        for nx, ny in neighbors:
                            if not self.game.revealed[ny][nx] and not self.game.flagged[ny][nx]:
                                if self.gui:
                                    self.gui.update_info(f"AI: Revealing safe cell ({nx}, {ny})")
                                    time.sleep(0.1)
                                self.game.reveal(nx, ny)
                                move_made = True
        return move_made

    def find_best_probability_move(self) -> Optional[Tuple[int, int]]:
        """Find the cell with lowest probability of being a mine."""
        safe_cells = []
        probability_map = {}
        
        for y in range(self.game.height):
            for x in range(self.game.width):
                if not self.game.revealed[y][x] and not self.game.flagged[y][x]:
                    prob = self.calculate_mine_probability(x, y)
                    if prob == 0:
                        safe_cells.append((x, y))
                    else:
                        probability_map[(x, y)] = prob
        
        if safe_cells:
            return random.choice(safe_cells)
        
        if probability_map:
            min_prob = min(probability_map.values())
            best_moves = [cell for cell, prob in probability_map.items() if prob == min_prob]
            return random.choice(best_moves)
        
        return None

    def calculate_mine_probability(self, x: int, y: int) -> float:
        """Calculate probability that (x, y) contains a mine based on neighbors."""
        neighbors = self.game.get_neighbors(x, y)
        total_prob = 0.0
        count = 0
        
        for nx, ny in neighbors:
            if self.game.revealed[ny][nx] and self.game.board[ny][nx] > 0:
                cell_neighbors = self.game.get_neighbors(nx, ny)
                hidden = [n for n in cell_neighbors if not self.game.revealed[n[1]][n[0]] and not self.game.flagged[n[1]][n[0]]]
                flagged = sum(1 for n in cell_neighbors if self.game.flagged[n[1]][n[0]])
                remaining = self.game.board[ny][nx] - flagged
                
                if remaining > 0 and len(hidden) > 0:
                    prob = remaining / len(hidden)
                    total_prob += prob
                    count += 1
        
        if count > 0:
            return total_prob / count
        
        # Default probability based on remaining mines and hidden cells
        remaining_mines = self.game.num_mines - self.game.get_flag_count()
        hidden_count = sum(1 for row in self.game.revealed for cell in row if not cell) - self.game.get_flag_count()
        
        if hidden_count > 0:
            return remaining_mines / hidden_count
        return 0.5

    def find_random_move(self) -> bool:
        """Make a random move when logic fails."""
        moves = [(x, y) for x in range(self.game.width) 
                 for y in range(self.game.height) 
                 if not self.game.revealed[y][x] and not self.game.flagged[y][x]]
        
        if moves:
            move = random.choice(moves)
            if self.gui:
                self.gui.update_info(f"AI: Random move at ({move[0]}, {move[1]})")
            return self.game.reveal(move[0], move[1])
        return False
