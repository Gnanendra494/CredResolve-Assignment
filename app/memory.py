import json
from pathlib import Path
from typing import Dict, Any

MEM_PATH = Path("memory.json")

class Memory:
    def __init__(self, path: Path = MEM_PATH):
        self.path = path
        if not self.path.exists():
            self._write({"users": {}, "conversations": []})

    def _read(self) -> Dict[str, Any]:
        with open(self.path, "r", encoding="utf-8") as f:
            return json.load(f)

    def _write(self, data: Dict[str, Any]):
        with open(self.path, "w", encoding="utf-8") as f:
            json.dump(data, f, ensure_ascii=False, indent=2)

    def save_user(self, user_id: str, info: Dict[str, Any]):
        data = self._read()
        data["users"][user_id] = info
        self._write(data)

    def get_user(self, user_id: str) -> Dict[str, Any]:
        data = self._read()
        return data["users"].get(user_id, {})

    def add_conversation(self, turn: Dict[str, Any]):
        data = self._read()
        data["conversations"].append(turn)
        self._write(data)
