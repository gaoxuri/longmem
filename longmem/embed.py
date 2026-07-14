"""Embedding layer: OpenAI-compatible backend with a local deterministic fallback.

The fallback tokenizes CJK text character-by-character and latin text word-by-word,
then hashes tokens into a fixed-dimensional bag-of-tokens vector — so the whole
stack runs end-to-end with zero external dependencies (ideal for dev and tests).
Swap in a real model by setting EMBED_PROVIDER=openai and EMBED_API_KEY in .env.
"""
import hashlib
import math
import re

from .config import EMBED_PROVIDER, EMBED_BASE_URL, EMBED_API_KEY, EMBED_MODEL, EMBED_DIM

_client = None

_TOKEN_RE = re.compile(r"[\u4e00-\u9fff]|[a-zA-Z0-9]+")


def _tokenize(text):
    return _TOKEN_RE.findall(text.lower())


def _get_client():
    global _client
    if _client is None:
        from openai import OpenAI

        _client = OpenAI(base_url=EMBED_BASE_URL, api_key=EMBED_API_KEY)
    return _client


def _openai_embed(texts):
    resp = _get_client().embeddings.create(model=EMBED_MODEL, input=texts)
    return [d.embedding for d in resp.data]


def _fallback_embed(text):
    vec = [0.0] * EMBED_DIM
    for tok in _tokenize(text):
        h = int(hashlib.md5(tok.encode("utf-8")).hexdigest(), 16) % EMBED_DIM
        vec[h] += 1.0
    norm = math.sqrt(sum(v * v for v in vec))
    if norm > 0:
        vec = [v / norm for v in vec]
    return vec


def embed(text):
    if EMBED_PROVIDER.lower() == "openai" and EMBED_API_KEY:
        return _openai_embed([text])[0]
    return _fallback_embed(text)


def embed_batch(texts):
    if EMBED_PROVIDER.lower() == "openai" and EMBED_API_KEY:
        return _openai_embed(texts)
    return [_fallback_embed(t) for t in texts]
