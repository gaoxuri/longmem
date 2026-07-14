"""Optional LLM summarization for long memories.

Disabled by default (SUMMARY_ENABLED=false); when off, the raw content is stored.
"""
from .config import SUMMARY_ENABLED, LLM_BASE_URL, LLM_API_KEY, LLM_MODEL

_client = None


def _get_llm():
    global _client
    if _client is None:
        from openai import OpenAI

        _client = OpenAI(base_url=LLM_BASE_URL, api_key=LLM_API_KEY)
    return _client


def summarize(content, max_chars=200):
    if not SUMMARY_ENABLED or not LLM_API_KEY:
        return content[:max_chars] if len(content) > max_chars else content
    try:
        resp = _get_llm().chat.completions.create(
            model=LLM_MODEL,
            temperature=0,
            messages=[
                {"role": "system", "content": "用一句话概括下面的内容，保留关键信息。"},
                {"role": "user", "content": content[:2000]},
            ],
        )
        return resp.choices[0].message.content.strip()
    except Exception:
        return content[:max_chars]
