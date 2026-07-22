"""Fail-closed parse of YOLO detection JSON consumed by BrainNode."""

from __future__ import annotations

import json
from typing import Any, Iterable, List, Set


def parse_detections_payload(raw: Any) -> List[dict]:
    """Parse YOLO detections JSON into a list of dicts only.

    Fail closed:
    - None / empty → []
    - invalid JSON → []
    - non-list top-level JSON → []
    - non-dict elements dropped
    """
    if raw is None:
        return []
    if isinstance(raw, (bytes, bytearray)):
        try:
            raw = raw.decode('utf-8')
        except UnicodeDecodeError:
            return []
    if not isinstance(raw, str):
        return []
    text = raw.strip()
    if not text:
        return []
    try:
        data = json.loads(text)
    except (json.JSONDecodeError, TypeError, ValueError):
        return []
    if not isinstance(data, list):
        return []
    out: List[dict] = []
    for item in data:
        if isinstance(item, dict):
            out.append(item)
    return out


def detection_class_names(detections: Iterable[Any]) -> Set[str]:
    """Extract non-empty class name strings from detection dicts."""
    names: Set[str] = set()
    for det in detections:
        if not isinstance(det, dict):
            continue
        cls = det.get('class')
        if cls is None or isinstance(cls, bool):
            continue
        name = str(cls).strip()
        if name:
            names.add(name)
    return names
