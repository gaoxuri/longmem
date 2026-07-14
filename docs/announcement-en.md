# LongMem — self-hosted long-term memory for LLM agents

> Copy-ready announcement for Hacker News ("Show HN") and Reddit r/LocalLLaMA.
> Edit the intro line to fit the venue. Keep it honest — no hype claims.

---

## Hacker News — "Show HN" (title + body)

**Title:** Show HN: LongMem – self-hosted long-term memory middleware for LLM agents (Postgres + pgvector)

**Body:**

Most LLM agents forget everything between sessions. If you want persistence you
usually end up hand-rolling a vector-store layer. LongMem is a small, MIT-licensed
middleware that gives any LLM app or agent a memory API backed by *your own*
PostgreSQL + pgvector.

What it does:
- `remember` / `recall` / `batch` / `update` / `delete` / `forget`
- per-memory TTL (auto-expiry) with a purge daemon
- recall filtering by `mem_type`, plus a recency bias so fresher memories rank higher
- pluggable embeddings: ships a zero-key deterministic fallback so it runs
  end-to-end with **no API key**; swap in any OpenAI-compatible model in production
- FastAPI HTTP API + Python SDK + CLI
- Docker one command (`docker compose up --build`), GitHub Actions CI, bilingual docs

Why self-hosted: your memory stays in a database you control — no closed-source
memory service, no per-call vendor lock-in.

Repo: https://github.com/gaoxuri/longmem
License: MIT

Feedback and PRs welcome.

---

## Reddit r/LocalLLaMA (post)

**Title:** LongMem: drop-in long-term memory for your local agents (Postgres + pgvector, MIT)

**Body:**

If you run local models and want your agents to actually remember things across
sessions without wiring up a vector DB by hand, I open-sourced LongMem.

- Backed by your own Postgres + pgvector — nothing leaves your infra.
- Zero-key demo mode: a deterministic local embedding lets the whole stack run
  with no API key; flip one env var to use an OpenAI-compatible embedder in prod.
- Features: batch write, TTL expiry + auto-purge, type filtering, recency bias,
  full CRUD over HTTP / SDK / CLI.
- `docker compose up --build` and you're done; CI is green.

It's intentionally tiny and dependency-light (FastAPI + psycopg2 + stdlib).
Good fit if you're building a local assistant and want memory without a SaaS.

https://github.com/gaoxuri/longmem

---

## One-liner (for X / Mastodon)

LongMem: self-hosted long-term memory for LLM agents. Your Postgres + pgvector,
zero-key demo mode, Docker-ready, MIT. https://github.com/gaoxuri/longmem #llm #agent #rag
