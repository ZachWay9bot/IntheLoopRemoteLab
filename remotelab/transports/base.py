from abc import ABC, abstractmethod


class Transport(ABC):
    """Job source/sink boundary.

    A transport moves jobs and results. It must not contain hardware-specific
    flash or motor-control logic.
    """

    @abstractmethod
    def receive(self):
        raise NotImplementedError

    @abstractmethod
    def publish_result(self, result: dict) -> None:
        raise NotImplementedError
