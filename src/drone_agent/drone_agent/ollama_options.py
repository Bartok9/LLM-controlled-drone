"""Fail-closed Ollama chat option sanitizers."""

from __future__ import annotations

import math
from typing import Union

Number = Union[int, float]

_DEFAULT_TEMPERATURE = 0.2
_TEMP_MIN = 0.0
_TEMP_MAX = 2.0


def clamp_temperature(
    value: object,
    default: float = _DEFAULT_TEMPERATURE,
) -> float:
    """Clamp Ollama sampling temperature to [0.0, 2.0].

    Invalid, missing, or non-finite values return *default* (0.2).
    """
    if value is None:
        return float(default)
    try:
        num = float(value)  # type: ignore[arg-type]
    except (TypeError, ValueError):
        return float(default)
    if not math.isfinite(num):
        return float(default)
    return max(_TEMP_MIN, min(_TEMP_MAX, num))
