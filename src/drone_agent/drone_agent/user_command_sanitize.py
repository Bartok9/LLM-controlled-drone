#!/usr/bin/env python3
"""Pure helpers: sanitize free-form /user_command mission text before LLM path."""

from __future__ import annotations

from typing import Any, Optional

DEFAULT_MAX_USER_COMMAND_CHARS = 2000

# Allow tab/LF/CR; drop remaining C0 controls + DEL.
_CONTROL_DROP = {chr(i) for i in range(32)} - {'\t', '\n', '\r'}
_CONTROL_DROP.add('\x7f')


def _clamp_max_chars(max_chars: Any) -> int:
    if isinstance(max_chars, bool) or max_chars is None:
        return DEFAULT_MAX_USER_COMMAND_CHARS
    try:
        n = int(max_chars)
    except (TypeError, ValueError):
        return DEFAULT_MAX_USER_COMMAND_CHARS
    if n <= 0:
        return DEFAULT_MAX_USER_COMMAND_CHARS
    # Soft upper bound so params cannot balloon memory.
    return min(n, 100_000)


def sanitize_user_command(
    raw: Any,
    max_chars: Any = DEFAULT_MAX_USER_COMMAND_CHARS,
) -> Optional[str]:
    """Return cleaned mission text, or None if empty/unusable after sanitize.

    - Non-str / None → None
    - Drop NUL and other C0 controls (keep tab/LF/CR)
    - Strip outer whitespace
    - Cut to max_chars (default 2000)
    """
    if raw is None or isinstance(raw, bool):
        return None
    if not isinstance(raw, str):
        try:
            raw = str(raw)
        except Exception:
            return None

    cleaned_chars = []
    for ch in raw:
        if ch in _CONTROL_DROP:
            continue
        cleaned_chars.append(ch)
    text = ''.join(cleaned_chars).strip()
    if not text:
        return None

    limit = _clamp_max_chars(max_chars)
    if len(text) > limit:
        text = text[:limit].rstrip()
        if not text:
            return None
    return text
