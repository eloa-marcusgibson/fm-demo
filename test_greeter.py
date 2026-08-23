import subprocess
import sys
import unittest

from greetings import farewell, greet, greet_all


class TestFarewell(unittest.TestCase):
    def test_farewell_returns_goodbye_plus_name(self):
        self.assertEqual(farewell("crew"), "goodbye crew")

    def test_farewell_spanish(self):
        self.assertEqual(farewell("crew", "es"), "adios crew")

    def test_farewell_missing_language_fallback_to_english(self):
        self.assertEqual(farewell("crew", "en"), "goodbye crew")

    def test_farewell_unknown_language_fallback_to_english(self):
        self.assertEqual(farewell("crew", "de"), "goodbye crew")


class TestMainSmoke(unittest.TestCase):
    def test_greetings_module_prints_greet_and_farewell(self):
        result = subprocess.run(
            [sys.executable, "-m", "greetings"],
            capture_output=True,
            text=True,
            check=False,
        )
        self.assertEqual(result.returncode, 0)
        self.assertEqual(
            result.stdout.strip().splitlines(),
            ["hello captain", "goodbye crew"],
        )


class TestGreet(unittest.TestCase):
    def test_greet_unchanged(self):
        self.assertEqual(greet("captain"), "hello captain")

    def test_greet_accepts_username_keyword(self):
        self.assertEqual(greet(username="captain"), "hello captain")

    def test_greet_spanish(self):
        self.assertEqual(greet("captain", "es"), "hola captain")

    def test_greet_missing_language_fallback_to_english(self):
        self.assertEqual(greet("captain", "en"), "hello captain")

    def test_greet_unknown_language_fallback_to_english(self):
        self.assertEqual(greet("captain", "de"), "hello captain")

    def test_greet_rejects_int_username(self):
        with self.assertRaises(ValueError) as ctx:
            greet(42)
        self.assertIn("str", str(ctx.exception).lower())

    def test_greet_rejects_none_username(self):
        with self.assertRaises(ValueError) as ctx:
            greet(None)
        self.assertIn("str", str(ctx.exception).lower())

    def test_greet_rejects_bytes_username(self):
        with self.assertRaises(ValueError) as ctx:
            greet(b"captain")
        self.assertIn("str", str(ctx.exception).lower())


class TestGreetAll(unittest.TestCase):
    def test_greet_all_returns_greetings_for_each_name(self):
        self.assertEqual(
            greet_all(["captain", "crew"]),
            ["hello captain", "hello crew"],
        )

    def test_greet_all_spanish(self):
        self.assertEqual(
            greet_all(["captain", "crew"], "es"),
            ["hola captain", "hola crew"],
        )

    def test_greet_all_empty_list(self):
        self.assertEqual(greet_all([]), [])

    def test_greet_all_rejects_int_entry(self):
        with self.assertRaises(ValueError) as ctx:
            greet_all(["captain", 42])
        self.assertIn("str", str(ctx.exception).lower())

    def test_greet_all_rejects_none_entry(self):
        with self.assertRaises(ValueError) as ctx:
            greet_all(["captain", None])
        self.assertIn("str", str(ctx.exception).lower())

    def test_greet_all_rejects_bytes_entry(self):
        with self.assertRaises(ValueError) as ctx:
            greet_all(["captain", b"crew"])
        self.assertIn("str", str(ctx.exception).lower())

if __name__ == "__main__":
    unittest.main()
