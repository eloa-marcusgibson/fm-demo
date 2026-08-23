import subprocess
import sys
import unittest


def run_cli(*args):
    return subprocess.run(
        [sys.executable, "-m", "greetings", *args],
        capture_output=True,
        text=True,
        check=False,
    )


class TestGreetCommand(unittest.TestCase):
    def test_greet_prints_hello_username(self):
        result = run_cli("greet", "Alice")
        self.assertEqual(result.returncode, 0)
        self.assertEqual(result.stdout.strip().splitlines(), ["hello Alice"])

    def test_greet_missing_username_exits_nonzero(self):
        result = run_cli("greet")
        self.assertNotEqual(result.returncode, 0)


class TestFarewellCommand(unittest.TestCase):
    def test_farewell_prints_goodbye_name(self):
        result = run_cli("farewell", "crew")
        self.assertEqual(result.returncode, 0)
        self.assertEqual(result.stdout.strip().splitlines(), ["goodbye crew"])

    def test_farewell_lang_prints_translated_line(self):
        result = run_cli("farewell", "crew", "--lang", "es")
        self.assertEqual(result.returncode, 0)
        self.assertEqual(result.stdout.strip().splitlines(), ["adios crew"])

    def test_farewell_missing_name_exits_nonzero(self):
        result = run_cli("farewell")
        self.assertNotEqual(result.returncode, 0)


class TestGreetAllCommand(unittest.TestCase):
    def test_greet_all_prints_one_line_per_name(self):
        result = run_cli("greet-all", "captain", "crew")
        self.assertEqual(result.returncode, 0)
        self.assertEqual(
            result.stdout.strip().splitlines(),
            ["hello captain", "hello crew"],
        )

    def test_greet_all_missing_names_exits_nonzero(self):
        result = run_cli("greet-all")
        self.assertNotEqual(result.returncode, 0)


class TestUnknownAndSmoke(unittest.TestCase):
    def test_unknown_subcommand_exits_nonzero(self):
        result = run_cli("nonesuch")
        self.assertNotEqual(result.returncode, 0)

    def test_no_args_prints_smoke_block(self):
        result = run_cli()
        self.assertEqual(result.returncode, 0)
        self.assertEqual(
            result.stdout.strip().splitlines(),
            ["hello captain", "goodbye crew"],
        )


if __name__ == "__main__":
    unittest.main()
