"""Offline tests for search_target sanitization."""

import os
import sys
import unittest

sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

from drone_agent.search_target import matches_search_target, sanitize_target_class  # noqa: E402


class TestSanitize(unittest.TestCase):
    def test_ok(self):
        self.assertEqual(sanitize_target_class("Person"), "person")
        self.assertEqual(sanitize_target_class("  car "), "car")
        self.assertEqual(sanitize_target_class("traffic light".replace(" ", " ")), "traffic light")

    def test_reject(self):
        self.assertIsNone(sanitize_target_class(""))
        self.assertIsNone(sanitize_target_class(None))
        self.assertIsNone(sanitize_target_class(True))
        self.assertIsNone(sanitize_target_class("evil;rm -rf"))
        self.assertIsNone(sanitize_target_class("a" * 65))
        self.assertIsNone(sanitize_target_class("Foo/Bar"))


class TestMatch(unittest.TestCase):
    def test_match(self):
        self.assertTrue(matches_search_target("Person", "person"))
        self.assertTrue(matches_search_target("car", "CAR"))
        self.assertFalse(matches_search_target("dog", "cat"))
        self.assertFalse(matches_search_target("person", None))
        self.assertFalse(matches_search_target("person", "bad;drop"))


if __name__ == "__main__":
    unittest.main()
