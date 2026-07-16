#!/usr/bin/env python3
"""Offline unit tests for gps_home_guard (no ROS)."""

from drone_agent.gps_home_guard import (
    is_valid_home_fix,
    is_valid_ned_position,
    position_triple_valid,
    safe_float,
)


def test_safe_float_rejects_bool_and_nan():
    assert safe_float(True) is None
    assert safe_float(False) is None
    assert safe_float(float("nan")) is None
    assert safe_float(float("inf")) is None
    assert safe_float("nope") is None
    assert safe_float(1.5) == 1.5
    assert safe_float("2.0") == 2.0


def test_is_valid_home_fix_happy():
    assert is_valid_home_fix(37.4, -122.1, 10.0, 3) is True
    assert is_valid_home_fix(0.0, 0.0, 0.0, 3) is True


def test_is_valid_home_fix_rejects_bad_fix_or_coords():
    assert is_valid_home_fix(37.4, -122.1, 10.0, 2) is False
    assert is_valid_home_fix(37.4, -122.1, 10.0, True) is False
    assert is_valid_home_fix(91.0, 0.0, 10.0, 3) is False
    assert is_valid_home_fix(0.0, 181.0, 10.0, 3) is False
    assert is_valid_home_fix(float("nan"), 0.0, 10.0, 3) is False
    assert is_valid_home_fix(0.0, 0.0, float("inf"), 3) is False
    assert is_valid_home_fix(0.0, 0.0, True, 3) is False


def test_is_valid_ned_position():
    assert is_valid_ned_position(1.0, 2.0, -3.0) is True
    assert is_valid_ned_position(1.0, float("nan"), -3.0) is False
    assert is_valid_ned_position(True, 2.0, -3.0) is False


def test_position_triple_valid():
    assert position_triple_valid([0.0, 1.0, -2.0]) is True
    assert position_triple_valid([0.0, 1.0]) is False
    assert position_triple_valid(None) is False
