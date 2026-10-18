from __future__ import annotations

import time

from remotelab.core.engine import Engine
from remotelab.core.state import QueueStateStore, fresh_state, normalize_state
from remotelab.transports.github_issue import GitHubIssueClient, parse_command


class IssueQueueRunner:
    def __init__(
        self,
        engine: Engine,
        client: GitHubIssueClient,
        state_store: QueueStateStore,
        poll_seconds: int = 8,
    ):
        self.engine = engine
        self.client = client
        self.state_store = state_store
        self.poll_seconds = max(1, int(poll_seconds))
        self.state = normalize_state(
            self.state_store.load(),
            self.client.binding.repo,
            self.client.binding.issue,
        )

    def bind_without_replaying_history(self) -> None:
        if self.state.get("last_seen_id", 0):
            return

        existing = list(self.client.comments())
        if existing:
            self.state["last_seen_id"] = max(
                int(entry["id"]) for entry in existing
            )
            created = [
                entry.get("created_at")
                for entry in existing
                if entry.get("created_at")
            ]
            if created:
                self.state["last_created_at"] = max(created)

        self.state_store.save(self.state)

    def recover_uncertain_job(self) -> None:
        inflight = self.state.get("in_flight")
        if not inflight:
            return

        job = inflight["job"]
        result = {
            "type": "result",
            "id": job["id"],
            "device": job["device"],
            "operation": job["operation"],
            "ok": False,
            "error": (
                "agent restarted while this job was in flight; "
                "it was not replayed automatically"
            ),
            "status": "execution-uncertain",
        }

        completed = self.state.get("completed", [])
        if job["id"] not in completed:
            self.state["completed"] = (completed + [job["id"]])[-1000:]

        self.state.setdefault("pending_results", []).append(result)
        self.state["in_flight"] = None
        self.state_store.save(self.state)

    def flush_pending_results(self) -> None:
        pending = self.state.setdefault("pending_results", [])
        while pending:
            self.client.post_result(pending[0])
            pending.pop(0)
            self.state_store.save(self.state)

    def _advance_cursor(self, entry: dict) -> None:
        self.state["last_seen_id"] = int(entry["id"])
        if entry.get("created_at"):
            self.state["last_created_at"] = entry["created_at"]
        self.state_store.save(self.state)

    def process_once(self) -> int:
        processed = 0
        self.flush_pending_results()

        for entry in self.client.comments(self.state.get("last_created_at")):
            comment_id = int(entry["id"])
            if comment_id <= int(self.state.get("last_seen_id", 0)):
                continue

            command = parse_command(
                entry,
                self.client.binding.operator,
            )

            # Cursor is persisted before any device operation. This makes the
            # queue at-most-once for hardware actions.
            self._advance_cursor(entry)

            if not command:
                continue
            if command["id"] in self.state.get("completed", []):
                continue

            self.state["in_flight"] = {
                "comment_id": comment_id,
                "job": command,
            }
            self.state_store.save(self.state)

            started = time.monotonic()
            try:
                result = self.engine.execute(
                    {
                        "job_id": command["id"],
                        "device": command["device"],
                        "operation": command["operation"],
                        "args": command["args"],
                    }
                )
                answer = {
                    "type": "result",
                    "id": command["id"],
                    "device": command["device"],
                    "operation": command["operation"],
                    "ok": bool(result.get("ok")),
                    "duration_s": round(time.monotonic() - started, 3),
                }
                if result.get("ok"):
                    answer["data"] = result.get("result")
                else:
                    answer["error"] = result.get("error", "unknown error")
            except Exception as exc:
                answer = {
                    "type": "result",
                    "id": command["id"],
                    "device": command["device"],
                    "operation": command["operation"],
                    "ok": False,
                    "duration_s": round(time.monotonic() - started, 3),
                    "error": type(exc).__name__ + ": " + str(exc),
                }

            self.state["completed"] = (
                self.state.get("completed", []) + [command["id"]]
            )[-1000:]
            self.state.setdefault("pending_results", []).append(answer)
            self.state["in_flight"] = None
            self.state_store.save(self.state)

            self.flush_pending_results()
            processed += 1

        return processed

    def run(self) -> None:
        self.client.validate()
        self.bind_without_replaying_history()
        self.recover_uncertain_job()
        self.flush_pending_results()

        while True:
            try:
                self.process_once()
                time.sleep(self.poll_seconds)
            except KeyboardInterrupt:
                return
            except Exception:
                time.sleep(max(10, self.poll_seconds))
