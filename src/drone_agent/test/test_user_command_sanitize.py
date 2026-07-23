import unittest

from drone_agent.user_command_sanitize import (
    DEFAULT_MAX_USER_COMMAND_CHARS,
    sanitize_user_command,
)


class TestUserCommandSanitize(unittest.TestCase):
    def test_empty_and_none(self):
        self.assertIsNone(sanitize_user_command(None))
        self.assertIsNone(sanitize_user_command(''))
        self.assertIsNone(sanitize_user_command('   \n\t  '))
        self.assertIsNone(sanitize_user_command(True))

    def test_strips_controls_keeps_text(self):
        raw = 'Fly\x00 north\x07 please'
        self.assertEqual(sanitize_user_command(raw), 'Fly north please')

    def test_keeps_tabs_newlines(self):
        raw = 'line1\nline2\tgo'
        self.assertEqual(sanitize_user_command(raw), 'line1\nline2\tgo')

    def test_cuts_long(self):
        long = 'a' * 5000
        out = sanitize_user_command(long, max_chars=100)
        self.assertIsNotNone(out)
        self.assertEqual(len(out), 100)

    def test_default_max(self):
        long = 'b' * (DEFAULT_MAX_USER_COMMAND_CHARS + 50)
        out = sanitize_user_command(long)
        self.assertIsNotNone(out)
        self.assertEqual(len(out), DEFAULT_MAX_USER_COMMAND_CHARS)

    def test_bad_max_uses_default(self):
        long = 'c' * (DEFAULT_MAX_USER_COMMAND_CHARS + 10)
        out = sanitize_user_command(long, max_chars=0)
        self.assertIsNotNone(out)
        self.assertEqual(len(out), DEFAULT_MAX_USER_COMMAND_CHARS)
        out2 = sanitize_user_command(long, max_chars=True)
        self.assertIsNotNone(out2)
        self.assertEqual(len(out2), DEFAULT_MAX_USER_COMMAND_CHARS)

    def test_normal_passthrough(self):
        self.assertEqual(
            sanitize_user_command('  Hover at 20m and watch  '),
            'Hover at 20m and watch',
        )


if __name__ == '__main__':
    unittest.main()
