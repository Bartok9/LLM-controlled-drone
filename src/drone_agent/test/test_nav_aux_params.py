import unittest

from drone_agent.nav_aux_params import (
    clamp_heading_deg,
    clamp_target_speed_mps,
    safe_finite_float,
    safe_gps_coord,
)


class TestSafeFinite(unittest.TestCase):
    def test_reject_bool(self):
        self.assertIsNone(safe_finite_float(True))
        self.assertIsNone(safe_finite_float(False))


class TestSpeed(unittest.TestCase):
    def test_default_and_bounds(self):
        self.assertEqual(clamp_target_speed_mps(None), 5.0)
        self.assertEqual(clamp_target_speed_mps(True), 5.0)
        self.assertEqual(clamp_target_speed_mps(0), 0.1)
        self.assertEqual(clamp_target_speed_mps(-3), 0.1)
        self.assertEqual(clamp_target_speed_mps(3.5), 3.5)
        self.assertEqual(clamp_target_speed_mps(100), 25.0)
        self.assertEqual(clamp_target_speed_mps(float("nan")), 5.0)


class TestHeading(unittest.TestCase):
    def test_default_and_norm(self):
        self.assertEqual(clamp_heading_deg(None), 0.0)
        self.assertEqual(clamp_heading_deg("x"), 0.0)
        self.assertAlmostEqual(clamp_heading_deg(0), 0.0)
        self.assertAlmostEqual(clamp_heading_deg(90), 90.0)
        self.assertAlmostEqual(clamp_heading_deg(180), 180.0)
        self.assertAlmostEqual(clamp_heading_deg(-180), 180.0)
        self.assertAlmostEqual(clamp_heading_deg(270), -90.0)
        self.assertAlmostEqual(clamp_heading_deg(540), 180.0)


class TestGps(unittest.TestCase):
    def test_ok(self):
        self.assertEqual(safe_gps_coord(37.5, -122.1, 10.0), (37.5, -122.1, 10.0))

    def test_defaults_and_clamp(self):
        self.assertEqual(
            safe_gps_coord(None, None, None, default_lat=1.0, default_lon=2.0, default_alt=3.0),
            (1.0, 2.0, 3.0),
        )
        lat, lon, alt = safe_gps_coord(99, -200, True)
        self.assertEqual(lat, 90.0)
        self.assertEqual(lon, -180.0)
        self.assertEqual(alt, 0.0)

    def test_bool_lat(self):
        lat, lon, alt = safe_gps_coord(True, 10, 5)
        self.assertEqual(lat, 0.0)
        self.assertEqual(lon, 10.0)
        self.assertEqual(alt, 5.0)


if __name__ == "__main__":
    unittest.main()
