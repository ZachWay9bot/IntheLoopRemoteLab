from __future__ import annotations

import contextlib
import re
import time

from .base import DeviceAdapter
from . import xbot_protocol as proto


IDENTITY_RE = re.compile(r"^XBOTFO\d\dV[0-9A-F]{5}$")


class XbotReadOnlyAdapter(DeviceAdapter):
    """Passive XBOT adapter used during the v0.4 migration.

    The only UART commands emitted are the existing READ-map request (0x01)
    and diagnostic request (0xF0). No STOP, IAP, reset, motor-start, permit
    mutation, or flash command exists in this adapter.
    """

    name = "xbot_readonly"

    def __init__(self, port: str, serial_factory=None):
        self.port = port
        self._serial_factory = serial_factory

    @contextlib.contextmanager
    def _session(self):
        if self._serial_factory is not None:
            ser = self._serial_factory(self.port)
        else:
            try:
                import serial
            except ImportError as exc:
                raise RuntimeError(
                    "pyserial is required for the XBOT read-only adapter"
                ) from exc

            kwargs = {
                "port": self.port,
                "baudrate": 115200,
                "timeout": 0.05,
                "write_timeout": 1.0,
            }
            ser = serial.Serial(**kwargs)

        try:
            time.sleep(0.08)
            if hasattr(ser, "reset_input_buffer"):
                ser.reset_input_buffer()
            yield ser
        finally:
            close = getattr(ser, "close", None)
            if close is not None:
                close()

    def identify(self) -> dict:
        with self._session() as ser:
            name, drv = proto.read_identity(ser)

        drv_hex = f"{drv:04X}"
        return {
            "name": name,
            "drv": drv_hex,
            "consistent": bool(
                IDENTITY_RE.fullmatch(name) and name[-4:] == drv_hex
            ),
            "port": self.port,
            "write_capable": False,
        }

    def diagnose(self) -> dict:
        with self._session() as ser:
            name, drv = proto.read_identity(ser)
            motor = proto.read_motor_status(ser)

        drv_hex = f"{drv:04X}"
        identity = {
            "name": name,
            "drv": drv_hex,
            "consistent": bool(
                IDENTITY_RE.fullmatch(name) and name[-4:] == drv_hex
            ),
        }

        return {
            "identity": identity,
            "motor": motor,
            "ready": bool(
                identity["consistent"]
                and motor["armed"] == 0
                and motor["gf"] == 0
                and motor["offset_ok"] == 1
            ),
            "port": self.port,
            "write_capable": False,
            "diagnostic_level": "identity+F0-only",
        }
