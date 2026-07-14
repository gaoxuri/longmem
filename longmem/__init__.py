"""LongMem — lightweight long-term memory middleware for LLM apps and agents."""
from .db import init_db
from .store import (
    remember,
    recall,
    list_memories,
    delete_memory,
    forget_user,
)

__version__ = "0.1.0"


class Memory:
    """Minimal SDK for embedding apps to give an LLM persistent memory."""

    def __init__(self, user_id, session_id=None):
        self.user_id = user_id
        self.session_id = session_id

    def remember(self, content, mem_type="fact"):
        return remember(self.user_id, content, self.session_id, mem_type)

    def recall(self, query, top_k=None, threshold=None):
        return recall(self.user_id, query, self.session_id, top_k, threshold)

    def forget(self):
        return forget_user(self.user_id)


__all__ = [
    "Memory",
    "remember",
    "recall",
    "list_memories",
    "delete_memory",
    "forget_user",
    "init_db",
    "__version__",
]
