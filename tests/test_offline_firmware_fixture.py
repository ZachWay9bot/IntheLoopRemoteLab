import json
import tempfile
import unittest
from pathlib import Path

from remotelab.adapters.loader import load_adapters
from remotelab.core.engine import Engine


class OfflineFirmwareFixtureTests(unittest.TestCase):
    def setUp(self):
        self.config = json.loads(
            (Path(__file__).resolve().parents[1] / "examples"
             / "offline_firmware_adapters.example.json").read_text(encoding="utf-8")
        )
        self.adapters = load_adapters(self.config["adapters"])

    def test_three_distinct_project_adapters(self):
        self.assertEqual(
            {a.name for a in self.adapters},
            {"offline_deltaesc", "offline_ebics", "offline_smartesc"},
        )

    def test_every_result_is_clearly_synthetic_and_no_firmware_is_run(self):
        with tempfile.TemporaryDirectory() as td:
            engine = Engine(self.adapters, Path(td) / "audit.jsonl")
            for adapter in self.adapters:
                for operation in ("identify", "diagnose"):
                    result = engine.execute({"device": adapter.name, "operation": operation})
                    self.assertTrue(result["ok"], result)
                    data = result["result"]
                    self.assertTrue(data["simulated"])
                    self.assertFalse(data["hardware_connected"])
                    self.assertFalse(data["write_capable"])
                    self.assertEqual(data["evidence"], "synthetic-fixture-only")
                self.assertFalse(engine.execute(
                    {"device": adapter.name, "operation": "diagnose"}
                )["result"]["firmware_executed"])

    def test_flash_and_motor_tests_not_exposed_by_core(self):
        with tempfile.TemporaryDirectory() as td:
            engine = Engine(self.adapters, Path(td) / "audit.jsonl")
            for adapter in self.adapters:
                for op in ("flash", "run_test"):
                    with self.assertRaises(PermissionError):
                        engine.execute({"device": adapter.name, "operation": op})

    def test_fixture_is_defensively_copied(self):
        a = self.adapters[0]
        initial = a.diagnose()["fixture"]["result"]
        data = a.diagnose()
        data["fixture"]["result"] = "tampered"
        self.assertEqual(a.diagnose()["fixture"]["result"], initial)

    def test_invalid_name_rejected(self):
        from remotelab.adapters.offline_fixture import OfflineFirmwareFixtureAdapter
        with self.assertRaises(ValueError):
            OfflineFirmwareFixtureAdapter(name="real_device", project="X",
                                          firmware_reference="unverified")


if __name__ == "__main__":
    unittest.main()
