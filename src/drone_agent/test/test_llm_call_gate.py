import unittest

from drone_agent.llm_call_gate import (
    clamp_min_llm_call_interval_sec,
    safe_finite_float,
    should_allow_llm_call,
)


class TestLlmCallGate(unittest.TestCase):
    def test_safe_finite_float_rejects_bool_nan(self):
        self.assertIsNone(safe_finite_float(True))
        self.assertIsNone(safe_finite_float(float('nan')))
        self.assertEqual(safe_finite_float('2.5'), 2.5)

    def test_clamp_defaults_and_bounds(self):
        self.assertEqual(clamp_min_llm_call_interval_sec(None), 3.0)
        self.assertEqual(clamp_min_llm_call_interval_sec(0), 3.0)
        self.assertEqual(clamp_min_llm_call_interval_sec(-1), 3.0)
        self.assertEqual(clamp_min_llm_call_interval_sec(True), 3.0)
        self.assertEqual(clamp_min_llm_call_interval_sec(0.1), 0.5)
        self.assertEqual(clamp_min_llm_call_interval_sec(100), 60.0)
        self.assertEqual(clamp_min_llm_call_interval_sec(5), 5.0)

    def test_should_allow(self):
        self.assertFalse(should_allow_llm_call(10.0, 9.0, 3.0))
        self.assertTrue(should_allow_llm_call(13.0, 9.0, 3.0))
        self.assertFalse(should_allow_llm_call(float('nan'), 0.0, 3.0))


if __name__ == '__main__':
    unittest.main()
