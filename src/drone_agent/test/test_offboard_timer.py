import math
import unittest

from drone_agent.offboard_timer import clamp_offboard_rate_hz, offboard_period_sec


class TestOffboardTimer(unittest.TestCase):
    def test_default_rate(self):
        self.assertEqual(clamp_offboard_rate_hz(10), 10.0)

    def test_zero_and_negative(self):
        self.assertEqual(clamp_offboard_rate_hz(0), 10.0)
        self.assertEqual(clamp_offboard_rate_hz(-3), 10.0)

    def test_non_finite(self):
        self.assertEqual(clamp_offboard_rate_hz(float("nan")), 10.0)
        self.assertEqual(clamp_offboard_rate_hz(float("inf")), 10.0)

    def test_clamp_bounds(self):
        self.assertEqual(clamp_offboard_rate_hz(0.1), 0.5)
        self.assertEqual(clamp_offboard_rate_hz(100), 50.0)

    def test_period(self):
        self.assertAlmostEqual(offboard_period_sec(10), 0.1)
        self.assertAlmostEqual(offboard_period_sec(0), 0.1)
        self.assertTrue(math.isfinite(offboard_period_sec(float("nan"))))


if __name__ == "__main__":
    unittest.main()
