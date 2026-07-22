"""Fail-closed helpers for BrainNode._target_found approach geometry."""

from __future__ import annotations

import math
from typing import Any, Optional, Sequence


def safe_float(value: Any) -> Optional[float]:
    """Coerce to finite float; reject bool/None/non-numeric/non-finite."""
    if value is None or isinstance(value, bool):
        return None
    try:
        num = float(value)
    except (TypeError, ValueError):
        return None
    if not math.isfinite(num):
        return None
    return num


def yaw_from_odom_quaternion(q: Any) -> Optional[float]:
    """Extract yaw (rad) from VehicleOdometry quaternion [w, x, y, z].

    Returns None when *q* is missing, too short, or contains non-finite values.
    """
    if q is None or not isinstance(q, Sequence) or isinstance(q, (str, bytes)):
        return None
    if len(q) < 4:
        return None
    w = safe_float(q[0])
    x = safe_float(q[1])
    y = safe_float(q[2])
    z = safe_float(q[3])
    if None in (w, x, y, z):
        return None
    # type narrowing
    assert w is not None and x is not None and y is not None and z is not None
    return math.atan2(
        2.0 * (w * z + x * y),
        1.0 - 2.0 * (y * y + z * z),
    )


def clamp_hover_alt_z(
    current_alt_agl: Any,
    fraction: float = 0.4,
    min_alt_m: float = 5.0,
    max_alt_m: float = 120.0,
) -> float:
    """Return NED-down hover altitude (negative) with AGL floor/ceiling.

    Non-finite / non-positive current altitude → ``-min_alt_m``.
    """
    alt = safe_float(current_alt_agl)
    if alt is None or alt <= 0.0:
        return -float(min_alt_m)
    hover_agl = max(float(min_alt_m), alt * float(fraction))
    hover_agl = max(float(min_alt_m), min(float(max_alt_m), hover_agl))
    return -hover_agl


def clamp_approach_distance_m(
    current_alt_agl: Any,
    fraction: float = 0.3,
    max_dist_m: float = 8.0,
    min_dist_m: float = 0.0,
) -> float:
    """Clamp lateral approach distance toward a visual target.

    Non-finite current altitude → ``0.0`` (no lateral move).
    """
    alt = safe_float(current_alt_agl)
    if alt is None or alt < 0.0:
        return 0.0
    dist = alt * float(fraction)
    dist = max(float(min_dist_m), min(float(max_dist_m), dist))
    if not math.isfinite(dist):
        return 0.0
    return float(dist)
