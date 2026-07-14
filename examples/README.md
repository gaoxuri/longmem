# Web demo (zero dependencies)

A tiny single-page demo that talks to a running LongMem API. Uses only the
Python standard library — no npm, no Streamlit, no extra packages.

```bash
# 1) start the API (default :8123)
python -m longmem.api

# 2) start the demo (default :8000)
python examples/web_demo.py --api http://localhost:8123 --port 8000

# 3) open http://localhost:8000
```

The page lets you remember memories and recall them for any user/session,
optionally filtering by `mem_type`.
