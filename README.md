# fm-demo

Scratch repo for the fm-port full-chain test.

## Usage

`greet(username, language="en")` returns a greeting string. Non-English
copy lives in one file per locale under `lang/` (for example
`lang/es.json`, `lang/fr.json`). Each file holds both `greet` and
`farewell`. English and unknown codes fall back to the hardcoded English
word:

```python
from greetings import greet

print(greet("Alice"))
# hello Alice
print(greet("Alice", "es"))
# Hola, Alice!
```

`farewell(name, language="en")` uses the same catalog and fallback:

```python
from greetings import farewell

print(farewell("Alice"))
# goodbye Alice
print(farewell("Alice", "es"))
# Adiós, Alice, hasta luego.
```

`greet_all(names, language="en")` greets each name in the same language.
The CLI `--lang` flag on `greet`, `farewell`, and `greet-all` does the same.

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
