import json
import subprocess
import sys
import unittest
from contextlib import contextmanager
from pathlib import Path

_LANG_DIR = Path(__file__).resolve().parent / "lang"


@contextmanager
def locale_file(code, payload):
    path = _LANG_DIR / f"{code}.json"
    path.write_text(json.dumps(payload), encoding="utf-8")
    try:
        yield
    finally:
        path.unlink(missing_ok=True)


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

    def test_greet_lang_prints_translated_line(self):
        result = run_cli("greet", "Alice", "--lang", "es")
        self.assertEqual(result.returncode, 0)
        self.assertEqual(result.stdout.strip().splitlines(), ["Hola, Alice!"])

    def test_greet_lang_de_prints_translated_line(self):
        result = run_cli("greet", "Ada", "--lang", "de")
        self.assertEqual(result.returncode, 0)
        self.assertEqual(result.stdout.strip().splitlines(), ["hallo Ada"])

    def test_greet_lang_fr_prints_translated_line(self):
        result = run_cli("greet", "Alice", "--lang", "fr")
        self.assertEqual(result.returncode, 0)
        self.assertEqual(result.stdout.strip().splitlines(), ["Bonjour Alice !"])

    def test_greet_lang_renders_literal_braces(self):
        with locale_file("gc", {"greet": "hello {{name}} -> {name}"}):
            result = run_cli("greet", "Ada", "--lang", "gc")
        self.assertEqual(result.returncode, 0)
        self.assertEqual(
            result.stdout.strip().splitlines(),
            ["hello {name} -> Ada"],
        )

    def test_greet_lang_unbalanced_braces_exits_nonzero_naming_locale(self):
        with locale_file("gd", {"greet": "hello {name"}):
            result = run_cli("greet", "Ada", "--lang", "gd")
        self.assertNotEqual(result.returncode, 0)
        self.assertIn("gd", result.stderr)

    def test_greet_lang_unknown_placeholder_exits_nonzero_naming_locale(self):
        with locale_file("ge", {"greet": "age {age}"}):
            result = run_cli("greet", "Ada", "--lang", "ge")
        self.assertNotEqual(result.returncode, 0)
        self.assertIn("ge", result.stderr)

    def test_greet_missing_username_exits_nonzero(self):
        result = run_cli("greet")
        self.assertNotEqual(result.returncode, 0)

    def test_greet_json_prints_object(self):
        result = run_cli("--json", "greet", "Alice")
        self.assertEqual(result.returncode, 0)
        payload = json.loads(result.stdout)
        self.assertIsInstance(payload, dict)
        self.assertEqual(payload, {"message": "hello Alice"})


class TestFarewellCommand(unittest.TestCase):
    def test_farewell_prints_goodbye_name(self):
        result = run_cli("farewell", "crew")
        self.assertEqual(result.returncode, 0)
        self.assertEqual(result.stdout.strip().splitlines(), ["goodbye crew"])

    def test_farewell_lang_prints_translated_line(self):
        result = run_cli("farewell", "crew", "--lang", "es")
        self.assertEqual(result.returncode, 0)
        self.assertEqual(
            result.stdout.strip().splitlines(),
            ["Adiós, crew, hasta luego."],
        )

    def test_farewell_lang_de_prints_translated_line(self):
        result = run_cli("farewell", "Ada", "--lang", "de")
        self.assertEqual(result.returncode, 0)
        self.assertEqual(result.stdout.strip().splitlines(), ["tschüss Ada"])

    def test_farewell_lang_fr_prints_translated_line(self):
        result = run_cli("farewell", "crew", "--lang", "fr")
        self.assertEqual(result.returncode, 0)
        self.assertEqual(result.stdout.strip().splitlines(), ["Au revoir, crew !"])

    def test_farewell_lang_renders_literal_braces(self):
        with locale_file("fc", {"farewell": "{{bye}} {name}"}):
            result = run_cli("farewell", "Ada", "--lang", "fc")
        self.assertEqual(result.returncode, 0)
        self.assertEqual(result.stdout.strip().splitlines(), ["{bye} Ada"])

    def test_farewell_lang_unbalanced_braces_exits_nonzero_naming_locale(self):
        with locale_file("fd", {"farewell": "bye {name"}):
            result = run_cli("farewell", "Ada", "--lang", "fd")
        self.assertNotEqual(result.returncode, 0)
        self.assertIn("fd", result.stderr)

    def test_farewell_lang_unknown_placeholder_exits_nonzero_naming_locale(self):
        with locale_file("fe", {"farewell": "age {age}"}):
            result = run_cli("farewell", "Ada", "--lang", "fe")
        self.assertNotEqual(result.returncode, 0)
        self.assertIn("fe", result.stderr)

    def test_farewell_missing_name_exits_nonzero(self):
        result = run_cli("farewell")
        self.assertNotEqual(result.returncode, 0)

    def test_farewell_json_prints_object(self):
        result = run_cli("--json", "farewell", "crew")
        self.assertEqual(result.returncode, 0)
        payload = json.loads(result.stdout)
        self.assertIsInstance(payload, dict)
        self.assertEqual(payload, {"message": "goodbye crew"})


class TestGreetAllCommand(unittest.TestCase):
    def test_greet_all_prints_one_line_per_name(self):
        result = run_cli("greet-all", "captain", "crew")
        self.assertEqual(result.returncode, 0)
        self.assertEqual(
            result.stdout.strip().splitlines(),
            ["hello captain", "hello crew"],
        )

    def test_greet_all_lang_prints_translated_lines(self):
        result = run_cli("greet-all", "captain", "crew", "--lang", "es")
        self.assertEqual(result.returncode, 0)
        self.assertEqual(
            result.stdout.strip().splitlines(),
            ["Hola, captain!", "Hola, crew!"],
        )

    def test_greet_all_missing_names_exits_nonzero(self):
        result = run_cli("greet-all")
        self.assertNotEqual(result.returncode, 0)

    def test_greet_all_json_prints_array_of_strings(self):
        result = run_cli("--json", "greet-all", "captain", "crew")
        self.assertEqual(result.returncode, 0)
        payload = json.loads(result.stdout)
        self.assertIsInstance(payload, list)
        self.assertEqual(payload, ["hello captain", "hello crew"])


class TestLangsCommand(unittest.TestCase):
    def test_langs_prints_known_codes_sorted(self):
        result = run_cli("langs")
        self.assertEqual(result.returncode, 0)
        self.assertEqual(result.stdout.strip().splitlines(), ["de", "en", "es", "fr"])


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

    def test_json_without_command_prints_smoke_block(self):
        result = run_cli("--json")
        self.assertEqual(result.returncode, 0)
        self.assertEqual(
            result.stdout.strip().splitlines(),
            ["hello captain", "goodbye crew"],
        )


if __name__ == "__main__":
    unittest.main()
