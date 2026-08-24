# fm-demo

Scratch repo for the fm-port full-chain test.

## Usage

`greet(username, language="en", count=None)` returns a greeting string.
Non-English copy lives in one file per locale under `lang/` (for example
`lang/es.json`, `lang/fr.json`). Each file holds both `greet` and
`farewell`. A value may be a plain string or a plural object with
`one`/`other` entries. English and unknown codes fall back to the
hardcoded English word. `count=None` uses the plain string when present,
otherwise `other`; `count=1` prefers `one`; any other integer prefers
`other`.

A plural `other` (or any template) with no `{name}` still takes the
append path, so `"Adiós a todos."` renders as `Adiós a todos. Ada`. That
is intended, not a bug.

```python
from greetings import greet

print(greet("Alice"))
# hello Alice
print(greet("Alice", "es"))
# Hola, Alice!
print(greet("Alice", "fr"))
# Bonjour à tous ! Alice
print(greet("Alice", "fr", count=1))
# Bonjour Alice !
```

`farewell(name, language="en", count=None)` uses the same catalog and fallback:

```python
from greetings import farewell

print(farewell("Alice"))
# goodbye Alice
print(farewell("Alice", "es"))
# Adiós a todos. Alice
print(farewell("Alice", "es", count=1))
# Adiós, Alice.
```

`greet_all(names, language="en", count=None)` greets each name in the same
language. The CLI `--lang` and `--count` flags on `greet`, `farewell`,
and `greet-all` do the same.

### Smoke block

Run the package as a module to print the built-in smoke output:

```bash
python -m greetings
```

Expected output:

```
hello captain
goodbye crew
```
