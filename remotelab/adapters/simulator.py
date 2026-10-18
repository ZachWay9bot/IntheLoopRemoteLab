from .base import DeviceAdapter


class SimulatorAdapter(DeviceAdapter):
    name = "simulator"

    def identify(self) -> dict:
        return {
            "id": "SIM-001",
            "adapter": self.name,
            "write_capable": False,
        }

    def diagnose(self) -> dict:
        return {
            "simulated": True,
            "healthy": True,
            "write_capable": False,
        }
