from __future__ import annotations

import re
import struct
import time


def frame(cmd: int, index: int = 0, data: bytes = b"", src: int = 0x3D, dst: int = 0x20) -> bytes:
    header = bytes([len(data), src, dst, cmd, index]) + data
    checksum = (~sum(header)) & 0xFFFF
    return b"\x5A\xA5" + header + struct.pack("<H", checksum)


def decode_frame(raw: bytes) -> dict:
    if len(raw) < 9:
        raise ValueError("frame too short")
    if raw[:2] != b"\x5A\xA5":
        raise ValueError("bad frame header")

    data_len = raw[2]
    total = data_len + 9
    if len(raw) != total:
        raise ValueError(f"bad frame length: expected {total}, got {len(raw)}")

    expected = (~sum(raw[2:-2])) & 0xFFFF
    actual = struct.unpack("<H", raw[-2:])[0]
    if expected != actual:
        raise ValueError("bad frame checksum")

    return {
        "src": raw[3],
        "dst": raw[4],
        "cmd": raw[5],
        "index": raw[6],
        "data": raw[7:-2],
    }


def recv(ser, timeout: float = 1.0) -> bytes:
    deadline = time.monotonic() + timeout
    buf = bytearray()

    while time.monotonic() < deadline:
        byte = ser.read(1)
        if not byte:
            continue

        buf += byte
        while len(buf) >= 2 and buf[:2] != b"\x5A\xA5":
            del buf[0]

        if len(buf) >= 3:
            total = buf[2] + 9
            if len(buf) >= total:
                raw = bytes(buf[:total])
                del buf[:total]
                decode_frame(raw)
                return raw

    raise TimeoutError("no valid XBOT reply")


def request(ser, cmd: int, index: int = 0, data: bytes = b"", timeout: float = 1.0) -> dict:
    ser.write(frame(cmd, index, data))
    return decode_frame(recv(ser, timeout=timeout))


def read_map(ser, index: int, count: int) -> bytes:
    reply = request(ser, 0x01, index, bytes([count]))
    if reply["cmd"] != 0x04:
        raise RuntimeError("unexpected READ reply")
    return reply["data"]


def read_identity(ser) -> tuple[str, int]:
    name = read_map(ser, 16, 14).replace(b"\x00", b"").decode("ascii", "replace").strip()
    drv_raw = read_map(ser, 26, 2)
    if len(drv_raw) != 2:
        raise RuntimeError("invalid DRV version length")
    drv = struct.unpack("<H", drv_raw)[0]
    return name, drv


def version_suffix(identity: str) -> str:
    match = re.fullmatch(r"XBOTFO(\d\d)V[0-9A-F]{5}", identity or "")
    if not match:
        raise RuntimeError(f"unsupported identity {identity!r}")
    return match.group(1)


def _u16(data: bytes, offset: int) -> int:
    return struct.unpack_from("<H", data, offset)[0]


def _s16(data: bytes, offset: int) -> int:
    return struct.unpack_from("<h", data, offset)[0]


def _u32(data: bytes, offset: int) -> int:
    return struct.unpack_from("<I", data, offset)[0]


def parse_motor_status(data: bytes) -> dict:
    if len(data) != 102 or data[:4] != b"XB03":
        raise RuntimeError("unexpected motor status payload")

    direction = data[14] if data[14] < 128 else data[14] - 256
    dscore = data[82] if data[82] < 128 else data[82] - 256

    return {
        "ms": _u32(data, 4),
        "state": data[8],
        "fault": data[9],
        "armed": data[10],
        "coast": data[11],
        "offset_ok": data[12],
        "sector": data[13],
        "dir": direction,
        "dscore": dscore,
        "good": data[15],
        "vbat": _u16(data, 16),
        "cur": (_s16(data, 24), _s16(data, 26), _s16(data, 28)),
        "span": _u16(data, 36),
        "ctrl": _u16(data, 44),
        "olstep": _u16(data, 46),
        "obsstep": _u16(data, 48),
        "pe": _s16(data, 50),
        "id": _s16(data, 52),
        "iq": _s16(data, 54),
        "peak": _u16(data, 56),
        "trans": _u32(data, 58),
        "bad": _u32(data, 62),
        "rev": _u32(data, 66),
        "samples": _u32(data, 74),
        "gf": _u32(data, 78),
        "speed_samples": _u16(data, 86),
        "idref": _s16(data, 88),
        "iqref": _s16(data, 90),
        "ccr": (_u16(data, 96), _u16(data, 98), _u16(data, 100)),
    }


def read_motor_status(ser) -> dict:
    reply = request(ser, 0xF0)
    if reply["cmd"] != 0xF0:
        raise RuntimeError("unexpected motor status command")
    return parse_motor_status(reply["data"])
