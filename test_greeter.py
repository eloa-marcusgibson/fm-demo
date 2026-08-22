import subprocess
import sys
import unittest

from greeter import farewell, greet


class TestFarewell(unittest.TestCase):
    def test_farewell_returns_goodbye_plus_name(self):
        self.assertEqual(farewell("crew"), "goodbye crew")


class TestMainSmoke(unittest.TestCase):
    def test_greeter_script_prints_greet_and_farewell(self):
        result = subprocess.run(
            [sys.executable, "greeter.py"],
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


if __name__ == "__main__":
    unittest.main()
