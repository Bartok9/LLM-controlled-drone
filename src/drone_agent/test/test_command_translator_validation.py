#!/usr/bin/env python3
"""Unit tests for CommandTranslator numeric validation (no live PX4 / ROS required)."""

from __future__ import annotations

import math
import sys
import types
import unittest
from unittest import mock


def _install_px4_msgs_stub():
    """Lightweight stub so command_translator can be imported without px4_msgs."""
    if 'px4_msgs' in sys.modules:
        return

    class _Msg:
        def __init__(self):
            self.timestamp = 0
            self.position = [0.0, 0.0, 0.0]
            self.yaw = float('nan')
            self.position_flag = True  # unused
            # Offboard flags
            self.position = [0.0, 0.0, 0.0]  # Trajectory only — reinited per class
            self.velocity = False
            self.acceleration = False
            self.attitude = False
            self.body_rate = False
            self.command = 0
            self.param1 = 0.0
            self.param2 = 0.0
            self.param3 = 0.0
            self.param4 = 0.0
            self.param5 = 0.0
            self.param6 = 0.0
            self.param7 = 0.0
            self.target_system = 1
            self.target_component = 1
            self.source_system = 1
            self.source_component = 1
            self.from_external = True

    class TrajectorySetpoint(_Msg):
        def __init__(self):
            super().__init__()
            self.position = [0.0, 0.0, 0.0]
            self.yaw = float('nan')

    class OffboardControlMode(_Msg):
        def __init__(self):
            super().__init__()
            self.position = True
            self.velocity = False
            self.acceleration = False
            self.attitude = False
            self.body_rate = False

    class VehicleCommand(_Msg):
        pass

    msg_mod = types.ModuleType('px4_msgs.msg')
    msg_mod.OffboardControlMode = OffboardControlMode
    msg_mod.TrajectorySetpoint = TrajectorySetpoint
    msg_mod.VehicleCommand = VehicleCommand

    pkg = types.ModuleType('px4_msgs')
    pkg.msg = msg_mod
    sys.modules['px4_msgs'] = pkg
    sys.modules['px4_msgs.msg'] = msg_mod


_install_px4_msgs_stub()

from drone_agent.command_translator import (  # noqa: E402
    CommandTranslator,
    NED_Z_MAX,
    NED_Z_MIN,
    _clamp_ned_alt_z,
    _finite_float,
)


class TestFiniteFloat(unittest.TestCase):
    def test_good(self):
        self.assertEqual(_finite_float(1.5), 1.5)
        self.assertEqual(_finite_float('2'), 2.0)

    def test_bad(self):
        self.assertIsNone(_finite_float(float('nan')))
        self.assertIsNone(_finite_float(float('inf')))
        self.assertIsNone(_finite_float('nope'))
        self.assertEqual(_finite_float(None, 9.0), 9.0)


class TestClampNed(unittest.TestCase):
    def test_in_range(self):
        self.assertEqual(_clamp_ned_alt_z(-20.0), -20.0)

    def test_too_high_agl(self):
        self.assertEqual(_clamp_ned_alt_z(-500.0), NED_Z_MIN)

    def test_too_low_agl(self):
        self.assertEqual(_clamp_ned_alt_z(-1.0), NED_Z_MAX)

    def test_positive_flipped(self):
        # positive treated as altitude AGL then negated then clamped
        self.assertEqual(_clamp_ned_alt_z(30.0), -30.0)


class TestProcessCommand(unittest.TestCase):
    def setUp(self):
        self.t = CommandTranslator()
        self.t.set_home(37.0, -122.0, 10.0)

    def test_position_ned_clamps_z(self):
        self.t.process_command({'action': 'position_ned', 'x': 1.0, 'y': 2.0, 'z': -999.0})
        self.assertEqual(self.t.target_z, NED_Z_MIN)
        self.assertEqual(self.t.target_x, 1.0)

    def test_position_ned_rejects_nan_xy(self):
        before = self.t.target_x
        self.t.process_command({'action': 'position_ned', 'x': float('nan'), 'y': 0, 'z': -10})
        self.assertEqual(self.t.target_x, before)

    def test_orbit_rejects_zero_radius(self):
        self.t.process_command(
            {'action': 'orbit', 'cx': 0, 'cy': 0, 'alt_z': -20, 'radius': 0, 'speed': 5}
        )
        self.assertFalse(self.t.orbiting)

    def test_orbit_accepts_valid(self):
        self.t.process_command(
            {'action': 'orbit', 'cx': 5, 'cy': -3, 'alt_z': -25, 'radius': 15, 'speed': 4}
        )
        self.assertTrue(self.t.orbiting)
        self.assertEqual(self.t.orbit_radius, 15.0)
        self.assertEqual(self.t.orbit_alt_z, -25.0)

    def test_square_rejects_negative_side(self):
        self.t.process_command({'action': 'square_survey', 'side': -5, 'alt_z': -15, 'speed': 2})
        self.assertFalse(self.t.square_active)

    def test_set_speed_rejects_negative(self):
        self.t.target_speed = 5.0
        self.t.process_command({'action': 'set_speed', 'speed': -1})
        self.assertEqual(self.t.target_speed, 5.0)

    def test_hold_clears_patterns(self):
        self.t.orbiting = True
        self.t.process_command({'action': 'hold'})
        self.assertFalse(self.t.orbiting)


if __name__ == '__main__':
    unittest.main()
