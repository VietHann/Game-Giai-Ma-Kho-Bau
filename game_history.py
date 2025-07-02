import json
import os
from datetime import datetime

class GameHistory:
    def __init__(self, history_file="game_history.json"):
        self.history_file = history_file
        self.history = self._load_history()

    def _load_history(self):
        if os.path.exists(self.history_file):
            try:
                with open(self.history_file, 'r', encoding='utf-8') as f:
                    return json.load(f)
            except:
                return []
        return []

    def _save_history(self):
        with open(self.history_file, 'w', encoding='utf-8') as f:
            json.dump(self.history, f, ensure_ascii=False, indent=2)

    def add_record(self, level_num, time_taken, attempts, score):
        record = {
            'timestamp': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
            'level': level_num,
            'time_taken': time_taken,
            'attempts': attempts,
            'score': score
        }
        self.history.append(record)
        self._save_history()

    def get_history(self):
        return self.history

    def clear_history(self):
        self.history = []
        self._save_history() 