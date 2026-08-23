# fm-demo

Scratch repo for the fm-port full-chain test.

## Usage

`greet(name)` returns a greeting string:

```python
from greetings import greet

print(greet("Alice"))
# hello Alice
```

`farewell(name, language="en")` returns a farewell string. Non-English
languages are loaded from `greetings_lang.json` at call time; English and
unknown codes fall back to `goodbye`:

```python
from greetings import farewell

print(farewell("Alice"))
# goodbye Alice
print(farewell("Alice", "es"))
# adios Alice
```

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
