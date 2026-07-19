"""Sanitize Ollama model identifiers and conversation history depth."""

from __future__ import annotations

import math
import re
from typing import Any

_DEFAULT_MODEL = 'qwen2.5:32b'
_DEFAULT_HISTORY = 10
_MODEL_RE = re.compile(r'^[A-Za-z0-9._:-]+$')
_MAX_MODEL_LEN = 128


def sanitize_ollama_model(name: Any, default: str = _DEFAULT_MODEL) -> str:
    """Return a safe model tag or default.

    Rejects non-strings, empty values, path separators, spaces, and
    characters outside a conservative allowlist.
    """
    if not isinstance(default, str) or not default.strip():
        default = _DEFAULT_MODEL
    if isinstance(name, bool) or name is None:
        return default
    if not isinstance(name, str):
        return default
    cleaned = name.strip()
    if not cleaned:
        return default
    if any(sep in cleaned for sep in ('/', '\\', '\x00')):
        return default
    if not _MODEL_RE.match(cleaned):
        return default
    if len(cleaned) > _MAX_MODEL_LEN:
        cleaned = cleaned[:_MAX_MODEL_LEN]
        if not _MODEL_RE.match(cleaned):
            return default
    return cleaned


def clamp_max_history_turns(value: Any, default: int = _DEFAULT_HISTORY) -> int:
    """Clamp history turn count to [0, 50]; invalid → default (10)."""
    if isinstance(default, bool) or not isinstance(default, int):
        default = _DEFAULT_HISTORY
    if isinstance(value, bool) or value is None:
        return default
    try:
        if isinstance(value, float) and not math.isfinite(value):
            return default
        n = int(value) if isinstance(value, int) else int(float(value))
    except (TypeError, ValueError):
        return default
    if n < 0:
        return default
    return max(0, min(50, n))
