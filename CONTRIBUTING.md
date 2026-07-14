# Contributing to LongMem

Thanks for your interest in improving LongMem! This project is intentionally
small and dependency-light. A few guidelines keep it that way.

## Setup

```bash
python -m venv .venv && . .venv/bin/activate
pip install -e ".[dev]"
# You need PostgreSQL + pgvector. The fastest path is:
#   docker compose up -d db
# Point the CLI/API at it via .env (see .env.example).
```

## Running the tests

```bash
pytest
```

Tests talk to a real PostgreSQL + pgvector instance (configured via env vars).
They create and clean up their own rows under the `test_user` namespace.

## Principles

- **Keep it dependency-light.** Pure `stdlib` + `psycopg2` + `fastapi` are the
  only hard runtime deps. Prefer the local fallback embedding over pulling in
  heavy ML libs.
- **Zero-key demo.** The default embedding must run with no API key.
- **Backward compatible.** New params default to old behavior.
- **Tests first.** Any new store/API behavior needs a test in `tests/`.

## Pull requests

1. Fork and branch from `main`.
2. Add a test for the change.
3. Run `pytest`.
4. Bump the version in `pyproject.toml` + `longmem/__init__.py` + `api.py`
   for user-facing changes.
5. Open the PR with a short description of the "why".

## Reporting bugs

Open an issue with: what you did, expected vs actual, and your env
(PostgreSQL version, embedding provider, Python version).
