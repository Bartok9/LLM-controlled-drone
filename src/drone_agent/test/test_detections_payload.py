"""Offline unit tests for detections_payload helpers."""

from __future__ import annotations

import unittest

from drone_agent.detections_payload import (
    detection_class_names,
    parse_detections_payload,
)


class ParseDetectionsTests(unittest.TestCase):
    def test_happy_list(self):
        raw = '[{"class":"person","confidence":0.9},{"class":"car"}]'
        dets = parse_detections_payload(raw)
        self.assertEqual(len(dets), 2)
        self.assertEqual(dets[0]['class'], 'person')

    def test_empty_and_none(self):
        self.assertEqual(parse_detections_payload(None), [])
        self.assertEqual(parse_detections_payload(''), [])
        self.assertEqual(parse_detections_payload('   '), [])

    def test_invalid_json(self):
        self.assertEqual(parse_detections_payload('{not json'), [])
        self.assertEqual(parse_detections_payload(123), [])

    def test_non_list_top_level(self):
        self.assertEqual(parse_detections_payload('{"class":"person"}'), [])
        self.assertEqual(parse_detections_payload('"person"'), [])
        self.assertEqual(parse_detections_payload('42'), [])

    def test_drop_non_dict_elements(self):
        raw = '[{"class":"dog"}, "x", 1, null, {"class":"cat"}]'
        dets = parse_detections_payload(raw)
        self.assertEqual([d['class'] for d in dets], ['dog', 'cat'])

    def test_bytes(self):
        dets = parse_detections_payload(b'[{"class":"bus"}]')
        self.assertEqual(dets[0]['class'], 'bus')


class ClassNamesTests(unittest.TestCase):
    def test_extract(self):
        dets = [
            {'class': ' person '},
            {'class': ''},
            {'class': None},
            {'confidence': 0.1},
            'nope',
            {'class': True},
            {'class': 'car'},
        ]
        self.assertEqual(detection_class_names(dets), {'person', 'car'})


if __name__ == '__main__':
    unittest.main()
