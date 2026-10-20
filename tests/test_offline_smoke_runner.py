import subprocess
import sys
import unittest
from pathlib import Path


class OfflineSmokeRunnerTests(unittest.TestCase):
    def test_all_three_firmware_fixture_routes_run_without_hardware(self):
        root = Path(__file__).resolve().parents[1]
        result = subprocess.run(
            [sys.executable, "-m", "tools.offline_three_firmware_smoke"],
            cwd=root,
            capture_output=True,
            text=True,
            timeout=30,
            check=False,
        )
        self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
        self.assertIn("Fixture dispatch checks: 6/6 PASS", result.stdout)
        self.assertIn("Hardware and firmware readiness: NOT TESTED", result.stdout)


if __name__ == "__main__":
    unittest.main()
