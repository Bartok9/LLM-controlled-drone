import unittest

from drone_agent.llm_client import (
    LLMClient,
    clamp_max_history_turns,
    clamp_request_timeout_sec,
    normalize_ollama_base_url,
)


class TestNormalizeUrl(unittest.TestCase):
    def test_ok(self):
        self.assertEqual(
            normalize_ollama_base_url("http://localhost:11434/"),
            "http://localhost:11434",
        )
        self.assertEqual(
            normalize_ollama_base_url("https://example.com/v1"),
            "https://example.com/v1",
        )

    def test_reject(self):
        for bad in ("", "file:///etc", "javascript:alert(1)", "localhost:11434", "ftp://x"):
            with self.assertRaises(ValueError):
                normalize_ollama_base_url(bad)


class TestClamps(unittest.TestCase):
    def test_history(self):
        self.assertEqual(clamp_max_history_turns(True), 10)
        self.assertEqual(clamp_max_history_turns(0), 1)
        self.assertEqual(clamp_max_history_turns(999), 100)
        self.assertEqual(clamp_max_history_turns(5), 5)

    def test_timeout(self):
        self.assertEqual(clamp_request_timeout_sec(True), 30.0)
        self.assertEqual(clamp_request_timeout_sec(0.5), 1.0)
        self.assertEqual(clamp_request_timeout_sec(500), 300.0)
        self.assertEqual(clamp_request_timeout_sec(float("nan")), 30.0)


class TestClientInit(unittest.TestCase):
    def test_ctor(self):
        c = LLMClient(ollama_url="http://127.0.0.1:11434/")
        self.assertEqual(c.ollama_url, "http://127.0.0.1:11434")
        self.assertEqual(c.request_timeout_sec, 30.0)

    def test_bad_model(self):
        with self.assertRaises(ValueError):
            LLMClient(model="  ")


if __name__ == "__main__":
    unittest.main()
