"""DeltaESC G30 application identity and frozen read-only diagnosis.

The existing GitHub Issue queue engine allows identify/diagnose only.
This adapter never emits IAP/flash/motor/offset writes and never guesses
whether a new stock DRV firmware supports DeltaESC-specific read registers.
"""
from __future__ import annotations

import contextlib
import struct
import time

from remotelab.adapters.base import DeviceAdapter
from remotelab.adapters.xbot.protocol import decode_frame, frame


class DeltaEscReadOnlyAdapter(DeviceAdapter):
    name = "deltaesc_g30"

    def __init__(self, port: str = "COM9", serial_factory=None):
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
                raise RuntimeError("pyserial required: py -m pip install -e .[serial]") from exc
            ser = serial.Serial(
                port=self.port,
                baudrate=115200,
                timeout=0.05,
                write_timeout=1.0,
            )
        try:
            if hasattr(ser, "reset_input_buffer"):
                ser.reset_input_buffer()
            yield ser
        finally:
            close = getattr(ser, "close", None)
            if close:
                close()

    @staticmethod
    def _read(ser, reg: int, length: int, timeout: float = 0.6):
        """One read request, ignore an echoed TX frame, check address & CRC."""
        outgoing = frame(0x01, reg, bytes((length,)))
        ser.write(outgoing)
        deadline = time.monotonic() + timeout
        buf = bytearray()
        while time.monotonic() < deadline:
            b = ser.read(1)
            if not b:
                continue
            buf += b
            while len(buf) >= 2 and buf[:2] != b"\x5a\xa5":
                del buf[0]
            if len(buf) < 3:
                continue
            n = buf[2]
            if n > 56:
                del buf[0]
                continue
            total = n + 9
            if len(buf) < total:
                continue
            packet = bytes(buf[:total])
            del buf[:total]
            try:
                reply = decode_frame(packet)
            except ValueError:
                continue
            # Ignore electrical TX echo, unrelated dashboard telegrams and
            # responses to an earlier query; do not interpret as calibration.
            if (reply["src"], reply["dst"], reply["cmd"], reply["index"]) != (0x20, 0x3d, 0x04, reg):
                continue
            if len(reply["data"]) != length:
                raise RuntimeError(f"Unexpected DeltaESC read length at 0x{reg:02X}")
            return reply["data"]
        raise TimeoutError(f"No valid read-only response for register 0x{reg:02X} on {ser.port if hasattr(ser,'port') else 'serial'}")

    def identify(self) -> dict:
        with self._session() as ser:
            raw = self._read(ser, 0x10, 14)
            identity = raw.decode("ascii", "replace").rstrip("\0")
        # Deliberately do NOT request DeltaESC-only registers on unknown stock.
        return {
            "identity": identity,
            "is_deltaesc": identity == "DELTAESC-G30D0",
            "port": self.port,
            "read_only": True,
            "iap_or_recovery_verified": False,
            "motor_running": False,
        }

    def diagnose(self) -> dict:
        with self._session() as ser:
            identity = self._read(ser, 0x10, 14).decode("ascii", "replace").rstrip("\0")
            if identity != "DELTAESC-G30D0":
                return {
                    "identity": identity,
                    "is_deltaesc": False,
                    "port": self.port,
                    "read_only": True,
                    "note": "Stock/unknown firmware: no DeltaESC-specific diagnostic registers queried",
                }
            d0 = self._read(ser, 0xd0, 16)
            if d0[:4] != b"DESC":
                raise RuntimeError("DeltaESC diagnostic signature mismatch")
            d9 = self._read(ser, 0xd9, 16)
            ff = self._read(ser, 0xff, 12)
            if ff[:4] != b"PF13":
                raise RuntimeError("Motor profile diagnostic signature mismatch")
        guards = struct.unpack_from("<H", d9, 6)[0]
        return {
            "identity": identity,
            "is_deltaesc": True,
            "port": self.port,
            "read_only": True,
            "foc_state": d0[8],
            "status_flags": d0[9],
            "fault": struct.unpack_from("<H", d0, 10)[0],
            "pwm_hz": struct.unpack_from("<H", d0, 12)[0],
            "control_hz": struct.unpack_from("<H", d0, 14)[0],
            "motor_params_valid": bool(d9[9]),
            "adc_offsets_valid": bool(d9[8]),
            "commissioning_guard_mask": guards,
            "pole_pairs": ff[4],
            "wheel_circumference_mm": struct.unpack_from("<H", ff, 6)[0],
            "phase_offset": struct.unpack_from("<h", ff, 8)[0],
            "drive_build": bool(ff[11]),
            "real_motor_run_verified": False,
            "iap_or_recovery_verified": False,
        }
