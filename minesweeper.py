import random
from collections import deque
from typing import List, Tuple, Optional


class Minesweeper:
    """Minesweeper game engine with first-click safety and proper flagging."""
    
    def __init__(self, width: int, height: int, num_mines: int, first_click: Optional[Tuple[int, int]] = None):
        self.width = width
        self.height = height
        self.num_mines = min(num_mines, width * height - 1)  # Ensure at least one safe cell
        self.board = [[0 for _ in range(width)] for _ in range(height)]
        self.revealed = [[False for _ in range(width)] for _ in range(height)]
        self.flagged = [[False for _ in range(width)] for _ in range(height)]
        self.first_click = first_click
        self.game_over = False
        self.game_won = False
        self._mines_placed = False
        
        # Place mines after first click (for first-click safety)
        if first_click is None:
            self.place_mines()
            self.calculate_adjacent_mines()
            self._mines_placed = True

    def place_mines(self, exclude: Optional[Tuple[int, int]] = None):
        """Place mines randomly, excluding the first click and its neighbors."""
        excluded_cells = set()
        if exclude:
            excluded_cells.add(exclude)
            # Exclude neighbors for better first-click experience
            for dy in (-1, 0, 1):
                for dx in (-1, 0, 1):
                    nx, ny = exclude[0] + dx, exclude[1] + dy
                    if 0 <= nx < self.width and 0 <= ny < self.height:
                        excluded_cells.add((nx, ny))
        
        mines_placed = 0
        while mines_placed < self.num_mines:
            x = random.randint(0, self.width - 1)
            y = random.randint(0, self.height - 1)
            if (x, y) not in excluded_cells and self.board[y][x] != -1:
                self.board[y][x] = -1
                mines_placed += 1

    def calculate_adjacent_mines(self):
        """Calculate the number of adjacent mines for each cell."""
        for y in range(self.height):
            for x in range(self.width):
                if self.board[y][x] == -1:
                    continue
                count = 0
                for dy in (-1, 0, 1):
                    for dx in (-1, 0, 1):
                        if dx == 0 and dy == 0:
                            continue
                        nx, ny = x + dx, y + dy
                        if 0 <= nx < self.width and 0 <= ny < self.height:
                            if self.board[ny][nx] == -1:
                                count += 1
                self.board[y][x] = count

    def reveal(self, x: int, y: int) -> bool:
        """Reveal a cell. Returns True if safe, False if mine hit."""
        if self.revealed[y][x] or self.flagged[y][x] or self.game_over:
            return True
        
        # Place mines on first click if not already placed
        if not self._mines_placed:
            self.place_mines(exclude=(x, y))
            self.calculate_adjacent_mines()
            self._mines_placed = True
        
        self.revealed[y][x] = True
        
        if self.board[y][x] == -1:
            self.game_over = True
            return False
        
        # Iterative flood-fill for empty cells (queue-based, avoids recursion limits)
        if self.board[y][x] == 0:
            queue = deque([(x, y)])
            visited = {(x, y)}
            
            while queue:
                cx, cy = queue.popleft()
                
                for dy in (-1, 0, 1):
                    for dx in (-1, 0, 1):
                        if dx == 0 and dy == 0:
                            continue
                        nx, ny = cx + dx, cy + dy
                        
                        if (0 <= nx < self.width and 0 <= ny < self.height and 
                            not self.revealed[ny][nx] and not self.flagged[ny][nx] and 
                            (nx, ny) not in visited):
                            self.revealed[ny][nx] = True
                            visited.add((nx, ny))
                            
                            # Continue flood-fill if this is also empty
                            if self.board[ny][nx] == 0:
                                queue.append((nx, ny))
        
        # Check win condition
        if self.is_solved():
            self.game_won = True
            self.game_over = True
        
        return True

    def toggle_flag(self, x: int, y: int) -> bool:
        """Toggle flag on a cell. Returns True if flag was toggled."""
        if self.revealed[y][x] or self.game_over:
            return False
        self.flagged[y][x] = not self.flagged[y][x]
        return True

    def get_flag_count(self) -> int:
        """Get the number of flagged cells."""
        return sum(sum(row) for row in self.flagged)

    def is_solved(self) -> bool:
        """Check if all safe cells are revealed."""
        for y in range(self.height):
            for x in range(self.width):
                if self.board[y][x] != -1 and not self.revealed[y][x]:
                    return False
        return True

    def get_neighbors(self, x: int, y: int) -> List[Tuple[int, int]]:
        """Get all valid neighbor coordinates."""
        neighbors = []
        for dy in (-1, 0, 1):
            for dx in (-1, 0, 1):
                if dx == 0 and dy == 0:
                    continue
                nx, ny = x + dx, y + dy
                if 0 <= nx < self.width and 0 <= ny < self.height:
                    neighbors.append((nx, ny))
        return neighbors

    def chord(self, x: int, y: int) -> bool:
        """Chord operation: reveal all unflagged neighbors if all mines are flagged."""
        if not self.revealed[y][x] or self.board[y][x] == 0:
            return False
        
        neighbors = self.get_neighbors(x, y)
        flagged_count = sum(1 for nx, ny in neighbors if self.flagged[ny][nx])
        
        if flagged_count == self.board[y][x]:
            # All mines are flagged, reveal unflagged neighbors
            for nx, ny in neighbors:
                if not self.revealed[ny][nx] and not self.flagged[ny][nx]:
                    if not self.reveal(nx, ny):
                        return False  # Hit a mine
            return True
        return False
