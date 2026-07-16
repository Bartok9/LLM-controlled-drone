#!/usr/bin/env python3
"""Pure helpers: clamp YOLO node parameters and validate frame geometry."""

from __future__ import annotations

import math
from typing import Any, Optional, Tuple


def clamp_confidence(value: Any, default: float = 0.5) -> float:
    """Return confidence in (0, 1]; bool/bad/non-positive → default."""
    if isinstance(value, bool) or value is None:
        return float(default)
    try:
        num = float(value)
    except (TypeError, ValueError):
        return float(default)
    if not math.isfinite(num) or num <= 0.0:
        return float(default)
    if num > 1.0:
        return 1.0
    return num


def clamp_skip_frames(value: Any, default: int = 2) -> int:
    """Return skip_frames in [0, 120]; reject bool and non-finite."""
    if isinstance(value, bool) or value is None:
        return int(default)
    try:
        num = float(value)
    except (TypeError, ValueError):
        return int(default)
    if not math.isfinite(num):
        return int(default)
    n = int(num)
    if n < 0:
        return int(default)
    if n > 120:
        return 120
    return n


def safe_frame_dims(h: Any, w: Any) -> Optional[Tuple[int, int]]:
    """Return (h, w) when both are positive integers; else None."""
    if isinstance(h, bool) or isinstance(w, bool):
        return None
    try:
        hi = int(h)
        wi = int(w)
    except (TypeError, ValueError):
        return None
    if hi <= 0 or wi <= 0:
        return None
    return hi, wi
