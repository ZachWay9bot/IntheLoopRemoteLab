from __future__ import annotations

import argparse

from remotelab import __version__
from remotelab.adapters.loader import load_adapters
from remotelab.adapters.simulator import SimulatorAdapter
from remotelab.auth import load_github_token
from remotelab.config import load_config
from remotelab.core.engine import Engine
from remotelab.core.state import QueueStateStore
from remotelab.runner import IssueQueueRunner
from remotelab.transports.github_issue import GitHubIssueClient, QueueBinding


def build_runner(cfg: dict) -> IssueQueueRunner:
    token = load_github_token()
    queue = cfg["queue"]
    binding = QueueBinding(
        repo=queue["repo"],
        issue=queue["issue"],
        operator=queue["operator"],
    )
    client = GitHubIssueClient(
        token,
        binding,
        user_agent=f"RemoteLab/{__version__}",
    )
    engine = Engine(
        load_adapters(cfg["adapters"]),
        cfg["audit_file"],
    )
    return IssueQueueRunner(
        engine,
        client,
        QueueStateStore(cfg["state_file"]),
        poll_seconds=cfg["poll_seconds"],
    )


def main(argv=None) -> int:
    parser = argparse.ArgumentParser(prog="remotelab")
    parser.add_argument(
        "action",
        nargs="?",
        choices=["simulator", "once", "run"],
        default="simulator",
    )
    parser.add_argument(
        "--config",
        default="remotelab.json",
        help="RemoteLab JSON config",
    )
    args = parser.parse_args(argv)

    if args.action == "simulator":
        engine = Engine([SimulatorAdapter()], "runtime/audit.jsonl")
        print("RemoteLab", __version__)
        print(
            engine.execute(
                {"device": "simulator", "operation": "identify"}
            )
        )
        print(
            engine.execute(
                {"device": "simulator", "operation": "diagnose"}
            )
        )
        return 0

    cfg = load_config(args.config)
    runner = build_runner(cfg)
    runner.prepare()

    if args.action == "once":
        count = runner.process_once()
        print(f"RemoteLab {__version__}: processed={count}")
        return 0

    runner.run(prepared=True)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
