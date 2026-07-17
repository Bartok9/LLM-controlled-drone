"""Offline unit tests for orbit_geometry helpers."""

import os
import sys
import unittest

sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

from drone_agent.orbit_geometry import (  # noqa: E402
    clamp_orbit_radius,
    clamp_orbit_speed,
    clamp_square_side,
    clamp_survey_speed,
    normalize_alt_z,
    safe_finite_float,
)


class TestSafeFiniteFloat(unittest.TestCase):
    def test_ok(self):
        self.assertEqual(safe_finite_float(3.5), 3.5)
        self.assertEqual(safe_finite_float("2"), 2.0)

    def test_reject(self):
        self.assertIsNone(safe_finite_float(True))
        self.assertIsNone(safe_finite_float(False))
        self.assertIsNone(safe_finite_float(float("nan")))
        self.assertIsNone(safe_finite_float(float("inf")))
        self.assertIsNone(safe_finite_float("nope"))
        self.assertEqual(safe_finite_float(None, 1.0), 1.0)


class TestClamps(unittest.TestCase):
    def test_radius(self):
        self.assertEqual(clamp_orbit_radius(20), 20.0)
        self.assertEqual(clamp_orbit_radius(0), 1.0)
        self.assertEqual(clamp_orbit_radius(-5), 1.0)
        self.assertEqual(clamp_orbit_radius(9999), 500.0)
        self.assertEqual(clamp_orbit_radius(None), 20.0)
        self.assertEqual(clamp_orbit_radius(True), 20.0)

    def test_orbit_speed(self):
        self.assertEqual(clamp_orbit_speed(5), 5.0)
        self.assertEqual(clamp_orbit_speed(0), 0.1)
        self.assertEqual(clamp_orbit_speed(100), 25.0)

    def test_square(self):
        self.assertEqual(clamp_square_side(10), 10.0)
        self.assertEqual(clamp_square_side(0.5), 1.0)
        self.assertEqual(clamp_square_side(500), 200.0)
        self.assertEqual(clamp_survey_speed(2), 2.0)
        self.assertEqual(clamp_survey_speed(0), 0.1)
        self.assertEqual(clamp_survey_speed(99), 15.0)


class TestNormalizeAltZ(unittest.TestCase):
    def test_prefer_alt_z(self):
        self.assertEqual(normalize_alt_z(cmd_alt_z=-40.0), -40.0)

    def test_legacy_alt(self):
        self.assertEqual(normalize_alt_z(cmd_alt=25.0), -25.0)

    def test_clamp_and_fallback(self):
        self.assertEqual(normalize_alt_z(cmd_alt_z=-200.0), -120.0)
        self.assertEqual(normalize_alt_z(cmd_alt_z=0.0), -1.0)
        self.assertEqual(normalize_alt_z(fallback_z=-12.0), -12.0)
        self.assertEqual(normalize_alt_z(cmd_alt_z=True, fallback_z=-8.0), -8.0)


if __name__ == "__main__":
    unittest.main()
