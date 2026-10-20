"""Run three synthetic RemoteLab firmware fixtures without a controller.

Does NOT build or execute DeltaESC, EBiCS or SmartESC firmware.
"""
from __future__ import annotations

import json
from pathlib import Path

from remotelab.adapters.loader import load_adapters
from remotelab.core.engine import Engine


def main() -> int:
    root = Path(__file__).resolve().parents[1]
    cfg = json.loads(
        (root / "examples" / "offline_firmware_adapters.example.json")
        .read_text(encoding="utf-8")
    )
    engine = Engine(
        load_adapters(cfg["adapters"]),
        root / "runtime" / "offline_firmware_audit.jsonl",
    )
    print("IntheLoopRemoteLab - OFFLINE FIXTURE SMOKE")
    print("SYNTHETIC: no physical hardware, no firmware execution, no motor tests")
    count = 0
    for name in ("offline_deltaesc", "offline_ebics", "offline_smartesc"):
        for operation in ("identify", "diagnose"):
            result = engine.execute({
                "device": name,
                "operation": operation,
                "job_id": f"offline-{name}-{operation}",
            })
            if not result["ok"] or not result["result"].get("simulated"):
                raise RuntimeError(f"{name}:{operation}: invalid fixture result {result}")
            print(f"{name} / {operation}: synthetic PASS")
            count += 1
    print(f"Fixture dispatch checks: {count}/6 PASS")
    print("Hardware and firmware readiness: NOT TESTED")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
