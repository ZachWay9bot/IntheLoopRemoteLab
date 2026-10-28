"""Tektronix TDS 210/220 RS-232 adapter for IntheLoopRemoteLab.

ASCII SCPI; no firmware flashing, acquisition start/stop or motor commands.
Waveform-source/format selection and immediate measurement configuration
affect the oscilloscope only.
"""
from __future__ import annotations

import contextlib
import math
import re
import time

from remotelab.adapters.base import DeviceAdapter

_ID_RE = re.compile(r"\bTDS\s*2(?:10|20)\b", re.IGNORECASE)
_CHANNELS = {"CH1", "CH2"}
_MEASURES = {
    "frequency": "FREQuency", "period": "PERIod",
    "vpp": "PK2pk", "mean": "MEAN", "rms": "CRMs",
}


class TektronixTDS200Adapter(DeviceAdapter):
    """One configured adapter instance per scope/port."""

    def __init__(self, port="COM11", name="tds220", baudrate=9600,
                 flow_control="none", serial_factory=None):
        if flow_control not in ("none", "rtscts", "xonxoff"):
            raise ValueError("flow_control must be none, rtscts or xonxoff")
        self.port = port
        self.name = name
        self.baudrate = int(baudrate)
        self.flow_control = flow_control
        self._serial_factory = serial_factory

    @contextlib.contextmanager
    def _session(self):
        if self._serial_factory is not None:
            ser = self._serial_factory(self.port)
        else:
            try:
                import serial
            except ImportError as exc:
                raise RuntimeError("Install: py -m pip install -e .[serial]") from exc
            ser = serial.Serial(
                port=self.port, baudrate=self.baudrate, bytesize=8,
                parity="N", stopbits=1, timeout=0.1, write_timeout=2.0,
                rtscts=self.flow_control == "rtscts",
                xonxoff=self.flow_control == "xonxoff",
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
    def _send(ser, command):
        ser.write((command + "\n").encode("ascii"))
        if hasattr(ser, "flush"):
            ser.flush()

    @staticmethod
    def _readline(ser, timeout=2.0, max_bytes=65536):
        deadline = time.monotonic() + timeout
        raw = bytearray()
        while time.monotonic() < deadline:
            part = ser.read(1)
            if not part:
                continue
            if part == b"\n":
                return bytes(raw).rstrip(b"\r").decode("ascii", "replace").strip()
            raw.extend(part)
            if len(raw) > max_bytes:
                raise ValueError("TDS response exceeded limit")
        raise TimeoutError("TDS response timeout: check baud, EOL and flow control")

    @classmethod
    def _query(cls, ser, command, timeout=2.0):
        cls._send(ser, command)
        return cls._readline(ser, timeout=timeout)

    @classmethod
    def _identity(cls, ser):
        for command in ("*IDN?", "ID?"):
            try:
                answer = cls._query(ser, command)
            except TimeoutError:
                continue
            found = _ID_RE.search(answer)
            if found:
                return answer, found.group(0).replace(" ", "").upper()
        raise RuntimeError("No supported TDS 210/220 identity on serial port")

    @staticmethod
    def _channel(channel):
        if channel not in _CHANNELS:
            raise ValueError("channel must be CH1 or CH2")
        return channel

    @classmethod
    def _number(cls, ser, command):
        answer = cls._query(ser, command)
        token = answer.split(";")[0].split()[-1].strip('"') if answer else ""
        try:
            return float(token)
        except ValueError as exc:
            raise ValueError(f"Unexpected {command} response: {answer[:100]!r}") from exc

    def identify(self):
        with self._session() as ser:
            identity, model = self._identity(ser)
        return {"identity": identity, "model": model, "port": self.port,
                "baudrate": self.baudrate, "read_only": True}

    def diagnose(self):
        with self._session() as ser:
            identity, model = self._identity(ser)
            readings = {}
            for key, command in (
                ("timebase_s_div", "HORizontal:MAIn:SCAle?"),
                ("ch1_v_div", "CH1:SCAle?"),
                ("ch2_v_div", "CH2:SCAle?"),
            ):
                readings[key] = self._number(ser, command)
            readings["trigger_source"] = self._query(
                ser, "TRIGger:MAIn:EDGE:SOUrce?"
            )
        return {"identity": identity, "model": model, "port": self.port,
                "read_only": True, **readings}

    def measure(self, channel="CH1", kind="frequency"):
        channel = self._channel(channel)
        if kind not in _MEASURES:
            raise ValueError("kind must be frequency, period, vpp, mean or rms")
        with self._session() as ser:
            _, model = self._identity(ser)
            self._send(ser, f"MEASUrement:IMMed:SOUrce {channel}")
            self._send(ser, f"MEASUrement:IMMed:TYPe {_MEASURES[kind]}")
            value = self._number(ser, "MEASUrement:IMMed:VALue?")
        if not math.isfinite(value) or abs(value) >= 9e36:
            raise ValueError("TDS measurement unavailable: check signal/trigger")
        return {"model": model, "channel": channel, "kind": kind,
                "value": value, "unit": "Hz" if kind == "frequency" else
                "s" if kind == "period" else "V"}

    def capture_waveform(self, channel="CH1", max_points=250):
        """Read up to 2500 raw points, return decimated calibrated X/Y pairs."""
        channel = self._channel(channel)
        if type(max_points) is not int or not 2 <= max_points <= 2500:
            raise ValueError("max_points must be an integer from 2 to 2500")
        with self._session() as ser:
            _, model = self._identity(ser)
            for command in (
                f"DATa:SOUrce {channel}", "DATa:ENCdg ASCIi",
                "DATa:WIDth 1", "DATa:STARt 1", "DATa:STOP 2500",
            ):
                self._send(ser, command)
            xinc = self._number(ser, "WFMPre:XINcr?")
            xzero = self._number(ser, "WFMPre:XZEro?")
            offset = self._number(ser, "WFMPre:PT_Off?")
            ymult = self._number(ser, "WFMPre:YMUlt?")
            yoff = self._number(ser, "WFMPre:YOFf?")
            yzero = self._number(ser, "WFMPre:YZEro?")
            raw = self._query(ser, "CURVe?", timeout=40.0)
        raw = re.sub(r"^:?CURVE\s+", "", raw, flags=re.IGNORECASE)
        try:
            values = [int(item.strip()) for item in raw.split(",")]
        except ValueError as exc:
            raise ValueError("Unexpected ASCII waveform format") from exc
        if not 1 <= len(values) <= 2500:
            raise ValueError(f"Unexpected waveform length: {len(values)}")
        volts = [yzero + ymult * (sample - yoff) for sample in values]
        indices = (list(range(len(values))) if len(values) <= max_points else
                   [round(i * (len(values) - 1) / (max_points - 1))
                    for i in range(max_points)])
        samples = [[round(xzero + (i - offset) * xinc, 12),
                    round(volts[i], 8)] for i in indices]
        return {
            "model": model, "port": self.port, "channel": channel,
            "source_points": len(values), "returned_points": len(samples),
            "format": "[time_s, voltage_v]", "samples": samples,
            "v_min": min(volts), "v_max": max(volts),
            "v_pp": max(volts) - min(volts),
            "v_rms_record": math.sqrt(sum(v*v for v in volts)/len(volts)),
        }
