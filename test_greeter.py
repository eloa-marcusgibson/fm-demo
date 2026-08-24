import json
import subprocess
import sys
import unittest
from contextlib import contextmanager
from pathlib import Path

from greetings import farewell, greet, greet_all

_LANG_DIR = Path(__file__).resolve().parent / "lang"


@contextmanager
def locale_file(code, payload):
    path = _LANG_DIR / f"{code}.json"
    path.write_text(json.dumps(payload), encoding="utf-8")
    try:
        yield
    finally:
        path.unlink(missing_ok=True)


class TestFarewell(unittest.TestCase):
    def test_farewell_returns_goodbye_plus_name(self):
        self.assertEqual(farewell("crew"), "goodbye crew")

    def test_farewell_spanish(self):
        self.assertEqual(farewell("crew", "es"), "Adiós, crew, hasta luego.")

    def test_farewell_german(self):
        self.assertEqual(farewell("Ada", "de"), "tschüss Ada")

    def test_farewell_french(self):
        self.assertEqual(farewell("crew", "fr"), "Au revoir, crew !")

    def test_farewell_missing_language_fallback_to_english(self):
        self.assertEqual(farewell("crew", "en"), "goodbye crew")

    def test_farewell_unknown_language_fallback_to_english(self):
        self.assertEqual(farewell("crew", "zz"), "goodbye crew")

    def test_farewell_without_placeholder_appends_name(self):
        with locale_file("fa", {"farewell": "ciao"}):
            self.assertEqual(farewell("Ada", "fa"), "ciao Ada")

    def test_farewell_renders_literal_braces(self):
        with locale_file("fb", {"farewell": "{{bye}} {name}"}):
            self.assertEqual(farewell("Ada", "fb"), "{bye} Ada")

    def test_farewell_unbalanced_braces_raises_naming_locale(self):
        with locale_file("fu", {"farewell": "bye {name"}):
            with self.assertRaises(ValueError) as ctx:
                farewell("Ada", "fu")
        self.assertIn("fu", str(ctx.exception))

    def test_farewell_unbalanced_closing_brace_raises_naming_locale(self):
        with locale_file("fv", {"farewell": "bye name}"}):
            with self.assertRaises(ValueError) as ctx:
                farewell("Ada", "fv")
        self.assertIn("fv", str(ctx.exception))

    def test_farewell_unknown_placeholder_raises_naming_locale(self):
        with locale_file("fp", {"farewell": "age {age}"}):
            with self.assertRaises(ValueError) as ctx:
                farewell("Ada", "fp")
        self.assertIn("fp", str(ctx.exception))


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
        self.assertEqual(greet("captain", "es"), "Hola, captain!")

    def test_greet_german(self):
        self.assertEqual(greet("Ada", "de"), "hallo Ada")

    def test_greet_french(self):
        self.assertEqual(greet("captain", "fr"), "Bonjour captain !")

    def test_greet_missing_language_fallback_to_english(self):
        self.assertEqual(greet("captain", "en"), "hello captain")

    def test_greet_unknown_language_fallback_to_english(self):
        self.assertEqual(greet("captain", "zz"), "hello captain")

    def test_greet_without_placeholder_appends_name(self):
        with locale_file("ga", {"greet": "ciao"}):
            self.assertEqual(greet("Ada", "ga"), "ciao Ada")

    def test_greet_renders_literal_braces(self):
        with locale_file("gb", {"greet": "hello {{name}} -> {name}"}):
            self.assertEqual(greet("Ada", "gb"), "hello {name} -> Ada")

    def test_greet_unbalanced_braces_raises_naming_locale(self):
        with locale_file("gu", {"greet": "hello {name"}):
            with self.assertRaises(ValueError) as ctx:
                greet("Ada", "gu")
        self.assertIn("gu", str(ctx.exception))

    def test_greet_unbalanced_closing_brace_raises_naming_locale(self):
        with locale_file("gv", {"greet": "hello name}"}):
            with self.assertRaises(ValueError) as ctx:
                greet("Ada", "gv")
        self.assertIn("gv", str(ctx.exception))

    def test_greet_unknown_placeholder_raises_naming_locale(self):
        with locale_file("gp", {"greet": "age {age}"}):
            with self.assertRaises(ValueError) as ctx:
                greet("Ada", "gp")
        self.assertIn("gp", str(ctx.exception))

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
            ["Hola, captain!", "Hola, crew!"],
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
