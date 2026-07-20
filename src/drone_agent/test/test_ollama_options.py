"""Unit tests for ollama_options helpers."""

import math
import sys
import unittest
from pathlib import Path

_ROOT = Path(__file__).resolve().parents[1]
if str(_ROOT) not in sys.path:
    sys.path.insert(0, str(_ROOT))

from drone_agent.ollama_options import clamp_temperature  # noqa: E402


class TestClampTemperature(unittest.TestCase):
    def test_default(self):
        self.assertEqual(clamp_temperature(None), 0.2)
        self.assertEqual(clamp_temperature("x"), 0.2)
        self.assertEqual(clamp_temperature(float("nan")), 0.2)
        self.assertEqual(clamp_temperature(float("inf")), 0.2)

    def test_range(self):
        self.assertEqual(clamp_temperature(-1), 0.0)
        self.assertEqual(clamp_temperature(3), 2.0)
        self.assertEqual(clamp_temperature(0), 0.0)
        self.assertEqual(clamp_temperature(2), 2.0)
        self.assertEqual(clamp_temperature(0.2), 0.2)

    def test_client_wire(self):
        from drone_agent.llm_client import LLMClient

        c = LLMClient(temperature=9)
        self.assertEqual(c.temperature, 2.0)
        c2 = LLMClient(temperature=float("nan"))
        self.assertEqual(c2.temperature, 0.2)


if __name__ == "__main__":
    unittest.main()
