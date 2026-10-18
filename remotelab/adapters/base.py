from abc import ABC, abstractmethod


class DeviceAdapter(ABC):
    name = "unnamed"

    @abstractmethod
    def identify(self) -> dict:
        raise NotImplementedError

    @abstractmethod
    def diagnose(self) -> dict:
        raise NotImplementedError

    def flash(self, image: bytes, permit=None) -> dict:
        raise PermissionError(
            "Hardware writes are disabled until the adapter is migrated and validated"
        )

    def run_test(self, test_name: str, permit=None) -> dict:
        raise PermissionError(
            "Active hardware tests are disabled until the adapter is migrated and validated"
        )
