import unittest

from remotelab.adapters.loader import load_adapter, load_adapters
from remotelab.adapters.simulator import SimulatorAdapter


class AdapterLoaderTests(unittest.TestCase):
    def test_load_simulator(self):
        adapter = load_adapter(
            {
                "module": "remotelab.adapters.simulator",
                "class": "SimulatorAdapter",
                "args": {},
            }
        )
        self.assertIsInstance(adapter, SimulatorAdapter)

    def test_disabled_entries_are_skipped(self):
        adapters = load_adapters(
            [
                {
                    "module": "does.not.matter",
                    "class": "Nope",
                    "enabled": False,
                },
                {
                    "module": "remotelab.adapters.simulator",
                    "class": "SimulatorAdapter",
                    "enabled": True,
                    "args": {},
                },
            ]
        )
        self.assertEqual(len(adapters), 1)

    def test_duplicate_names_rejected(self):
        spec = {
            "module": "remotelab.adapters.simulator",
            "class": "SimulatorAdapter",
            "args": {},
        }
        with self.assertRaises(ValueError):
            load_adapters([spec, spec])


if __name__ == "__main__":
    unittest.main()
