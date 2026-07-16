#!/usr/bin/env python3
"""Pure helpers: validate GPS home fix and NED odometry before flight-state update."""

from __future__ import annotations

import math
from typing import Any, Optional


def safe_float(value: Any, default: Optional[float] = None) -> Optional[float]:
    """Coerce to float; reject bool, non-finite, and bad types."""
    if value is None:
        return default
    if isinstance(value, bool):
        return default
    try:
        num = float(value)
    except (TypeError, ValueError):
        return default
    if not math.isfinite(num):
        return default
    return num


def is_valid_home_fix(
    lat: Any,
    lon: Any,
    alt: Any,
    fix_type: Any,
    min_fix: int = 3,
) -> bool:
    """True when fix quality and lat/lon/alt are safe to use as home origin."""
    try:
        fix_i = int(fix_type)
    except (TypeError, ValueError):
        return False
    if isinstance(fix_type, bool):
        return False
    if fix_i < int(min_fix):
        return False

    lat_f = safe_float(lat)
    lon_f = safe_float(lon)
    alt_f = safe_float(alt)
    if lat_f is None or lon_f is None or alt_f is None:
        return False
    if not (-90.0 <= lat_f <= 90.0):
        return False
    if not (-180.0 <= lon_f <= 180.0):
        return False
    return True


def is_valid_ned_position(x: Any, y: Any, z: Any) -> bool:
    """True when all three NED components are finite floats (bool rejected)."""
    return (
        safe_float(x) is not None
        and safe_float(y) is not None
        and safe_float(z) is not None
    )


def position_triple_valid(pos: Any) -> bool:
    """Validate indexable position sequence of length >= 3."""
    try:
        return is_valid_ned_position(pos[0], pos[1], pos[2])
    except (TypeError, IndexError, KeyError):
        return False
