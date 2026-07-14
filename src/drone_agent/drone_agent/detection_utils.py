"""Pure helpers for YOLO → JSON detection payloads (unit-testable offline)."""

from __future__ import annotations

import math
from typing import Any, Optional


def _finite_float(value: Any) -> Optional[float]:
    try:
        num = float(value)
    except (TypeError, ValueError):
        return None
    if not math.isfinite(num):
        return None
    return num


def sanitize_detection(
    class_name: Any,
    confidence: Any,
    bbox_center: Any,
    bbox_area: Any,
) -> Optional[dict]:
    """Build a detection dict or return None if any field is unusable.

    Fail closed: non-finite numbers, empty class, or centers/areas outside [0, 1]
    after clamping only when values are finite.
    """
    if class_name is None:
        return None
    name = str(class_name).strip()
    if not name:
        return None

    conf = _finite_float(confidence)
    if conf is None:
        return None
    conf = max(0.0, min(1.0, conf))

    if not isinstance(bbox_center, (list, tuple)) or len(bbox_center) < 2:
        return None
    cx = _finite_float(bbox_center[0])
    cy = _finite_float(bbox_center[1])
    if cx is None or cy is None:
        return None
    cx = max(0.0, min(1.0, cx))
    cy = max(0.0, min(1.0, cy))

    area = _finite_float(bbox_area)
    if area is None:
        return None
    area = max(0.0, min(1.0, area))

    return {
        'class': name,
        'confidence': round(conf, 2),
        'bbox_center': [round(cx, 2), round(cy, 2)],
        'bbox_area': round(area, 4),
    }


def safe_bbox_center_x(detection: Any, default: float = 0.5) -> float:
    """Return horizontal bbox center in [0.1, 0.9] for steering, or default."""
    if not isinstance(detection, dict):
        return default
    center = detection.get('bbox_center')
    if not isinstance(center, (list, tuple)) or len(center) < 1:
        return default
    cx = _finite_float(center[0])
    if cx is None:
        return default
    return max(0.1, min(0.9, cx))
