from __future__ import annotations

import json
import os
import tempfile
from pathlib import Path


class QueueStateStore:
    def __init__(self, path: str | Path):
        self.path = Path(path)

    def load(self) -> dict:
        if not self.path.exists():
            return {}
        with self.path.open("r", encoding="utf-8") as handle:
            data = json.load(handle)
        if not isinstance(data, dict):
            raise RuntimeError("queue state is not an object")
        return data

    def save(self, state: dict) -> None:
        self.path.parent.mkdir(parents=True, exist_ok=True)

        fd, tmp_name = tempfile.mkstemp(
            prefix=self.path.name + ".",
            suffix=".tmp",
            dir=str(self.path.parent),
        )
        try:
            with os.fdopen(fd, "w", encoding="utf-8") as handle:
                json.dump(
                    state,
                    handle,
                    ensure_ascii=False,
                    sort_keys=True,
                    indent=2,
                )
                handle.write("\n")
                handle.flush()
                os.fsync(handle.fileno())
            os.replace(tmp_name, self.path)
        finally:
            if os.path.exists(tmp_name):
                os.unlink(tmp_name)


def fresh_state(repo: str, issue: int) -> dict:
    return {
        "repo": repo,
        "issue": issue,
        "last_seen_id": 0,
        "last_created_at": None,
        "completed": [],
        "pending_results": [],
        "in_flight": None,
    }


def normalize_state(state: dict, repo: str, issue: int) -> dict:
    if state.get("repo") != repo or state.get("issue") != issue:
        return fresh_state(repo, issue)

    state.setdefault("last_seen_id", 0)
    state.setdefault("last_created_at", None)
    state.setdefault("completed", [])
    state.setdefault("pending_results", [])
    state.setdefault("in_flight", None)
    return state
