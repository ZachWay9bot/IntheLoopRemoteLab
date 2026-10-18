from ..base import DeviceAdapter


class XbotLegacyAdapter(DeviceAdapter):
    name = "xbot_legacy"

    def identify(self) -> dict:
        return {
            "adapter": self.name,
            "status": "migration-placeholder",
            "production_agent_untouched": True,
            "write_capable": False,
        }

    def diagnose(self) -> dict:
        return {
            "adapter": self.name,
            "status": "not-connected",
            "write_capable": False,
        }
