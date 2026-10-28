from __future__ import annotations

import datetime as _dt
import json
import threading
from pathlib import Path
from typing import Iterable

from remotelab.adapters.base import DeviceAdapter


READ_ONLY_OPERATIONS = frozenset({"identify", "diagnose", "measure", "capture_waveform"})


class Engine:
    """Hardware-independent dispatcher.

    v0.4.x deliberately exposes read-only device operations only. The job
    schema already carries an args object so later adapters do not need a
    transport-protocol change when bounded write operations are introduced.
    """

    def __init__(self, adapters: Iterable[DeviceAdapter], audit_file: Path | str):
        self.adapters = {adapter.name: adapter for adapter in adapters}
        self.audit_file = Path(audit_file)
        self._lock = threading.Lock()

    def execute(self, job: dict) -> dict:
        self._validate_job(job)
        device_name = job["device"]
        operation = job["operation"]
        args = job.get("args", {})

        adapter = self.adapters.get(device_name)
        if adapter is None:
            raise PermissionError(f"Unknown device adapter: {device_name}")
        if operation not in READ_ONLY_OPERATIONS:
            raise PermissionError(
                "v0.4 migration core permits read-only operations only"
            )

        handler = getattr(adapter, operation, None)
        if handler is None or not callable(handler):
            raise PermissionError(
                f"Adapter {device_name!r} does not implement {operation!r}"
            )

        with self._lock:
            try:
                result = handler(**args)
                self._audit(
                    job.get("job_id"),
                    device_name,
                    operation,
                    True,
                )
                return {"ok": True, "result": result}
            except Exception as exc:
                self._audit(
                    job.get("job_id"),
                    device_name,
                    operation,
                    False,
                    str(exc),
                )
                return {"ok": False, "error": str(exc)}

    @staticmethod
    def _validate_job(job: dict) -> None:
        if not isinstance(job, dict):
            raise ValueError("Job must be an object")

        allowed = {"device", "operation", "job_id", "args"}
        unknown = set(job) - allowed
        if unknown:
            raise ValueError(f"Unknown job fields: {sorted(unknown)}")

        if not isinstance(job.get("device"), str) or not job["device"]:
            raise ValueError("device is required")
        if not isinstance(job.get("operation"), str) or not job["operation"]:
            raise ValueError("operation is required")

        if "job_id" in job and not isinstance(job["job_id"], str):
            raise ValueError("job_id must be a string")

        args = job.get("args", {})
        if not isinstance(args, dict):
            raise ValueError("args must be an object")

    def _audit(
        self,
        job_id: str | None,
        device: str,
        operation: str,
        ok: bool,
        error: str | None = None,
    ) -> None:
        record = {
            "time": _dt.datetime.now(_dt.timezone.utc).isoformat(),
            "job_id": job_id,
            "device": device,
            "operation": operation,
            "ok": ok,
        }
        if error is not None:
            record["error"] = error

        self.audit_file.parent.mkdir(parents=True, exist_ok=True)
        with self.audit_file.open("a", encoding="utf-8") as handle:
            handle.write(json.dumps(record, sort_keys=True) + "\n")
