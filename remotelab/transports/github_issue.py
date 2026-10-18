from __future__ import annotations

import datetime as dt
import json
import re
import urllib.error
import urllib.parse
import urllib.request
from dataclasses import dataclass
from typing import Iterable

API_BASE = "https://api.github.com"
COMMAND_PREFIX = "REMOTELAB-CMD/1\n"
RESULT_PREFIX = "REMOTELAB-RESULT/1\n"
MAX_COMMENT_BYTES = 56_000
JOB_ID_RE = re.compile(r"^[A-Za-z0-9][A-Za-z0-9._:-]{0,127}$")


def parse_command(entry: dict, operator: str) -> dict | None:
    if str(entry.get("user", {}).get("login", "")).lower() != operator.lower():
        return None

    body = entry.get("body", "")
    if not isinstance(body, str) or not body.startswith(COMMAND_PREFIX):
        return None

    try:
        obj = json.loads(body[len(COMMAND_PREFIX):])
    except Exception:
        return None

    if not isinstance(obj, dict):
        return None
    if set(obj) != {"id", "device", "operation", "args"}:
        return None
    if not isinstance(obj["id"], str) or not JOB_ID_RE.fullmatch(obj["id"]):
        return None
    if not isinstance(obj["device"], str) or not obj["device"]:
        return None
    if not isinstance(obj["operation"], str) or not obj["operation"]:
        return None
    if not isinstance(obj["args"], dict):
        return None

    return obj


def format_result(obj: dict) -> str:
    body = RESULT_PREFIX + json.dumps(
        obj, ensure_ascii=False, separators=(",", ":"), sort_keys=True
    )
    if len(body.encode("utf-8")) <= MAX_COMMENT_BYTES:
        return body

    slim = {
        key: obj.get(key)
        for key in ("type", "id", "device", "operation", "ok", "duration_s", "error")
        if key in obj
    }
    error = str(slim.get("error") or "result too large")
    slim["error"] = error[:2000] + " [full result stored locally]"
    return RESULT_PREFIX + json.dumps(
        slim, ensure_ascii=False, separators=(",", ":"), sort_keys=True
    )


@dataclass(frozen=True)
class QueueBinding:
    repo: str
    issue: int
    operator: str


class GitHubIssueClient:
    def __init__(self, token: str, binding: QueueBinding, user_agent: str):
        self.token = token
        self.binding = binding
        self.user_agent = user_agent

    def api(self, method: str, path: str, obj=None):
        if not path.startswith("/") or path.startswith("//") or ".." in path:
            raise ValueError("unsafe GitHub API path")

        raw_body = None
        if obj is not None:
            raw_body = json.dumps(obj, ensure_ascii=False).encode("utf-8")

        request = urllib.request.Request(
            API_BASE + path,
            data=raw_body,
            method=method,
            headers={
                "Authorization": "Bearer " + self.token,
                "Accept": "application/vnd.github+json",
                "X-GitHub-Api-Version": "2022-11-28",
                "User-Agent": self.user_agent,
                "Content-Type": "application/json",
            },
        )

        try:
            with urllib.request.urlopen(request, timeout=20) as response:
                raw = response.read()
                return json.loads(raw) if raw else {}
        except urllib.error.HTTPError as exc:
            brief = exc.read(400).decode("utf-8", "replace")
            raise RuntimeError(
                f"GitHub API HTTP {exc.code}: {brief}"
            ) from exc

    def validate(self) -> str:
        me = self.api("GET", "/user")["login"]
        if me.lower() != self.binding.operator.lower():
            raise RuntimeError(
                f"GitHub token identity {me!r} != operator "
                f"{self.binding.operator!r}"
            )

        repo = self.api("GET", f"/repos/{self.binding.repo}")
        if not repo.get("private", False):
            raise RuntimeError("relay repository is not private")

        issue = self.api(
            "GET",
            f"/repos/{self.binding.repo}/issues/{self.binding.issue}",
        )
        if issue.get("state") != "open":
            raise RuntimeError("relay issue is not open")

        return me

    def comments(self, since: str | None = None) -> Iterable[dict]:
        page = 1
        since_arg = (
            "&since=" + urllib.parse.quote(since, safe="")
            if since
            else ""
        )

        while True:
            rows = self.api(
                "GET",
                f"/repos/{self.binding.repo}/issues/"
                f"{self.binding.issue}/comments"
                f"?per_page=100&page={page}{since_arg}",
            )
            if not isinstance(rows, list):
                raise RuntimeError("invalid comments response")

            yield from rows

            if len(rows) < 100:
                return

            page += 1
            if page > 50:
                raise RuntimeError("relay issue too large; rotate issue")

    def post_result(self, result: dict):
        body = format_result(result)
        return self.api(
            "POST",
            f"/repos/{self.binding.repo}/issues/"
            f"{self.binding.issue}/comments",
            {"body": body},
        )
