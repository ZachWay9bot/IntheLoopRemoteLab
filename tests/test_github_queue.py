import json
import tempfile
import unittest
from pathlib import Path

from remotelab.adapters.simulator import SimulatorAdapter
from remotelab.core.engine import Engine
from remotelab.core.state import QueueStateStore, fresh_state
from remotelab.runner import IssueQueueRunner
from remotelab.transports.github_issue import (
    COMMAND_PREFIX,
    QueueBinding,
    format_result,
    parse_command,
)


class FakeClient:
    def __init__(self, comments):
        self.binding = QueueBinding(
            repo="owner/private-queue",
            issue=1,
            operator="operator",
        )
        self._comments = list(comments)
        self.posted = []

    def validate(self):
        return "operator"

    def comments(self, since=None):
        return list(self._comments)

    def post_result(self, result):
        self.posted.append(result)
        return {"id": len(self.posted)}


def command_comment(cid, job_id="j1", operation="identify"):
    return {
        "id": cid,
        "created_at": f"2026-10-18T20:00:{cid:02d}Z",
        "user": {"login": "operator"},
        "body": COMMAND_PREFIX
        + json.dumps(
            {
                "id": job_id,
                "device": "simulator",
                "operation": operation,
                "args": {},
            }
        ),
    }


class QueueTests(unittest.TestCase):
    def test_parse_strict_command(self):
        cmd = parse_command(command_comment(1), "operator")
        self.assertEqual(cmd["id"], "j1")
        self.assertEqual(cmd["device"], "simulator")

    def test_wrong_author_ignored(self):
        item = command_comment(1)
        item["user"]["login"] = "someone-else"
        self.assertIsNone(parse_command(item, "operator"))

    def test_result_prefix(self):
        body = format_result({"type": "result", "id": "x", "ok": True})
        self.assertTrue(body.startswith("REMOTELAB-RESULT/1\n"))

    def test_runner_executes_once_and_posts(self):
        with tempfile.TemporaryDirectory() as tmp:
            store = QueueStateStore(Path(tmp) / "state.json")
            store.save(fresh_state("owner/private-queue", 1))
            client = FakeClient([command_comment(1)])
            engine = Engine(
                [SimulatorAdapter()],
                Path(tmp) / "audit.jsonl",
            )
            runner = IssueQueueRunner(engine, client, store)

            self.assertEqual(runner.process_once(), 1)
            self.assertEqual(len(client.posted), 1)
            self.assertTrue(client.posted[0]["ok"])

            self.assertEqual(runner.process_once(), 0)
            self.assertEqual(len(client.posted), 1)

    def test_inflight_is_not_replayed_after_restart(self):
        with tempfile.TemporaryDirectory() as tmp:
            path = Path(tmp) / "state.json"
            store = QueueStateStore(path)
            state = fresh_state("owner/private-queue", 1)
            state["in_flight"] = {
                "comment_id": 5,
                "job": {
                    "id": "maybe-ran",
                    "device": "simulator",
                    "operation": "identify",
                    "args": {},
                },
            }
            store.save(state)

            client = FakeClient([])
            engine = Engine(
                [SimulatorAdapter()],
                Path(tmp) / "audit.jsonl",
            )
            runner = IssueQueueRunner(engine, client, store)
            runner.recover_uncertain_job()
            runner.flush_pending_results()

            self.assertEqual(len(client.posted), 1)
            self.assertEqual(
                client.posted[0]["status"],
                "execution-uncertain",
            )
            self.assertIn("maybe-ran", runner.state["completed"])
            self.assertIsNone(runner.state["in_flight"])


if __name__ == "__main__":
    unittest.main()
