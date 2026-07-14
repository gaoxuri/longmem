"""LongMem — lightweight long-term memory middleware for LLM apps and agents."""
from .db import init_db
from .store import (
    remember,
    recall,
    list_memories,
    update_memory,
    delete_memory,
    forget_user,
    batch_remember,
    purge_expired,
)

__version__ = "0.2.3"


class Memory:
    """Minimal SDK for embedding apps to give an LLM persistent memory."""

    def __init__(self, user_id, session_id=None):
        self.user_id = user_id
        self.session_id = session_id

    def remember(self, content, mem_type="fact", ttl_seconds=None):
        return remember(self.user_id, content, self.session_id, mem_type, ttl_seconds)

    def remember_batch(self, items):
        """items: list of dicts {content, mem_type?, ttl_seconds?, session_id?}."""
        norm = [
            (self.user_id, it["content"], it.get("session_id", self.session_id),
             it.get("mem_type", "fact"), it.get("ttl_seconds"))
            for it in items
        ]
        return batch_remember(norm)

    def recall(self, query, top_k=None, threshold=None, type_filter=None, recency_bias=0.0):
        return recall(self.user_id, query, self.session_id, top_k, threshold, type_filter, recency_bias)

    def update(self, memory_id, content=None, mem_type=None, ttl_seconds=None):
        return update_memory(memory_id, content, mem_type, ttl_seconds)

    def forget(self):
        return forget_user(self.user_id)


__all__ = [
    "Memory",
    "remember",
    "recall",
    "list_memories",
    "update_memory",
    "delete_memory",
    "forget_user",
    "batch_remember",
    "purge_expired",
    "init_db",
    "__version__",
]
