import math
import unittest
from types import SimpleNamespace

from drone_agent.telemetry_format import format_drone_state_lines, safe_float


class TestSafeFloat(unittest.TestCase):
    def test_ok(self):
        self.assertEqual(safe_float(1.5), 1.5)
        self.assertEqual(safe_float("2"), 2.0)

    def test_reject(self):
        self.assertIsNone(safe_float(True))
        self.assertIsNone(safe_float(float("nan")))
        self.assertIsNone(safe_float(float("inf")))
        self.assertIsNone(safe_float("nope"))
        self.assertEqual(safe_float(None, 3.0), 3.0)


class TestFormat(unittest.TestCase):
    def test_empty(self):
        lines = format_drone_state_lines()
        self.assertTrue(any("GPS: No fix" in L for L in lines))
        self.assertTrue(any("Odometry: Not available" in L for L in lines))

    def test_nan_odom(self):
        odom = SimpleNamespace(position=(float("nan"), 0.0, -10.0), velocity=(0, 0, 0))
        lines = format_drone_state_lines(odometry=odom)
        self.assertTrue(any("invalid/non-finite" in L for L in lines))

    def test_good_paths(self):
        gps = SimpleNamespace(latitude_deg=1.0, longitude_deg=2.0, altitude_msl_m=10.0, fix_type=3)
        odom = SimpleNamespace(position=(1.0, 2.0, -10.0), velocity=(0.1, 0.0, 0.0))
        bat = SimpleNamespace(remaining=0.5, voltage_v=12.3)
        vs = SimpleNamespace(arming_state=2, nav_state=14)
        snap = {
            "home_set": True,
            "home_lat": 1.0,
            "home_lon": 2.0,
            "home_alt": 10.0,
            "orbiting": False,
            "target_x": 0.0,
            "target_y": 0.0,
            "target_z": -10.0,
        }
        lines = format_drone_state_lines(
            gps=gps,
            odometry=odom,
            battery=bat,
            vehicle_status=vs,
            translator_snapshot=snap,
            armed=True,
            search_target="person",
        )
        joined = "\n".join(lines)
        self.assertIn("GPS: lat=", joined)
        self.assertIn("Battery: 50%", joined)
        self.assertIn('scanning for "person"', joined)

    def test_battery_clamp(self):
        bat = SimpleNamespace(remaining=1.5, voltage_v=11.0)  # over 100%
        lines = format_drone_state_lines(battery=bat)
        self.assertTrue(any("Battery: 100%" in L for L in lines))


if __name__ == "__main__":
    unittest.main()
