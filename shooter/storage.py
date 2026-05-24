from __future__ import annotations

import json
from pathlib import Path


DEFAULT_DATA = {"players": {}}


class PlayerStorage:
    def __init__(self, data_file: str | Path) -> None:
        self.data_file = Path(data_file)

    def load(self) -> dict:
        if not self.data_file.exists():
            return DEFAULT_DATA.copy()

        try:
            with self.data_file.open("r", encoding="utf-8") as handle:
                data = json.load(handle)
        except (json.JSONDecodeError, OSError):
            return DEFAULT_DATA.copy()

        players = data.get("players")
        if not isinstance(players, dict):
            return DEFAULT_DATA.copy()

        return {"players": players}

    def save(self, data: dict) -> None:
        self.data_file.parent.mkdir(parents=True, exist_ok=True)
        with self.data_file.open("w", encoding="utf-8") as handle:
            json.dump(data, handle, indent=2)

    def ensure_player(self, username: str) -> dict:
        data = self.load()
        players = data["players"]
        record = players.setdefault(
            username,
            {
                "best_score": 0,
                "games_played": 0,
                "last_score": 0,
            },
        )
        self.save(data)
        return record

    def update_score(self, username: str, score: int) -> dict:
        data = self.load()
        players = data["players"]
        record = players.setdefault(
            username,
            {
                "best_score": 0,
                "games_played": 0,
                "last_score": 0,
            },
        )
        record["games_played"] += 1
        record["last_score"] = score
        record["best_score"] = max(record["best_score"], score)
        self.save(data)
        return record

    def leaderboard(self) -> list[tuple[str, dict]]:
        data = self.load()
        players = data["players"]
        return sorted(
            players.items(),
            key=lambda item: (item[1].get("best_score", 0), item[1].get("last_score", 0)),
            reverse=True,
        )
