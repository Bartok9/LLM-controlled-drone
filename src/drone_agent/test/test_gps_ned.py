import math
import unittest

from drone_agent.gps_ned import clamp_lat_lon, gps_to_ned, safe_float


class TestGpsNed(unittest.TestCase):
    def test_safe_float_rejects_bool_nan(self):
        self.assertIsNone(safe_float(True))
        self.assertIsNone(safe_float(float('nan')))
        self.assertIsNone(safe_float(float('inf')))
        self.assertEqual(safe_float('1.5'), 1.5)

    def test_clamp_lat_lon_bounds(self):
        self.assertEqual(clamp_lat_lon(37.5, -122.1), (37.5, -122.1))
        self.assertIsNone(clamp_lat_lon(91.0, 0.0))
        self.assertIsNone(clamp_lat_lon(0.0, 181.0))
        self.assertIsNone(clamp_lat_lon(True, 0.0))

    def test_no_home_fallback(self):
        ned = gps_to_ned(0, 0, 120.0, 0, 0, 100.0, home_set=False)
        self.assertEqual(ned, (0.0, 0.0, -20.0))

    def test_no_home_rejects_bad_alt(self):
        self.assertIsNone(
            gps_to_ned(0, 0, float('nan'), 0, 0, 100.0, home_set=False)
        )

    def test_home_conversion_north(self):
        # 0.001 deg lat ≈ 111.139 m north
        ned = gps_to_ned(37.001, -122.0, 50.0, 37.0, -122.0, 40.0, home_set=True)
        self.assertIsNotNone(ned)
        assert ned is not None
        n, e, d = ned
        self.assertAlmostEqual(n, 0.001 * 111_139.0, places=3)
        self.assertAlmostEqual(e, 0.0, places=6)
        self.assertAlmostEqual(d, -10.0, places=6)

    def test_home_rejects_out_of_range(self):
        self.assertIsNone(
            gps_to_ned(95.0, 0.0, 10.0, 0.0, 0.0, 0.0, home_set=True)
        )
        self.assertIsNone(
            gps_to_ned(0.0, 0.0, 10.0, float('nan'), 0.0, 0.0, home_set=True)
        )

    def test_east_uses_cos_lat(self):
        home_lat = 45.0
        ned = gps_to_ned(45.0, 0.001, 0.0, 45.0, 0.0, 0.0, home_set=True)
        self.assertIsNotNone(ned)
        assert ned is not None
        n, e, d = ned
        self.assertAlmostEqual(n, 0.0, places=6)
        expected_e = 0.001 * 111_139.0 * math.cos(math.radians(home_lat))
        self.assertAlmostEqual(e, expected_e, places=3)
        self.assertAlmostEqual(d, 0.0, places=6)


if __name__ == '__main__':
    unittest.main()
