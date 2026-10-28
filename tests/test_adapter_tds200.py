"""Offline serial simulation: no real TDS device is contacted."""
import tempfile
import unittest
from pathlib import Path

from remotelab.adapters.tds200 import TektronixTDS200Adapter
from remotelab.core.engine import Engine


class FakeScope:
    def __init__(self, model="TDS 220"):
        self.port = "FAKE"
        self.model = model
        self.pending = bytearray()
        self.commands = []
        self.closed = False

    def reset_input_buffer(self):
        self.pending.clear()

    def flush(self):
        pass

    def close(self):
        self.closed = True

    def write(self, data):
        command = data.decode("ascii").strip()
        self.commands.append(command)
        replies = {
            "*IDN?": f"TEKTRONIX,{self.model},0,FW:2.03",
            "HORizontal:MAIn:SCAle?": "1.0E-3",
            "CH1:SCAle?": "2.0E-1",
            "CH2:SCAle?": "5.0E-1",
            "TRIGger:MAIn:EDGE:SOUrce?": "CH1",
            "MEASUrement:IMMed:VALue?": "3.684E5",
            "WFMPre:XINcr?": "1.0E-6",
            "WFMPre:XZEro?": "-2.0E-6",
            "WFMPre:PT_Off?": "1",
            "WFMPre:YMUlt?": "2.0E-2",
            "WFMPre:YOFf?": "0",
            "WFMPre:YZEro?": "1.0E-1",
            "CURVe?": "-10,0,10,20",
        }
        if "?" in command:
            if command not in replies:
                raise AssertionError("Unexpected SCPI query: " + command)
            self.pending.extend((replies[command] + "\r\n").encode("ascii"))
        return len(data)

    def read(self, n):
        if not self.pending:
            return b""
        value = bytes(self.pending[:n])
        del self.pending[:n]
        return value


class TektronixAdapterTests(unittest.TestCase):
    def factory(self, model="TDS 220", name="tds220"):
        fake = FakeScope(model)
        adapter = TektronixTDS200Adapter(port="FAKE", name=name,
                                         serial_factory=lambda _: fake)
        return adapter, fake

    def test_identify_210(self):
        adapter, fake = self.factory("TDS 210", "tds210")
        self.assertEqual(adapter.identify()["model"], "TDS210")
        self.assertTrue(fake.closed)

    def test_identify_220(self):
        adapter, _ = self.factory()
        self.assertEqual(adapter.identify()["model"], "TDS220")

    def test_diagnose(self):
        adapter, fake = self.factory()
        result = adapter.diagnose()
        self.assertEqual(result["timebase_s_div"], .001)
        self.assertEqual(result["ch2_v_div"], .5)
        self.assertIn("TRIGger:MAIn:EDGE:SOUrce?", fake.commands)

    def test_measure(self):
        adapter, fake = self.factory()
        result = adapter.measure("CH2", "frequency")
        self.assertEqual(result["value"], 368400)
        self.assertIn("MEASUrement:IMMed:SOUrce CH2", fake.commands)

    def test_waveform_scaling(self):
        adapter, fake = self.factory()
        result = adapter.capture_waveform("CH1", max_points=3)
        self.assertEqual(result["source_points"], 4)
        self.assertEqual(result["returned_points"], 3)
        self.assertEqual(result["samples"],
                         [[-3e-6, -0.1], [-1e-6, 0.3], [0.0, 0.5]])
        self.assertAlmostEqual(result["v_pp"], .6)
        self.assertIn("DATa:ENCdg ASCIi", fake.commands)

    def test_invalid_args_before_serial(self):
        adapter, fake = self.factory()
        with self.assertRaises(ValueError):
            adapter.capture_waveform("CH3")
        with self.assertRaises(ValueError):
            adapter.measure("CH1", "unsafe")
        self.assertEqual(fake.commands, [])

    def test_core_dispatch(self):
        adapter, _ = self.factory()
        with tempfile.TemporaryDirectory() as folder:
            engine = Engine([adapter], Path(folder)/"audit.jsonl")
            result = engine.execute({"device": "tds220",
                                     "operation": "capture_waveform",
                                     "args": {"max_points": 2}})
        self.assertTrue(result["ok"])
        self.assertEqual(result["result"]["returned_points"], 2)

    def test_no_flash_or_motor(self):
        adapter, _ = self.factory()
        with self.assertRaises(PermissionError):
            adapter.flash(b"test")
        with self.assertRaises(PermissionError):
            adapter.run_test("start")


if __name__ == "__main__":
    unittest.main()
