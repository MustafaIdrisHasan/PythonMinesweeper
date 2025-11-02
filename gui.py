import tkinter as tk
from tkinter import ttk, messagebox
import time
from typing import Optional, Tuple
from minesweeper import Minesweeper
from ai import MinesweeperAI
from stats import GameStats


class MinesweeperGUI:
    """Modern Minesweeper GUI with all features."""
    
    # Color scheme
    COLORS = {
        'bg': '#2b2b2b',
        'cell_bg': '#c0c0c0',
        'cell_hidden': '#d3d3d3',
        'cell_revealed': '#ffffff',
        'cell_flag': '#ff0000',
        'mine': '#000000',
        'text': '#000000',
        'numbers': ['', '#0000ff', '#008000', '#ff0000', '#000080', '#800000', '#008080', '#000000', '#808080']
    }
    
    DIFFICULTIES = {
        'Beginner': (9, 9, 10),
        'Intermediate': (16, 16, 40),
        'Expert': (30, 16, 99),
        'Custom': None
    }
    
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("Minesweeper - Professional Edition")
        self.root.configure(bg=self.COLORS['bg'])
        
        # Game state
        self.game: Optional[Minesweeper] = None
        self.ai: Optional[MinesweeperAI] = None
        self.stats = GameStats()
        self.current_difficulty = 'Beginner'
        self.start_time = None
        self.timer_running = False
        
        # UI Components
        self.cells = []
        self.mine_counter_label = None
        self.timer_label = None
        self.info_label = None
        
        self.setup_ui()
        self.new_game()
        
    def setup_ui(self):
        """Setup the user interface."""
        # Top frame for controls
        top_frame = tk.Frame(self.root, bg=self.COLORS['bg'], pady=10)
        top_frame.pack(fill=tk.X)
        
        # Difficulty selection
        diff_frame = tk.Frame(top_frame, bg=self.COLORS['bg'])
        diff_frame.pack(side=tk.LEFT, padx=10)
        
        tk.Label(diff_frame, text="Difficulty:", bg=self.COLORS['bg'], 
                fg='white', font=('Arial', 10, 'bold')).pack(side=tk.LEFT, padx=5)
        
        self.diff_var = tk.StringVar(value=self.current_difficulty)
        diff_menu = ttk.Combobox(diff_frame, textvariable=self.diff_var, 
                                 values=list(self.DIFFICULTIES.keys()),
                                 state='readonly', width=12)
        diff_menu.pack(side=tk.LEFT, padx=5)
        diff_menu.bind('<<ComboboxSelected>>', self.on_difficulty_change)
        
        # New Game button
        new_game_btn = tk.Button(top_frame, text="New Game (F2)", 
                                command=self.new_game, bg='#4CAF50',
                                fg='white', font=('Arial', 10, 'bold'),
                                padx=15, pady=5, relief=tk.RAISED, bd=2)
        new_game_btn.pack(side=tk.LEFT, padx=10)
        
        # Stats button
        stats_btn = tk.Button(top_frame, text="Statistics", 
                             command=self.show_stats, bg='#2196F3',
                             fg='white', font=('Arial', 10, 'bold'),
                             padx=15, pady=5, relief=tk.RAISED, bd=2)
        stats_btn.pack(side=tk.LEFT, padx=10)
        
        # AI Solver button
        self.ai_btn = tk.Button(top_frame, text="AI Solver", 
                               command=self.toggle_ai, bg='#FF9800',
                               fg='white', font=('Arial', 10, 'bold'),
                               padx=15, pady=5, relief=tk.RAISED, bd=2)
        self.ai_btn.pack(side=tk.LEFT, padx=10)
        self.ai_active = False
        
        # Info panel
        info_frame = tk.Frame(self.root, bg=self.COLORS['bg'], pady=5)
        info_frame.pack(fill=tk.X)
        
        # Mine counter
        self.mine_counter_label = tk.Label(info_frame, text="Mines: 000", 
                                           bg=self.COLORS['bg'], fg='white',
                                           font=('Arial', 12, 'bold'))
        self.mine_counter_label.pack(side=tk.LEFT, padx=20)
        
        # Timer
        self.timer_label = tk.Label(info_frame, text="Time: 000", 
                                    bg=self.COLORS['bg'], fg='white',
                                    font=('Arial', 12, 'bold'))
        self.timer_label.pack(side=tk.RIGHT, padx=20)
        
        # Info label
        self.info_label = tk.Label(self.root, text="Click a cell to start!", 
                                   bg=self.COLORS['bg'], fg='yellow',
                                   font=('Arial', 9))
        self.info_label.pack(pady=5)
        
        # Game board frame
        self.board_frame = tk.Frame(self.root, bg=self.COLORS['bg'])
        self.board_frame.pack(pady=10)
        
        # Keyboard shortcuts
        self.root.bind('<F2>', lambda e: self.new_game())
        self.root.bind('<Control-r>', lambda e: self.new_game())
        
    def on_difficulty_change(self, event=None):
        """Handle difficulty change."""
        self.current_difficulty = self.diff_var.get()
        self.new_game()
    
    def new_game(self):
        """Start a new game."""
        if self.ai_active:
            self.toggle_ai()  # Stop AI if running
        
        self.timer_running = False
        self.start_time = None
        
        # Get difficulty settings
        if self.current_difficulty == 'Custom':
            self.show_custom_dialog()
            return
        
        width, height, num_mines = self.DIFFICULTIES[self.current_difficulty]
        
        # Create new game
        self.game = Minesweeper(width, height, num_mines)
        self.ai = MinesweeperAI(self.game, self)
        
        # Clear old board
        for widget in self.board_frame.winfo_children():
            widget.destroy()
        self.cells = []
        
        # Create board
        self.create_board()
        self.update_display()
        self.update_info("New game started! Click a cell to begin.")
        
    def show_custom_dialog(self):
        """Show custom difficulty dialog."""
        dialog = tk.Toplevel(self.root)
        dialog.title("Custom Difficulty")
        dialog.configure(bg=self.COLORS['bg'])
        dialog.transient(self.root)
        dialog.grab_set()
        
        # Center dialog
        dialog.geometry("300x200+%d+%d" % (
            self.root.winfo_rootx() + 250,
            self.root.winfo_rooty() + 200
        ))
        
        tk.Label(dialog, text="Width:", bg=self.COLORS['bg'], fg='white').grid(row=0, column=0, padx=10, pady=10)
        width_var = tk.StringVar(value="16")
        tk.Entry(dialog, textvariable=width_var, width=10).grid(row=0, column=1, padx=10, pady=10)
        
        tk.Label(dialog, text="Height:", bg=self.COLORS['bg'], fg='white').grid(row=1, column=0, padx=10, pady=10)
        height_var = tk.StringVar(value="16")
        tk.Entry(dialog, textvariable=height_var, width=10).grid(row=1, column=1, padx=10, pady=10)
        
        tk.Label(dialog, text="Mines:", bg=self.COLORS['bg'], fg='white').grid(row=2, column=0, padx=10, pady=10)
        mines_var = tk.StringVar(value="40")
        tk.Entry(dialog, textvariable=mines_var, width=10).grid(row=2, column=1, padx=10, pady=10)
        
        def start_custom():
            try:
                w, h, m = int(width_var.get()), int(height_var.get()), int(mines_var.get())
                if 5 <= w <= 50 and 5 <= h <= 30 and 1 <= m < w * h:
                    self.DIFFICULTIES['Custom'] = (w, h, m)
                    dialog.destroy()
                    self.new_game()
                else:
                    messagebox.showerror("Error", "Invalid values! Width: 5-50, Height: 5-30, Mines: 1 to (width*height-1)")
            except ValueError:
                messagebox.showerror("Error", "Please enter valid numbers!")
        
        tk.Button(dialog, text="Start", command=start_custom, 
                 bg='#4CAF50', fg='white', padx=20).grid(row=3, column=0, columnspan=2, pady=20)
    
    def create_board(self):
        """Create the game board UI."""
        cell_size = 25 if self.game.width <= 16 else 20 if self.game.width <= 30 else 15
        
        for y in range(self.game.height):
            row = []
            for x in range(self.game.width):
                btn = tk.Button(
                    self.board_frame,
                    width=2,
                    height=1,
                    bg=self.COLORS['cell_hidden'],
                    relief=tk.RAISED,
                    bd=2,
                    font=('Arial', 9, 'bold'),
                    command=lambda cx=x, cy=y: self.on_cell_click(cx, cy),
                    cursor='hand2'
                )
                btn.grid(row=y, column=x, padx=1, pady=1)
                
                # Right-click binding
                btn.bind('<Button-3>', lambda e, cx=x, cy=y: self.on_cell_right_click(cx, cy))
                
                # Middle-click for chording
                btn.bind('<Button-2>', lambda e, cx=x, cy=y: self.on_cell_middle_click(cx, cy))
                
                row.append(btn)
            self.cells.append(row)
    
    def on_cell_click(self, x: int, y: int):
        """Handle left-click on a cell."""
        if self.game.game_over:
            return
        
        if not self.timer_running and not self.game.revealed[y][x]:
            self.start_timer()
        
        success = self.game.reveal(x, y)
        self.update_display()
        
        if not success:
            self.game_over(lost=True)
        elif self.game.game_won:
            self.game_over(lost=False)
        else:
            self.update_info(f"Revealed ({x}, {y})")
    
    def on_cell_right_click(self, x: int, y: int):
        """Handle right-click to toggle flag."""
        if self.game.game_over or self.game.revealed[y][x]:
            return
        
        self.game.toggle_flag(x, y)
        self.update_display()
        self.update_info(f"Flagged ({x}, {y})" if self.game.flagged[y][x] else f"Unflagged ({x}, {y})")
    
    def on_cell_middle_click(self, x: int, y: int):
        """Handle middle-click for chording."""
        if self.game.game_over or not self.game.revealed[y][x]:
            return
        
        self.game.chord(x, y)
        self.update_display()
        
        if self.game.game_won:
            self.game_over(lost=False)
    
    def update_display(self):
        """Update the visual display of the board."""
        if not self.game:
            return
        
        for y in range(self.game.height):
            for x in range(self.game.width):
                btn = self.cells[y][x]
                
                if self.game.flagged[y][x]:
                    btn.config(text='🚩', bg='#ffcccc', state=tk.NORMAL)
                elif self.game.revealed[y][x]:
                    btn.config(state=tk.DISABLED, relief=tk.SUNKEN)
                    if self.game.board[y][x] == -1:
                        btn.config(text='💣', bg='#ff0000', fg='white')
                    elif self.game.board[y][x] == 0:
                        btn.config(text='', bg=self.COLORS['cell_revealed'])
                    else:
                        num = self.game.board[y][x]
                        color = self.COLORS['numbers'][num] if num < len(self.COLORS['numbers']) else '#000000'
                        btn.config(text=str(num), bg=self.COLORS['cell_revealed'], fg=color)
                else:
                    btn.config(text='', bg=self.COLORS['cell_hidden'], state=tk.NORMAL)
        
        # Update mine counter
        remaining = self.game.num_mines - self.game.get_flag_count()
        self.mine_counter_label.config(text=f"Mines: {remaining:03d}")
    
    def start_timer(self):
        """Start the game timer."""
        self.start_time = time.time()
        self.timer_running = True
        self.update_timer()
    
    def update_timer(self):
        """Update the timer display."""
        if self.timer_running and not self.game.game_over:
            elapsed = int(time.time() - self.start_time)
            self.timer_label.config(text=f"Time: {elapsed:03d}")
            self.root.after(1000, self.update_timer)
    
    def game_over(self, lost: bool):
        """Handle game over."""
        self.timer_running = False
        
        if lost:
            # Reveal all mines
            for y in range(self.game.height):
                for x in range(self.game.width):
                    if self.game.board[y][x] == -1:
                        self.game.revealed[y][x] = True
            
            self.update_display()
            elapsed = int(time.time() - self.start_time) if self.start_time else 0
            
            self.update_info("💥 Game Over! You hit a mine!")
            self.stats.record_game(False, elapsed, self.current_difficulty.lower())
            
            messagebox.showinfo("Game Over", f"You hit a mine!\nTime: {elapsed} seconds")
        else:
            elapsed = int(time.time() - self.start_time) if self.start_time else 0
            best_time = self.stats.get_best_time(self.current_difficulty.lower())
            
            self.update_info("🎉 Congratulations! You won!")
            self.stats.record_game(True, elapsed, self.current_difficulty.lower())
            
            msg = f"Congratulations! You cleared all mines!\nTime: {elapsed} seconds"
            if best_time and elapsed == best_time:
                msg += f"\n🎯 New Best Time for {self.current_difficulty}!"
            elif best_time:
                msg += f"\nBest Time: {self.stats._format_time(best_time)}"
            
            messagebox.showinfo("You Win!", msg)
    
    def toggle_ai(self):
        """Toggle AI solver on/off."""
        if self.ai_active:
            self.ai_active = False
            self.ai_btn.config(text="AI Solver", bg='#FF9800')
            self.update_info("AI Solver stopped")
        else:
            if self.game.game_over:
                self.new_game()
            self.ai_active = True
            self.ai_btn.config(text="Stop AI", bg='#f44336')
            self.update_info("AI Solver started")
            self.run_ai()
    
    def run_ai(self):
        """Run AI solver moves."""
        if not self.ai_active or self.game.game_over:
            return
        
        if not self.timer_running and not self.game.revealed[self.game.height//2][self.game.width//2]:
            self.start_timer()
        
        moved = self.ai.make_move()
        
        if moved:
            self.update_display()
            
            if self.game.game_won:
                self.game_over(lost=False)
                self.ai_active = False
                self.ai_btn.config(text="AI Solver", bg='#FF9800')
            elif not self.game.game_over:
                self.root.after(200, self.run_ai)  # Continue AI moves
            else:
                self.game_over(lost=True)
                self.ai_active = False
                self.ai_btn.config(text="AI Solver", bg='#FF9800')
    
    def update_info(self, message: str):
        """Update the info label."""
        self.info_label.config(text=message)
    
    def show_stats(self):
        """Show statistics dialog."""
        stats_window = tk.Toplevel(self.root)
        stats_window.title("Game Statistics")
        stats_window.configure(bg=self.COLORS['bg'])
        stats_window.transient(self.root)
        
        # Center window
        stats_window.geometry("400x400+%d+%d" % (
            self.root.winfo_rootx() + 200,
            self.root.winfo_rooty() + 100
        ))
        
        stats_text = tk.Text(stats_window, bg='#1e1e1e', fg='white', 
                            font=('Consolas', 10), wrap=tk.WORD, padx=10, pady=10)
        stats_text.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        stats_text.insert('1.0', self.stats.get_summary())
        stats_text.config(state=tk.DISABLED)
        
        # Reset button
        def reset_stats():
            if messagebox.askyesno("Reset Statistics", "Are you sure you want to reset all statistics?"):
                self.stats.reset_stats()
                stats_text.config(state=tk.NORMAL)
                stats_text.delete('1.0', tk.END)
                stats_text.insert('1.0', self.stats.get_summary())
                stats_text.config(state=tk.DISABLED)
        
        btn_frame = tk.Frame(stats_window, bg=self.COLORS['bg'])
        btn_frame.pack(pady=10)
        tk.Button(btn_frame, text="Reset Statistics", command=reset_stats,
                 bg='#f44336', fg='white', padx=15).pack(side=tk.LEFT, padx=5)
        tk.Button(btn_frame, text="Close", command=stats_window.destroy,
                 bg='#4CAF50', fg='white', padx=15).pack(side=tk.LEFT, padx=5)
    
    def run(self):
        """Start the GUI main loop."""
        self.root.mainloop()


if __name__ == "__main__":
    app = MinesweeperGUI()
    app.run()

