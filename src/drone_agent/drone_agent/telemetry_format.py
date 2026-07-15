#!/usr/bin/env python3
"""Pure helpers to format telemetry strings for LLM prompts (no ROS imports)."""

from __future__ import annotations

from typing import Any, Mapping, Optional, Sequence


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
    if num != num or num in (float("inf"), float("-inf")):  # nan/inf
        return default
    import math

    if not math.isfinite(num):
        return default
    return num


def _triple_finite(seq: Any) -> Optional[tuple[float, float, float]]:
    if seq is None:
        return None
    try:
        a, b, c = seq[0], seq[1], seq[2]
    except (TypeError, IndexError, KeyError):
        return None
    fa, fb, fc = safe_float(a), safe_float(b), safe_float(c)
    if fa is None or fb is None or fc is None:
        return None
    return fa, fb, fc


def format_drone_state_lines(
    *,
    gps: Any = None,
    odometry: Any = None,
    battery: Any = None,
    vehicle_status: Any = None,
    translator_snapshot: Optional[Mapping[str, Any]] = None,
    armed: bool = False,
    search_target: Optional[str] = None,
) -> list[str]:
    """Build human-readable telemetry lines. Never raises on bad fields."""
    lines: list[str] = []

    if gps is not None:
        lat = safe_float(getattr(gps, "latitude_deg", None))
        lon = safe_float(getattr(gps, "longitude_deg", None))
        alt = safe_float(getattr(gps, "altitude_msl_m", None))
        fix = getattr(gps, "fix_type", None)
        fix_i = None
        if not isinstance(fix, bool):
            try:
                fix_i = int(fix)
            except (TypeError, ValueError):
                fix_i = None
        if lat is not None and lon is not None and alt is not None and fix_i is not None:
            lines.append(
                f"GPS: lat={lat:.6f}, lon={lon:.6f}, alt={alt:.1f}m MSL, fix={fix_i}"
            )
        else:
            lines.append("GPS: unavailable fields")
    else:
        lines.append("GPS: No fix")

    if odometry is not None:
        pos = _triple_finite(getattr(odometry, "position", None))
        vel = _triple_finite(getattr(odometry, "velocity", None))
        if pos is not None:
            lines.append(
                f"Local position (NED): x={pos[0]:.1f}m, y={pos[1]:.1f}m, z={pos[2]:.1f}m"
            )
        else:
            lines.append("Odometry: invalid/non-finite")
        if vel is not None:
            lines.append(
                f"Velocity (NED): vx={vel[0]:.1f}, vy={vel[1]:.1f}, vz={vel[2]:.1f} m/s"
            )
        elif pos is not None:
            lines.append("Velocity (NED): unavailable")
    else:
        lines.append("Odometry: Not available")

    if battery is not None:
        rem = safe_float(getattr(battery, "remaining", None))
        volts = safe_float(getattr(battery, "voltage_v", None))
        if rem is not None and volts is not None:
            pct = max(0.0, min(100.0, rem * 100.0))
            lines.append(f"Battery: {pct:.0f}% ({volts:.1f}V)")
        else:
            lines.append("Battery: unknown")
    # omit battery line when no battery msg (matches prior style loosely)

    if vehicle_status is not None:
        arm_state = getattr(vehicle_status, "arming_state", None)
        nav = getattr(vehicle_status, "nav_state", None)
        try:
            arm_s = int(arm_state) if not isinstance(arm_state, bool) else arm_state
        except (TypeError, ValueError):
            arm_s = arm_state
        try:
            nav_s = int(nav) if not isinstance(nav, bool) else nav
        except (TypeError, ValueError):
            nav_s = nav
        lines.append(f"Armed: {armed} (from vehicle_status arming_state={arm_s})")
        lines.append(f"Nav state: {nav_s}")
    else:
        lines.append(
            f"Armed: {armed} (vehicle_status not received — inferred from altitude)"
        )

    snap = translator_snapshot or {}
    home_set = bool(snap.get("home_set", False))
    if home_set:
        hlat = safe_float(snap.get("home_lat"), 0.0) or 0.0
        hlon = safe_float(snap.get("home_lon"), 0.0) or 0.0
        halt = safe_float(snap.get("home_alt"), 0.0) or 0.0
        lines.append(
            f"Home GPS (NED origin): lat={hlat:.6f}, lon={hlon:.6f}, alt={halt:.1f}m MSL"
        )
    else:
        lines.append("Home GPS: not set yet")

    orbiting = bool(snap.get("orbiting", False))
    lines.append(f"Orbiting: {orbiting}")
    if search_target:
        lines.append(f'Search mode: actively scanning for "{search_target}"')

    tx = safe_float(snap.get("target_x"), 0.0) or 0.0
    ty = safe_float(snap.get("target_y"), 0.0) or 0.0
    tz = safe_float(snap.get("target_z"), 0.0) or 0.0
    lines.append(f"Current target (NED): x={tx:.1f}, y={ty:.1f}, z={tz:.1f}")

    return lines
