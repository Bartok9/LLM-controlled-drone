"""Unit tests for square_params helpers."""

import math
import sys
import unittest
from pathlib import Path

# Allow imports without installing the package.
_ROOT = Path(__file__).resolve().parents[1]
if str(_ROOT) not in sys.path:
    sys.path.insert(0, str(_ROOT))

from drone_agent.square_params import clamp_square_threshold_m, finite_ned_xyz  # noqa: E402


class TestClampSquareThreshold(unittest.TestCase):
    def test_default_none(self):
        self.assertEqual(clamp_square_threshold_m(None), 1.0)

    def test_invalid(self):
        self.assertEqual(clamp_square_threshold_m("x"), 1.0)
        self.assertEqual(clamp_square_threshold_m(float("nan")), 1.0)
        self.assertEqual(clamp_square_threshold_m(float("inf")), 1.0)

    def test_clamp_range(self):
        self.assertEqual(clamp_square_threshold_m(0.01), 0.1)
        self.assertEqual(clamp_square_threshold_m(100), 50.0)
        self.assertEqual(clamp_square_threshold_m(2.5), 2.5)

    def test_custom_default(self):
        self.assertEqual(clamp_square_threshold_m(None, default=3.0), 3.0)


class TestFiniteNedXyz(unittest.TestCase):
    def test_ok(self):
        self.assertEqual(finite_ned_xyz(1, 2, -3), (1.0, 2.0, -3.0))

    def test_nan(self):
        self.assertIsNone(finite_ned_xyz(float("nan"), 0, 0))
        self.assertIsNone(finite_ned_xyz(0, float("inf"), 0))

    def test_bad_type(self):
        self.assertIsNone(finite_ned_xyz("a", 0, 0))
        self.assertIsNone(finite_ned_xyz(None, 1, 2))


class TestUpdatePositionGuard(unittest.TestCase):
    def test_semicolon_early_return(self):
        try:
            import px4_msgs  # noqa: F401
        except ImportError:
            self.skipTest("px4_msgs not installed")
        from drone_agent.command_translator import CommandTranslator

        t = CommandTranslator()
        t.square_active = True
        t.square_waypoints = [(0.0, 0.0), (1.0, 0.0)]
        t.square_wp_index = 0
        t.square_threshold = 1.0
        t.update_position(float("nan"), 0.0, -10.0)
        self.assertEqual(t.square_wp_index, 0)


if __name__ == "__main__":
    unittest.main()
