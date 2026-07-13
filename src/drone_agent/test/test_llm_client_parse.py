#!/usr/bin/env python3
"""Unit tests for LLMClient JSON action allowlist (mocked Ollama, no network)."""

from __future__ import annotations

import json
import unittest
from unittest import mock

from drone_agent.llm_client import ALLOWED_ACTIONS, LLMClient


def _fake_urlopen_payload(payload: dict):
    body = json.dumps(payload).encode("utf-8")

    class _Resp:
        def __enter__(self):
            return self

        def __exit__(self, *args):
            return False

        def read(self):
            return body

    return _Resp()


class TestLLMClientParse(unittest.TestCase):
    def setUp(self):
        self.client = LLMClient(
            model="test-model", ollama_url="http://localhost:9", max_history_turns=3
        )

    def test_allowed_actions_match_translator_surface(self):
        for name in (
            "arm_offboard",
            "position_ned",
            "orbit",
            "square_survey",
            "hold",
            "land",
            "rtl",
        ):
            self.assertIn(name, ALLOWED_ACTIONS)

    def test_accepts_valid_action(self):
        payload = {
            "message": {
                "content": json.dumps({"action": "hold", "thought": "stop"}),
            }
        }
        with mock.patch(
            "urllib.request.urlopen", return_value=_fake_urlopen_payload(payload)
        ):
            cmd = self.client.ask("state", "stop", "[]")
        self.assertEqual(cmd["action"], "hold")

    def test_rejects_unknown_action(self):
        payload = {
            "message": {
                "content": json.dumps({"action": "velocity_body", "vx": 99}),
            }
        }
        with mock.patch(
            "urllib.request.urlopen", return_value=_fake_urlopen_payload(payload)
        ):
            with self.assertRaises(ValueError):
                self.client.ask("state", "go fast", "[]")

    def test_rejects_non_object_json(self):
        payload = {"message": {"content": "[1,2,3]"}}
        with mock.patch(
            "urllib.request.urlopen", return_value=_fake_urlopen_payload(payload)
        ):
            with self.assertRaises(ValueError):
                self.client.ask("state", "x", "[]")

    def test_rejects_empty_content(self):
        payload = {"message": {"content": ""}}
        with mock.patch(
            "urllib.request.urlopen", return_value=_fake_urlopen_payload(payload)
        ):
            with self.assertRaises(ValueError):
                self.client.ask("state", "x", "[]")


if __name__ == "__main__":
    unittest.main()
