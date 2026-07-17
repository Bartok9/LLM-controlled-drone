"""Fail-closed clamps for orbit / square survey geometry (no ROS deps)."""

from __future__ import annotations

from typing import Any, Optional


def safe_finite_float(value: Any, default: Optional[float] = None) -> Optional[float]:
    """Return a finite float, or *default*. Rejects bool and non-numeric."""
    if isinstance(value, bool) or value is None:
        return default
    try:
        f = float(value)
    except (TypeError, ValueError):
        return default
    if f != f or f in (float("inf"), float("-inf")):  # NaN / inf
        return default
    return f


def clamp_positive(
    value: Any,
    default: float,
    min_v: float,
    max_v: float,
) -> float:
    """Parse finite float; if invalid use *default*; clamp to [min_v, max_v]."""
    f = safe_finite_float(value, None)
    if f is None:
        f = default
    if f < min_v:
        return min_v
    if f > max_v:
        return max_v
    return f


def clamp_orbit_radius(v: Any) -> float:
    return clamp_positive(v, default=20.0, min_v=1.0, max_v=500.0)


def clamp_orbit_speed(v: Any) -> float:
    return clamp_positive(v, default=5.0, min_v=0.1, max_v=25.0)


def clamp_square_side(v: Any) -> float:
    return clamp_positive(v, default=10.0, min_v=1.0, max_v=200.0)


def clamp_survey_speed(v: Any) -> float:
    return clamp_positive(v, default=2.0, min_v=0.1, max_v=15.0)


def normalize_alt_z(
    cmd_alt_z: Any = None,
    cmd_alt: Any = None,
    fallback_z: float = -10.0,
) -> float:
    """NED down altitude for orbit/square (negative = above home).

    Prefer finite *cmd_alt_z*, else ``-abs(cmd_alt)`` if finite, else *fallback_z*.
    Clamp AGL to [1, 120] → z in [-120, -1].
    """
    z = safe_finite_float(cmd_alt_z, None)
    if z is None:
        alt = safe_finite_float(cmd_alt, None)
        if alt is not None:
            z = -abs(alt)
        else:
            fb = safe_finite_float(fallback_z, -10.0)
            z = fb if fb is not None else -10.0
    # Force negative altitude storage: treat positive z as "down-positive by mistake"
    if z > 0:
        z = -z
    if z == 0:
        z = -1.0
    # Clamp magnitude
    agl = abs(z)
    if agl < 1.0:
        agl = 1.0
    if agl > 120.0:
        agl = 120.0
    return -agl
