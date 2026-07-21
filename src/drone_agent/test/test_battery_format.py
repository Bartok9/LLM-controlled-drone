import unittest

from drone_agent.battery_format import format_battery_line


class TestBatteryFormat(unittest.TestCase):
    def test_fraction(self):
        self.assertEqual(format_battery_line(0.87, 12.4), "Battery: 87% (12.4V)")

    def test_percent(self):
        self.assertEqual(format_battery_line(55, 11.1), "Battery: 55% (11.1V)")

    def test_nan_remaining(self):
        self.assertEqual(format_battery_line(float("nan"), 12.0), "Battery: unknown (12.0V)")

    def test_bad_voltage_omitted(self):
        self.assertEqual(format_battery_line(0.5, float("nan")), "Battery: 50%")

    def test_none(self):
        self.assertEqual(format_battery_line(None, None), "Battery: unknown")


if __name__ == "__main__":
    unittest.main()
