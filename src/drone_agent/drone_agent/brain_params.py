"""Fail-closed clamps for brain_node timer parameters (offline-safe)."""
from __future__ import annotations

from typing import Any, Optional

_DEFAULT_LLM_INTERVAL = 7.0
_DEFAULT_OFFBOARD_HZ = 10.0


def safe_finite_float(value: Any, default: Optional[float] = None) -> Optional[float]:
    """Parse a finite float; reject bool, None, non-numeric, NaN, inf."""
    if value is None or isinstance(value, bool):
        return default
    try:
        f = float(value)
    except (TypeError, ValueError):
        return default
    if f != f or f in (float("inf"), float("-inf")):  # NaN / inf
        return default
    return f


def clamp_llm_interval_sec(value: Any) -> float:
    """LLM decision interval seconds in [1.0, 120.0]; default 7.0 if invalid."""
    f = safe_finite_float(value)
    if f is None:
        return _DEFAULT_LLM_INTERVAL
    if f < 1.0:
        return 1.0
    if f > 120.0:
        return 120.0
    return f


def clamp_offboard_rate_hz(value: Any) -> float:
    """Offboard publish rate Hz in [1.0, 50.0]; default 10.0 if invalid."""
    f = safe_finite_float(value)
    if f is None:
        return _DEFAULT_OFFBOARD_HZ
    if f < 1.0:
        return 1.0
    if f > 50.0:
        return 50.0
    return f
