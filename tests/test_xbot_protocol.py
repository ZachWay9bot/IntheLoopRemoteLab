import struct
import unittest

from remotelab.adapters import xbot_protocol as proto


class ProtocolTests(unittest.TestCase):
    def test_frame_roundtrip(self):
        raw = proto.frame(0x01, 16, b"\x0E")
        decoded = proto.decode_frame(raw)
        self.assertEqual(decoded["cmd"], 0x01)
        self.assertEqual(decoded["index"], 16)
        self.assertEqual(decoded["data"], b"\x0E")

    def test_bad_checksum_rejected(self):
        raw = bytearray(proto.frame(0x01, 16, b"\x0E"))
        raw[-1] ^= 0x01
        with self.assertRaises(ValueError):
            proto.decode_frame(bytes(raw))

    def test_parse_motor_status(self):
        data = bytearray(102)
        data[:4] = b"XB03"
        struct.pack_into("<I", data, 4, 1234)
        data[8] = 0
        data[9] = 0
        data[10] = 0
        data[12] = 1
        data[14] = 1
        data[15] = 99
        struct.pack_into("<H", data, 16, 2400)
        struct.pack_into("<I", data, 78, 0)

        result = proto.parse_motor_status(bytes(data))
        self.assertEqual(result["ms"], 1234)
        self.assertEqual(result["armed"], 0)
        self.assertEqual(result["offset_ok"], 1)
        self.assertEqual(result["gf"], 0)
        self.assertEqual(result["vbat"], 2400)

    def test_identity_suffix(self):
        self.assertEqual(proto.version_suffix("XBOTFO76V00761"), "76")

    def test_identity_suffix_rejects_garbage(self):
        with self.assertRaises(RuntimeError):
            proto.version_suffix("not-an-xbot")


if __name__ == "__main__":
    unittest.main()
