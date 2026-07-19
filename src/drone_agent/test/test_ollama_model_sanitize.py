import unittest

from drone_agent.ollama_model_sanitize import clamp_max_history_turns, sanitize_ollama_model


class TestOllamaModelSanitize(unittest.TestCase):
    def test_model_happy(self):
        self.assertEqual(sanitize_ollama_model('qwen2.5:32b'), 'qwen2.5:32b')
        self.assertEqual(sanitize_ollama_model('  llama3.2:latest  '), 'llama3.2:latest')

    def test_model_reject(self):
        self.assertEqual(sanitize_ollama_model(''), 'qwen2.5:32b')
        self.assertEqual(sanitize_ollama_model(None), 'qwen2.5:32b')
        self.assertEqual(sanitize_ollama_model(True), 'qwen2.5:32b')
        self.assertEqual(sanitize_ollama_model('../etc/passwd'), 'qwen2.5:32b')
        self.assertEqual(sanitize_ollama_model('bad model'), 'qwen2.5:32b')
        long_ok = 'a' * 200
        self.assertEqual(len(sanitize_ollama_model(long_ok)), 128)

    def test_history(self):
        self.assertEqual(clamp_max_history_turns(10), 10)
        self.assertEqual(clamp_max_history_turns(None), 10)
        self.assertEqual(clamp_max_history_turns(True), 10)
        self.assertEqual(clamp_max_history_turns(-1), 10)
        self.assertEqual(clamp_max_history_turns(100), 50)
        self.assertEqual(clamp_max_history_turns(0), 0)
        self.assertEqual(clamp_max_history_turns(3.9), 3)


if __name__ == '__main__':
    unittest.main()
