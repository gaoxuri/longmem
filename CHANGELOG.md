# Changelog

All notable changes to LongMem are documented here.

## [0.2.4] — TTL auto-purge
- `POST /purge` endpoint (alias of `/forget/expired`) hard-deletes expired memories.
- CLI `longmem purge --once` and `longmem purge --interval N` (daemon loop).
- `docker-compose.yml`: new `purger` service that cleans expired memories every 60s.
- `CONTRIBUTING.md` added.

## [0.2.3] — Web demo
- `examples/web_demo.py` + `examples/static/index.html`: zero-dependency web UI
  that talks to a running LongMem API (stdlib `http.server`, no npm/Streamlit).
- `examples/README.md`.

## [0.2.2] — Recall filtering
- `recall` accepts `type_filter` (narrow by `mem_type`) and `recency_bias`
  (0..1, blend cosine score with recency so fresher memories rank higher).
- Backward compatible: omit both → identical to old behavior.

## [0.2.1] — Update endpoint
- `PUT /memory/{id}`: patch content (re-embed), `mem_type`, `ttl_seconds`.
- `DELETE /memory/{id}` kept for removal.
- SDK `Memory.update(...)`.

## [0.2.0] — Batch + TTL
- `POST /remember/batch`: write many memories in one request.
- Per-memory `ttl_seconds`; expired memories are filtered from recall/list.
- `POST /forget/expired`: hard-delete expired memories.
- SDK `Memory.remember(ttl_seconds=)` and `Memory.remember_batch()`.
- `init_db()` is idempotent (backfills `ttl_seconds` for existing deployments).

## [0.1.0] — Initial release
- `remember` / `recall` / `list` / `delete` / `forget`.
- Pluggable embedding: local deterministic fallback (zero-key) or OpenAI-compatible.
- Optional LLM summarization.
- FastAPI HTTP API + Python SDK + CLI.
- Docker + docker-compose (PostgreSQL + pgvector).
- GitHub Actions CI (pytest against pgvector/pg16).
