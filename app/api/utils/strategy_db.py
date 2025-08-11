import sqlite3
from typing import List
import os

class StrategyDatabase:
    def __init__(self, db_path=None):
        if db_path is None:
            current_dir = os.getcwd()
            project_root = os.path.dirname(os.path.dirname(current_dir))
            db_path = os.path.abspath(os.path.join(project_root, 'app', 'strategies.db'))
        self.db_path = db_path
        self.conn = None
        self.has_strategies = False
        self.connect()

    def connect(self):
        try:
            self.conn = sqlite3.connect(self.db_path)
            cursor = self.conn.cursor()
            cursor.execute("SELECT name FROM sqlite_master WHERE type='table'")
            tables = [row[0] for row in cursor.fetchall()]
            if 'strategies' in tables:
                self.has_strategies = True
        except Exception as e:
            self.has_strategies = False

    def get_strategy_actions_by_game(self, strategy: str, game_number: int) -> List[int]:
        if not self.has_strategies:
            return []
        try:
            cursor = self.conn.cursor()
            cursor.execute("SELECT action_sequence FROM strategies WHERE strategy = ? AND game_number = ?", (strategy, game_number))
            row = cursor.fetchone()
            if row and row[0]:
                actions = [int(a.strip()) for a in row[0].split(',') if a.strip().isdigit()]
                return actions
            return []
        except Exception as e:
            return []

    def get_all_game_numbers(self, strategy: str) -> List[int]:
        if not self.has_strategies:
            return []
        try:
            cursor = self.conn.cursor()
            cursor.execute("SELECT DISTINCT game_number FROM strategies WHERE strategy = ? ORDER BY game_number", (strategy,))
            return [int(row[0]) for row in cursor.fetchall()]
        except Exception as e:
            return []
