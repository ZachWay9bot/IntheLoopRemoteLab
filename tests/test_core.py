import tempfile
import unittest
from pathlib import Path

from remotelab.adapters.simulator import SimulatorAdapter
from remotelab.adapters.xbot_legacy import XbotLegacyAdapter
from remotelab.core.engine import Engine


class CoreTests(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.audit = Path(self.tmp.name) / "audit.jsonl"
        self.engine = Engine(
            [SimulatorAdapter(), XbotLegacyAdapter()],
            self.audit,
        )

    def tearDown(self):
        self.tmp.cleanup()

    def test_simulator_identify(self):
        result = self.engine.execute(
            {"device": "simulator", "operation": "identify", "job_id": "t1"}
        )
        self.assertTrue(result["ok"])
        self.assertEqual(result["result"]["id"], "SIM-001")

    def test_simulator_diagnose(self):
        result = self.engine.execute(
            {"device": "simulator", "operation": "diagnose"}
        )
        self.assertTrue(result["result"]["simulated"])

    def test_write_operation_blocked(self):
        with self.assertRaises(PermissionError):
            self.engine.execute({"device": "simulator", "operation": "flash"})

    def test_unknown_device_blocked(self):
        with self.assertRaises(PermissionError):
            self.engine.execute({"device": "missing", "operation": "identify"})

    def test_extra_fields_blocked(self):
        with self.assertRaises(ValueError):
            self.engine.execute(
                {
                    "device": "simulator",
                    "operation": "diagnose",
                    "shell": "cmd.exe",
                }
            )

    def test_audit_created(self):
        self.engine.execute({"device": "simulator", "operation": "identify"})
        self.assertTrue(self.audit.exists())

    def test_xbot_placeholder_is_read_only(self):
        result = self.engine.execute(
            {"device": "xbot_legacy", "operation": "identify"}
        )
        self.assertTrue(result["ok"])
        self.assertFalse(result["result"]["write_capable"])


if __name__ == "__main__":
    unittest.main()
