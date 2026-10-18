from __future__ import annotations

import importlib

from .base import DeviceAdapter


def load_adapter(spec: dict) -> DeviceAdapter:
    if not isinstance(spec, dict):
        raise ValueError("adapter spec must be an object")
    if not spec.get("enabled", True):
        raise ValueError("disabled adapter cannot be loaded")

    module_name = spec.get("module")
    class_name = spec.get("class")
    args = spec.get("args", {})

    if not isinstance(module_name, str) or not module_name:
        raise ValueError("adapter.module is required")
    if not isinstance(class_name, str) or not class_name:
        raise ValueError("adapter.class is required")
    if not isinstance(args, dict):
        raise ValueError("adapter.args must be an object")

    module = importlib.import_module(module_name)
    cls = getattr(module, class_name, None)
    if cls is None:
        raise ValueError(f"adapter class not found: {module_name}:{class_name}")

    adapter = cls(**args)
    if not isinstance(adapter, DeviceAdapter):
        raise TypeError(
            f"{module_name}:{class_name} is not a DeviceAdapter"
        )
    return adapter


def load_adapters(specs: list[dict]) -> list[DeviceAdapter]:
    if not isinstance(specs, list):
        raise ValueError("adapters must be a list")

    adapters = [
        load_adapter(spec)
        for spec in specs
        if isinstance(spec, dict) and spec.get("enabled", True)
    ]

    if not adapters:
        raise ValueError("no adapters enabled")

    names = [adapter.name for adapter in adapters]
    if len(names) != len(set(names)):
        raise ValueError("adapter names must be unique")

    return adapters
