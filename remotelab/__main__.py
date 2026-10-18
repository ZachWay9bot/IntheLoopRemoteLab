from pathlib import Path

from .core.engine import Engine
from .adapters.simulator import SimulatorAdapter


def main():
    engine = Engine(
        adapters=[SimulatorAdapter()],
        audit_file=Path("runtime") / "audit.jsonl",
    )
    print("RemoteLab", __import__("remotelab").__version__)
    print(engine.execute({"device": "simulator", "operation": "identify"}))
    print(engine.execute({"device": "simulator", "operation": "diagnose"}))


if __name__ == "__main__":
    main()
