"""Sanitize YOLO search_target class names from LLM orbit commands."""

from __future__ import annotations

import re
from typing import Any, Optional

_ALLOWED = re.compile(r"^[a-z0-9_ \-]+$")
_MAX_LEN = 64


def sanitize_target_class(value: Any) -> Optional[str]:
    """Return a safe lowercase class name, or None if unusable."""
    if value is None or isinstance(value, bool):
        return None
    if not isinstance(value, str):
        try:
            value = str(value)
        except Exception:
            return None
    s = value.strip().lower()
    if not s or len(s) > _MAX_LEN:
        return None
    if not _ALLOWED.match(s):
        return None
    return s


def matches_search_target(detection_class: Any, search_target: Any) -> bool:
    """Case-insensitive match after sanitizing both sides when possible."""
    tgt = sanitize_target_class(search_target)
    if not tgt:
        return False
    det = sanitize_target_class(detection_class)
    if det is not None:
        return det == tgt
    # Detection labels sometimes skip sanitize if slightly odd case-only
    if isinstance(detection_class, str):
        return detection_class.strip().lower() == tgt
    return False
