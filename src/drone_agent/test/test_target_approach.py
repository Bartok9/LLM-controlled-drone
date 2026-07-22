"""Offline unit tests for target_approach helpers."""

from __future__ import annotations

import math
import unittest

from drone_agent.target_approach import (
    clamp_approach_distance_m,
    clamp_hover_alt_z,
    safe_float,
    yaw_from_odom_quaternion,
)


class SafeFloatTests(unittest.TestCase):
    def test_ok(self):
        self.assertEqual(safe_float(1.5), 1.5)
        self.assertEqual(safe_float("2"), 2.0)

    def test_reject(self):
        self.assertIsNone(safe_float(None))
        self.assertIsNone(safe_float(True))
        self.assertIsNone(safe_float(float("nan")))
        self.assertIsNone(safe_float(float("inf")))
        self.assertIsNone(safe_float("x"))


class YawTests(unittest.TestCase):
    def test_identity_quat_yaw_zero(self):
        # w=1, x=y=z=0 → yaw 0
        y = yaw_from_odom_quaternion([1.0, 0.0, 0.0, 0.0])
        self.assertIsNotNone(y)
        self.assertAlmostEqual(y, 0.0, places=6)

    def test_90deg_about_z(self):
        # yaw ≈ π/2: w=cos(π/4), z=sin(π/4)
        w = math.cos(math.pi / 4)
        z = math.sin(math.pi / 4)
        y = yaw_from_odom_quaternion([w, 0.0, 0.0, z])
        self.assertIsNotNone(y)
        self.assertAlmostEqual(y, math.pi / 2, places=5)

    def test_bad_inputs(self):
        self.assertIsNone(yaw_from_odom_quaternion(None))
        self.assertIsNone(yaw_from_odom_quaternion([1.0, 0.0, 0.0]))
        self.assertIsNone(yaw_from_odom_quaternion([float("nan"), 0, 0, 0]))
        self.assertIsNone(yaw_from_odom_quaternion("wxyz"))


class HoverAltTests(unittest.TestCase):
    def test_fraction_with_floor(self):
        # 20 m * 0.4 = 8 → above floor 5
        self.assertAlmostEqual(clamp_hover_alt_z(20.0), -8.0)
        # 8 m * 0.4 = 3.2 → floor 5
        self.assertAlmostEqual(clamp_hover_alt_z(8.0), -5.0)

    def test_invalid(self):
        self.assertEqual(clamp_hover_alt_z(float("nan")), -5.0)
        self.assertEqual(clamp_hover_alt_z(-1.0), -5.0)
        self.assertEqual(clamp_hover_alt_z(None), -5.0)

    def test_ceiling(self):
        self.assertEqual(clamp_hover_alt_z(1000.0, fraction=0.4, max_alt_m=120.0), -120.0)


class ApproachDistTests(unittest.TestCase):
    def test_clamp_max(self):
        # 40*0.3=12 → max 8
        self.assertAlmostEqual(clamp_approach_distance_m(40.0), 8.0)
        self.assertAlmostEqual(clamp_approach_distance_m(10.0), 3.0)

    def test_invalid_zero_move(self):
        self.assertEqual(clamp_approach_distance_m(float("nan")), 0.0)
        self.assertEqual(clamp_approach_distance_m(None), 0.0)


if __name__ == "__main__":
    unittest.main()
