#!/usr/bin/env python3
"""Offline unit tests for yolo_params (no ROS / ultralytics)."""

from drone_agent.yolo_params import clamp_confidence, clamp_skip_frames, safe_frame_dims


def test_clamp_confidence():
    assert clamp_confidence(0.7) == 0.7
    assert clamp_confidence(1.5) == 1.0
    assert clamp_confidence(0) == 0.5
    assert clamp_confidence(-1) == 0.5
    assert clamp_confidence(True) == 0.5
    assert clamp_confidence("x") == 0.5
    assert clamp_confidence(float("nan")) == 0.5


def test_clamp_skip_frames():
    assert clamp_skip_frames(3) == 3
    assert clamp_skip_frames(0) == 0
    assert clamp_skip_frames(-1) == 2
    assert clamp_skip_frames(999) == 120
    assert clamp_skip_frames(True) == 2
    assert clamp_skip_frames(2.0) == 2


def test_safe_frame_dims():
    assert safe_frame_dims(480, 640) == (480, 640)
    assert safe_frame_dims(0, 640) is None
    assert safe_frame_dims(480, -1) is None
    assert safe_frame_dims(True, 640) is None
