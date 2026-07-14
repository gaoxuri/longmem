"""End-to-end smoke tests for LongMem store (uses the configured PG)."""
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from longmem import init_db, remember, recall, list_memories, delete_memory, forget_user

USER = "test_user"


def setup_module(module):
    init_db()
    forget_user(USER)


def teardown_module(module):
    forget_user(USER)


def test_remember_and_list():
    res = remember(USER, "用户喜欢用 Python 写后端", mem_type="preference")
    assert res["id"] > 0
    rows = list_memories(USER)
    assert any("Python" in r["content"] for r in rows)


def test_recall_returns_relevant():
    remember(USER, "用户使用 PostgreSQL 数据库存储数据")
    remember(USER, "用户喜欢打篮球")
    results = recall(USER, "数据库怎么存的")
    assert len(results) > 0
    # The PostgreSQL/database memory should rank first (character overlap)
    top = results[0]
    assert "数据库" in top["content"]
    assert top["score"] > 0


def test_delete_and_forget():
    res = remember(USER, "临时记忆，稍后删除")
    mid = res["id"]
    assert delete_memory(mid) is True
    assert delete_memory(mid) is False  # already gone
    remember(USER, "另一条")
    n = forget_user(USER)
    assert n >= 1
    assert list_memories(USER) == []
