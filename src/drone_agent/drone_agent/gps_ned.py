#!/usr/bin/env python3
"""Pure helpers: fail-closed GPS → local NED conversion."""

from __future__ import annotations

import math
from typing import Any, Optional, Tuple


def safe_float(value: Any, default: Optional[float] = None) -> Optional[float]:
    """Coerce to finite float; reject bool and non-numeric noise."""
    if value is None or isinstance(value, bool):
        return default
    try:
        num = float(value)
    except (TypeError, ValueError):
        return default
    if not math.isfinite(num):
        return default
    return num


def clamp_lat_lon(lat: Any, lon: Any) -> Optional[Tuple[float, float]]:
    """Return (lat, lon) when both are finite and inside geographic bounds."""
    lat_f = safe_float(lat)
    lon_f = safe_float(lon)
    if lat_f is None or lon_f is None:
        return None
    if not (-90.0 <= lat_f <= 90.0):
        return None
    if not (-180.0 <= lon_f <= 180.0):
        return None
    return lat_f, lon_f


def gps_to_ned(
    lat: Any,
    lon: Any,
    alt_msl: Any,
    home_lat: Any,
    home_lon: Any,
    home_alt_msl: Any,
    home_set: bool,
) -> Optional[Tuple[float, float, float]]:
    """Convert GPS WGS84 to local NED metres relative to home.

    Returns None when inputs are non-finite, out of range, or home is
    claimed set but invalid. When home_set is False and alt is finite,
    returns (0.0, 0.0, -(alt - home_alt)) matching the historical
    no-home fallback (lat/lon ignored for horizontal).
    """
    alt_f = safe_float(alt_msl)
    home_alt_f = safe_float(home_alt_msl, default=0.0)
    if alt_f is None or home_alt_f is None:
        return None

    if not home_set:
        return 0.0, 0.0, -(alt_f - home_alt_f)

    point = clamp_lat_lon(lat, lon)
    home = clamp_lat_lon(home_lat, home_lon)
    if point is None or home is None:
        return None

    lat_f, lon_f = point
    h_lat, h_lon = home
    dlat = lat_f - h_lat
    dlon = lon_f - h_lon
    north_m = dlat * 111_139.0
    east_m = dlon * 111_139.0 * math.cos(math.radians(h_lat))
    down_m = -(alt_f - home_alt_f)
    if not (math.isfinite(north_m) and math.isfinite(east_m) and math.isfinite(down_m)):
        return None
    return north_m, east_m, down_m
