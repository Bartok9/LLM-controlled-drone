"""Fail-closed battery telemetry lines for LLM prompts."""

from __future__ import annotations

import math
from typing import Any


def format_battery_line(remaining: Any, voltage_v: Any = None) -> str:
    """Format a single battery line; never raise on bad telemetry."""
    pct: float | None = None
    try:
        r = float(remaining)
    except (TypeError, ValueError):
        r = float("nan")
    if math.isfinite(r):
        if 0.0 <= r <= 1.0:
            pct = r * 100.0
        elif 0.0 <= r <= 100.0:
            pct = r
        else:
            pct = max(0.0, min(100.0, r))

    volt_s = ""
    try:
        v = float(voltage_v)
    except (TypeError, ValueError):
        v = float("nan")
    if math.isfinite(v) and 0.0 < v <= 100.0:
        volt_s = f" ({v:.1f}V)"

    if pct is None:
        if volt_s:
            return f"Battery: unknown{volt_s}"
        return "Battery: unknown"
    return f"Battery: {pct:.0f}%{volt_s}"
