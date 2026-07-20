"""Fail-closed helpers for square survey geometry / odometry."""

from __future__ import annotations

import math
from typing import Optional, Tuple, Union

Number = Union[int, float]

_DEFAULT_THRESHOLD_M = 1.0
_THRESHOLD_MIN_M = 0.1
_THRESHOLD_MAX_M = 50.0


def clamp_square_threshold_m(
    value: object,
    default: float = _DEFAULT_THRESHOLD_M,
) -> float:
    """Clamp square waypoint reach threshold to [0.1, 50] meters.

    Invalid, missing, or non-finite values return *default* (1.0 m).
    """
    if value is None:
        return float(default)
    try:
        num = float(value)  # type: ignore[arg-type]
    except (TypeError, ValueError):
        return float(default)
    if not math.isfinite(num):
        return float(default)
    return max(_THRESHOLD_MIN_M, min(_THRESHOLD_MAX_M, num))


def finite_ned_xyz(
    x: object,
    y: object,
    z: object,
) -> Optional[Tuple[float, float, float]]:
    """Parse NED x/y/z; return None unless all three are finite floats."""
    try:
        fx = float(x)  # type: ignore[arg-type]
        fy = float(y)  # type: ignore[arg-type]
        fz = float(z)  # type: ignore[arg-type]
    except (TypeError, ValueError):
        return None
    if not (math.isfinite(fx) and math.isfinite(fy) and math.isfinite(fz)):
        return None
    return fx, fy, fz
