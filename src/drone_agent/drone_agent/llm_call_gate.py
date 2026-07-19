"""Fail-closed helpers for throttling brain_node LLM calls."""

from __future__ import annotations

import math
from typing import Any, Optional

_DEFAULT_MIN_INTERVAL = 3.0
_MIN_INTERVAL_LO = 0.5
_MIN_INTERVAL_HI = 60.0


def safe_finite_float(value: Any, default: Optional[float] = None) -> Optional[float]:
    """Return a finite float, or default. Rejects bool and non-numeric noise."""
    if isinstance(value, bool) or value is None:
        return default
    try:
        f = float(value)
    except (TypeError, ValueError):
        return default
    if not math.isfinite(f):
        return default
    return f


def clamp_min_llm_call_interval_sec(value: Any) -> float:
    """Clamp min seconds between LLM calls; default 3.0 if invalid."""
    f = safe_finite_float(value, default=None)
    if f is None or f <= 0:
        return _DEFAULT_MIN_INTERVAL
    return max(_MIN_INTERVAL_LO, min(_MIN_INTERVAL_HI, f))


def should_allow_llm_call(now: float, last_call: float, min_interval: float) -> bool:
    """True when enough wall time has elapsed since last_call."""
    n = safe_finite_float(now, default=None)
    last = safe_finite_float(last_call, default=None)
    interval = clamp_min_llm_call_interval_sec(min_interval)
    if n is None or last is None:
        return False
    return (n - last) >= interval
