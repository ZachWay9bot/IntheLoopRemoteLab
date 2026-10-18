from .base import DeviceAdapter


class XbotLegacyAdapter(DeviceAdapter):
    """Migration boundary for the existing production XBOT RemoteLab.

    This adapter intentionally does not talk to COM ports, flash firmware, or
    submit jobs yet. The existing XBOT installation and its queue remain the
    production path until the newer agent behaviour has been migrated and
    regression-tested.
    """

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
            "reason": "Use the existing production XBOT RemoteLab during migration",
            "write_capable": False,
        }
