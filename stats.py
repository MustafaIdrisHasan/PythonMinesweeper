import json
import os
from typing import Dict, Optional
from datetime import datetime


class GameStats:
    """Track and persist game statistics."""
    
    STATS_FILE = "minesweeper_stats.json"
    
    def __init__(self):
        self.stats = self.load_stats()
    
    def load_stats(self) -> Dict:
        """Load statistics from file."""
        if os.path.exists(self.STATS_FILE):
            try:
                with open(self.STATS_FILE, 'r') as f:
                    return json.load(f)
            except (json.JSONDecodeError, IOError):
                pass
        
        # Default stats structure
        return {
            "games_played": 0,
            "games_won": 0,
            "games_lost": 0,
            "best_times": {
                "beginner": None,
                "intermediate": None,
                "expert": None,
                "custom": None
            },
            "total_time": 0,
            "win_streak": 0,
            "best_win_streak": 0
        }
    
    def save_stats(self):
        """Save statistics to file."""
        try:
            with open(self.STATS_FILE, 'w') as f:
                json.dump(self.stats, f, indent=2)
        except IOError:
            pass
    
    def record_game(self, won: bool, time_seconds: float, difficulty: str = "custom"):
        """Record a completed game."""
        self.stats["games_played"] += 1
        
        if won:
            self.stats["games_won"] += 1
            self.stats["win_streak"] += 1
            self.stats["best_win_streak"] = max(
                self.stats["best_win_streak"], 
                self.stats["win_streak"]
            )
            
            # Update best time for difficulty
            best_time = self.stats["best_times"].get(difficulty)
            if best_time is None or time_seconds < best_time:
                self.stats["best_times"][difficulty] = time_seconds
        else:
            self.stats["games_lost"] += 1
            self.stats["win_streak"] = 0
        
        self.stats["total_time"] += time_seconds
        self.save_stats()
    
    def get_win_rate(self) -> float:
        """Calculate win rate as percentage."""
        if self.stats["games_played"] == 0:
            return 0.0
        return (self.stats["games_won"] / self.stats["games_played"]) * 100
    
    def get_best_time(self, difficulty: str) -> Optional[float]:
        """Get best time for a difficulty level."""
        return self.stats["best_times"].get(difficulty)
    
    def reset_stats(self):
        """Reset all statistics."""
        self.stats = {
            "games_played": 0,
            "games_won": 0,
            "games_lost": 0,
            "best_times": {
                "beginner": None,
                "intermediate": None,
                "expert": None,
                "custom": None
            },
            "total_time": 0,
            "win_streak": 0,
            "best_win_streak": 0
        }
        self.save_stats()
    
    def get_summary(self) -> str:
        """Get a formatted summary of statistics."""
        win_rate = self.get_win_rate()
        return f"""Statistics Summary:
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
Games Played: {self.stats['games_played']}
Games Won: {self.stats['games_won']}
Games Lost: {self.stats['games_lost']}
Win Rate: {win_rate:.1f}%
Current Win Streak: {self.stats['win_streak']}
Best Win Streak: {self.stats['best_win_streak']}

Best Times:
  Beginner: {self._format_time(self.stats['best_times']['beginner'])}
  Intermediate: {self._format_time(self.stats['best_times']['intermediate'])}
  Expert: {self._format_time(self.stats['best_times']['expert'])}
  Custom: {self._format_time(self.stats['best_times']['custom'])}
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"""
    
    @staticmethod
    def _format_time(seconds: Optional[float]) -> str:
        """Format time in seconds to MM:SS format."""
        if seconds is None:
            return "N/A"
        mins = int(seconds // 60)
        secs = int(seconds % 60)
        return f"{mins:02d}:{secs:02d}"

