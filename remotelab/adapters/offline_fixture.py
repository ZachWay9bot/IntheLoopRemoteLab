"""Offline-only fixture adapter for exercising the RemoteLab job path.

This module does not import firmware, open ports, flash images or control hardware.
Values are intentionally synthetic and MUST NOT be treated as hardware evidence.
"""

from __future__ import annotations

from copy import deepcopy

from .base import DeviceAdapter


class OfflineFirmwareFixtureAdapter(DeviceAdapter):
    def __init__(
        self,
        *,
        name: str,
        project: str,
        firmware_reference: str,
        diagnostic_fixture: dict | None = None,
    ):
        if not isinstance(name, str) or not name.startswith("offline_"):
            raise ValueError("offline fixture name must begin with offline_")
        if not isinstance(project, str) or not project.strip():
            raise ValueError("project must be provided")
        if not isinstance(firmware_reference, str) or not firmware_reference.strip():
            raise ValueError("firmware_reference must be provided")
        if diagnostic_fixture is not None and not isinstance(diagnostic_fixture, dict):
            raise TypeError("diagnostic_fixture must be an object")
        self.name = name
        self.project = project
        self.firmware_reference = firmware_reference
        self.fixture = deepcopy(diagnostic_fixture or {})

    def identify(self) -> dict:
        return {
            "adapter": self.name,
            "project": self.project,
            "firmware_reference": self.firmware_reference,
            "simulated": True,
            "hardware_connected": False,
            "firmware_loaded": False,
            "write_capable": False,
            "evidence": "synthetic-fixture-only",
        }

    def diagnose(self) -> dict:
        return {
            "adapter": self.name,
            "project": self.project,
            "simulated": True,
            "hardware_connected": False,
            "firmware_executed": False,
            "write_capable": False,
            "evidence": "synthetic-fixture-only",
            "fixture": deepcopy(self.fixture),
        }
