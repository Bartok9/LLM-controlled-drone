"""Helpers for safe offboard publish timer periods."""

from __future__ import annotations

import math
from typing import Any


def clamp_offboard_rate_hz(value: Any, default: float = 10.0) -> float:
    """Return a finite offboard rate in [0.5, 50.0] Hz, else *default*."""
    try:
        rate = float(value)
    except (TypeError, ValueError):
        return float(default)
    if not math.isfinite(rate) or rate <= 0.0:
        return float(default)
    return max(0.5, min(50.0, rate))


def offboard_period_sec(rate_hz: Any, default_rate: float = 10.0) -> float:
    """Seconds between offboard ticks (never divides by zero)."""
    rate = clamp_offboard_rate_hz(rate_hz, default=default_rate)
    return 1.0 / rate
