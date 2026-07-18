import math
import unittest

from drone_agent.brain_params import (
    clamp_llm_interval_sec,
    clamp_offboard_rate_hz,
    safe_finite_float,
)


class TestSafeFiniteFloat(unittest.TestCase):
    def test_ok(self):
        self.assertEqual(safe_finite_float(3.5), 3.5)
        self.assertEqual(safe_finite_float("2"), 2.0)

    def test_reject(self):
        self.assertIsNone(safe_finite_float(True))
        self.assertIsNone(safe_finite_float(False))
        self.assertIsNone(safe_finite_float(None))
        self.assertIsNone(safe_finite_float("x"))
        self.assertIsNone(safe_finite_float(float("nan")))
        self.assertIsNone(safe_finite_float(float("inf")))
        self.assertEqual(safe_finite_float(None, 1.0), 1.0)


class TestClampLlmInterval(unittest.TestCase):
    def test_default(self):
        self.assertEqual(clamp_llm_interval_sec(None), 7.0)
        self.assertEqual(clamp_llm_interval_sec(True), 7.0)
        self.assertEqual(clamp_llm_interval_sec("bad"), 7.0)
        self.assertEqual(clamp_llm_interval_sec(float("nan")), 7.0)

    def test_bounds(self):
        self.assertEqual(clamp_llm_interval_sec(0), 1.0)
        self.assertEqual(clamp_llm_interval_sec(-1), 1.0)
        self.assertEqual(clamp_llm_interval_sec(7), 7.0)
        self.assertEqual(clamp_llm_interval_sec(200), 120.0)


class TestClampOffboardRate(unittest.TestCase):
    def test_default(self):
        self.assertEqual(clamp_offboard_rate_hz(None), 10.0)
        self.assertEqual(clamp_offboard_rate_hz(False), 10.0)
        self.assertEqual(clamp_offboard_rate_hz(float("inf")), 10.0)

    def test_bounds(self):
        self.assertEqual(clamp_offboard_rate_hz(0.5), 1.0)
        self.assertEqual(clamp_offboard_rate_hz(10), 10.0)
        self.assertEqual(clamp_offboard_rate_hz(100), 50.0)
        # Ensures period = 1/rate never divides by zero
        r = clamp_offboard_rate_hz(0)
        self.assertGreaterEqual(r, 1.0)
        self.assertTrue(math.isfinite(1.0 / r))


if __name__ == "__main__":
    unittest.main()
