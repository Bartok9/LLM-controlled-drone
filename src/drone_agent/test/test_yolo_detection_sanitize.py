"""Offline tests for YOLO detection sanitization (no ultralytics)."""

import math
import unittest

from drone_agent.detection_utils import sanitize_detection, safe_bbox_center_x


class TestSanitizeDetection(unittest.TestCase):
    def test_happy_path(self):
        d = sanitize_detection("person", 0.87, [0.4, 0.6], 0.12)
        self.assertEqual(d["class"], "person")
        self.assertEqual(d["confidence"], 0.87)
        self.assertEqual(d["bbox_center"], [0.4, 0.6])
        self.assertEqual(d["bbox_area"], 0.12)

    def test_clamp_confidence_and_area(self):
        d = sanitize_detection("car", 1.5, [0.0, 1.0], -0.1)
        self.assertEqual(d["confidence"], 1.0)
        self.assertEqual(d["bbox_area"], 0.0)

    def test_reject_nan_and_empty_class(self):
        self.assertIsNone(sanitize_detection("", 0.5, [0.5, 0.5], 0.1))
        self.assertIsNone(sanitize_detection("dog", float("nan"), [0.5, 0.5], 0.1))
        self.assertIsNone(sanitize_detection("dog", 0.5, [float("inf"), 0.5], 0.1))
        self.assertIsNone(sanitize_detection("dog", 0.5, [0.5], 0.1))

    def test_safe_bbox_center_x(self):
        self.assertEqual(safe_bbox_center_x({"bbox_center": [0.02, 0.5]}), 0.1)
        self.assertEqual(safe_bbox_center_x({"bbox_center": [0.98, 0.5]}), 0.9)
        self.assertEqual(safe_bbox_center_x({"bbox_center": [float("nan"), 0.5]}), 0.5)
        self.assertEqual(safe_bbox_center_x({}), 0.5)
        self.assertTrue(math.isfinite(safe_bbox_center_x({"bbox_center": [0.3, 0.4]})))


if __name__ == "__main__":
    unittest.main()
