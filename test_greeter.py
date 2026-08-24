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
        self.assertEqual(farewell("crew", "es"), "Adiós a todos. crew")

    def test_farewell_spanish_count_one(self):
        self.assertEqual(farewell("crew", "es", count=1), "Adiós, crew.")

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

    def test_farewell_plural_count_one_uses_one_entry(self):
        with locale_file("q1", {"farewell": {"one": "Adiós, {name}.", "other": "Adiós a todos."}}):
            self.assertEqual(farewell("Ada", "q1", count=1), "Adiós, Ada.")

    def test_farewell_plural_count_five_uses_other_entry(self):
        with locale_file("q2", {"farewell": {"one": "Adiós, {name}.", "other": "Adiós a todos."}}):
            self.assertEqual(farewell("Ada", "q2", count=5), "Adiós a todos. Ada")


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

    def test_greet_english_count_does_not_change_append(self):
        self.assertEqual(greet("captain", count=1), "hello captain")
        self.assertEqual(greet("captain", count=5), "hello captain")

    def test_greet_accepts_username_keyword(self):
        self.assertEqual(greet(username="captain"), "hello captain")

    def test_greet_spanish(self):
        self.assertEqual(greet("captain", "es"), "Hola, captain!")

    def test_greet_german(self):
        self.assertEqual(greet("Ada", "de"), "hallo Ada")

    def test_greet_french(self):
        self.assertEqual(greet("captain", "fr"), "Bonjour à tous ! captain")

    def test_greet_french_count_one(self):
        self.assertEqual(greet("captain", "fr", count=1), "Bonjour captain !")

    def test_greet_missing_language_fallback_to_english(self):
        self.assertEqual(greet("captain", "en"), "hello captain")

    def test_greet_unknown_language_fallback_to_english(self):
        self.assertEqual(greet("captain", "zz"), "hello captain")

    def test_greet_unknown_language_count_still_falls_back(self):
        self.assertEqual(greet("captain", "zz", count=1), "hello captain")

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

    def test_greet_plural_count_one_uses_one_entry(self):
        with locale_file("p1", {"greet": {"one": "Hola {name}!", "other": "Hola a todos, {name}s!"}}):
            self.assertEqual(greet("Ada", "p1", count=1), "Hola Ada!")

    def test_greet_plural_count_five_uses_other_entry(self):
        with locale_file("p2", {"greet": {"one": "Hola {name}!", "other": "Hola a todos, {name}s!"}}):
            self.assertEqual(greet("Ada", "p2", count=5), "Hola a todos, Adas!")

    def test_greet_plural_count_none_uses_other_entry(self):
        with locale_file("p3", {"greet": {"one": "Hola {name}!", "other": "Hola a todos, {name}s!"}}):
            self.assertEqual(greet("Ada", "p3"), "Hola a todos, Adas!")

    def test_greet_string_count_none_uses_plain_string(self):
        with locale_file("p4", {"greet": "ciao {name}"}):
            self.assertEqual(greet("Ada", "p4"), "ciao Ada")

    def test_greet_plural_missing_one_falls_to_other(self):
        with locale_file("p5", {"greet": {"other": "Hola a todos, {name}s!"}}):
            self.assertEqual(greet("Ada", "p5", count=1), "Hola a todos, Adas!")

    def test_greet_plain_string_used_when_other_absent(self):
        with locale_file("p6", {"greet": "ciao {name}"}):
            self.assertEqual(greet("Ada", "p6", count=5), "ciao Ada")

    def test_greet_plural_neither_one_nor_other_raises_naming_locale(self):
        with locale_file("p7", {"greet": {"one": "Hola {name}!"}}):
            with self.assertRaises(ValueError) as ctx:
                greet("Ada", "p7")
        self.assertIn("p7", str(ctx.exception))

    def test_greet_non_int_count_raises_value_error(self):
        with self.assertRaises(ValueError):
            greet("Ada", count=1.5)

    def test_greet_plural_entry_renders_literal_braces(self):
        with locale_file("p8", {"greet": {"one": "hello {{name}} -> {name}", "other": "hi"}}):
            self.assertEqual(greet("Ada", "p8", count=1), "hello {name} -> Ada")

    def test_greet_plural_unknown_placeholder_raises_naming_locale(self):
        with locale_file("p9", {"greet": {"one": "age {age}", "other": "hi {name}"}}):
            with self.assertRaises(ValueError) as ctx:
                greet("Ada", "p9", count=1)
        self.assertIn("p9", str(ctx.exception))

    def test_greet_plural_invalid_unused_entry_still_raises_naming_locale(self):
        with locale_file("p0", {"greet": {"one": "age {age}", "other": "hi {name}"}}):
            with self.assertRaises(ValueError) as ctx:
                greet("Ada", "p0", count=5)
        self.assertIn("p0", str(ctx.exception))


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

    def test_greet_all_plural_count_one_uses_one_entry(self):
        with locale_file("r1", {"greet": {"one": "Hola {name}!", "other": "Hola a todos, {name}s!"}}):
            self.assertEqual(
                greet_all(["Ada", "Bo"], "r1", count=1),
                ["Hola Ada!", "Hola Bo!"],
            )

    def test_greet_all_plural_count_five_uses_other_entry(self):
        with locale_file("r2", {"greet": {"one": "Hola {name}!", "other": "Hola a todos, {name}s!"}}):
            self.assertEqual(
                greet_all(["Ada"], "r2", count=5),
                ["Hola a todos, Adas!"],
            )

if __name__ == "__main__":
    unittest.main()
