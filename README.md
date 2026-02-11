# manifest-fix

Quick script for fixing manifest issues now that we have more specific rules. Pretty dumb for now, but sort of useful.

## Usage

```sh
uv run main.py ~/stuff/dupon/qoc_*
```

can take multiple blobs if you want to run it against a bunch of things

then follow it up with a formatter run either `black` or `ruff`