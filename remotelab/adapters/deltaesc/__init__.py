"""Read-only DeltaESC G30 application adapter. No old XBOT queue or motor actions."""
from .readonly import DeltaEscReadOnlyAdapter

__all__ = ["DeltaEscReadOnlyAdapter"]
