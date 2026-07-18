"""Fail-closed clamps for set_speed / set_heading / look_at GPS (offline-safe)."""
from __future__ import annotations

from typing import Any, Optional, Tuple

_DEFAULT_SPEED = 5.0
_DEFAULT_HEADING = 0.0


def safe_finite_float(value: Any, default: Optional[float] = None) -> Optional[float]:
    if value is None or isinstance(value, bool):
        return default
    try:
        f = float(value)
    except (TypeError, ValueError):
        return default
    if f != f or f in (float("inf"), float("-inf")):
        return default
    return f


def clamp_target_speed_mps(value: Any) -> float:
    """Cruise / pattern speed m/s in [0.1, 25.0]; default 5.0 if invalid."""
    f = safe_finite_float(value)
    if f is None:
        return _DEFAULT_SPEED
    if f < 0.1:
        return 0.1
    if f > 25.0:
        return 25.0
    return f


def clamp_heading_deg(value: Any) -> float:
    """Heading degrees normalized to (-180, 180]; default 0.0 if invalid."""
    f = safe_finite_float(value)
    if f is None:
        return _DEFAULT_HEADING
    # Normalize into (-180, 180]
    x = ((f + 180.0) % 360.0) - 180.0
    if x <= -180.0:
        x += 360.0
    return x


def safe_gps_coord(
    lat: Any,
    lon: Any,
    alt: Any,
    *,
    default_lat: float = 0.0,
    default_lon: float = 0.0,
    default_alt: float = 0.0,
) -> Tuple[float, float, float]:
    """Fail-closed WGS84 lat/lon/alt for ROI / look_at."""
    la = safe_finite_float(lat)
    lo = safe_finite_float(lon)
    al = safe_finite_float(alt)
    if la is None:
        la = float(default_lat)
    if lo is None:
        lo = float(default_lon)
    if al is None:
        al = float(default_alt)
    if la < -90.0:
        la = -90.0
    elif la > 90.0:
        la = 90.0
    if lo < -180.0:
        lo = -180.0
    elif lo > 180.0:
        lo = 180.0
    return la, lo, al
