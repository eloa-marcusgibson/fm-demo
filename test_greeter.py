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


class TestGreetAll(unittest.TestCase):
    def test_greet_all_returns_greetings_for_each_name(self):
        self.assertEqual(
            greet_all(["captain", "crew"]),
            ["hello captain", "hello crew"],
        )

    def test_greet_all_empty_list(self):
        self.assertEqual(greet_all([]), [])

if __name__ == "__main__":
    unittest.main()
