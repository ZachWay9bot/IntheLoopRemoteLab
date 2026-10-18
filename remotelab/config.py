from __future__ import annotations

import json
from pathlib import Path


DEFAULT_ADAPTERS = [
    {
        "module": "remotelab.adapters.simulator",
        "class": "SimulatorAdapter",
        "enabled": True,
        "args": {},
    }
]


def load_config(path: str | Path) -> dict:
    path = Path(path)
    with path.open("r", encoding="utf-8") as handle:
        cfg = json.load(handle)

    if not isinstance(cfg, dict):
        raise ValueError("config must be an object")

    queue = cfg.get("queue")
    if not isinstance(queue, dict):
        raise ValueError("queue config missing")

    required = {"repo", "issue", "operator"}
    missing = required - set(queue)
    if missing:
        raise ValueError(f"queue config missing: {sorted(missing)}")

    if not isinstance(queue["repo"], str) or "/" not in queue["repo"]:
        raise ValueError("queue.repo must be owner/name")
    if not isinstance(queue["issue"], int) or queue["issue"] < 1:
        raise ValueError("queue.issue must be >= 1")
    if not isinstance(queue["operator"], str) or not queue["operator"]:
        raise ValueError("queue.operator missing")

    cfg.setdefault("poll_seconds", 8)
    cfg.setdefault("state_file", "runtime/queue_state.json")
    cfg.setdefault("audit_file", "runtime/audit.jsonl")
    cfg.setdefault("adapters", list(DEFAULT_ADAPTERS))

    if not isinstance(cfg["adapters"], list):
        raise ValueError("adapters must be a list")

    return cfg
