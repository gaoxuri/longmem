"""End-to-end smoke tests for LongMem store (uses the configured PG)."""
import os
import sys
import time

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from longmem import init_db, remember, recall, list_memories, delete_memory, forget_user
from longmem.store import batch_remember, purge_expired, update_memory

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


def test_update_memory():
    res = remember(USER, "原始内容：用户喜欢红色")
    mid = res["id"]
    assert update_memory(mid, content="更新内容：用户喜欢蓝色")
    rows = list_memories(USER)
    assert any(r["id"] == mid and "蓝色" in r["content"] for r in rows)
    # type-only update keeps content
    assert update_memory(mid, mem_type="preference")
    rows = [r for r in list_memories(USER) if r["id"] == mid]
    assert rows and rows[0]["mem_type"] == "preference"
    delete_memory(mid)
    res = batch_remember([
        (USER, "批量记忆一", None, "fact", None),
        (USER, "批量记忆二", None, "fact", None),
    ])
    assert len(res) == 2
    ids = [r["id"] for r in res]
    assert all(i > 0 for i in ids)
    # cleanup
    for i in ids:
        delete_memory(i)


def test_recall_filters():
    forget_user(USER)
    remember(USER, "用户使用 PostgreSQL 数据库存储数据", mem_type="fact")
    remember(USER, "用户的偏好：喜欢 Python", mem_type="preference")
    # type_filter narrows results
    pref = recall(USER, "喜欢什么", type_filter="preference")
    assert len(pref) >= 1 and all(r["mem_type"] == "preference" for r in pref)
    # recency_bias does not crash and still returns > 0
    biased = recall(USER, "存储", recency_bias=0.3)
    assert len(biased) >= 1
    # default (no args) still works
    assert recall(USER, "数据库") != []
    forget_user(USER)


def test_purge_cli():
    forget_user(USER)
    remember(USER, "1 秒后过期", ttl_seconds=1)
    time.sleep(1.2)
    # purge via store function
    n = purge_expired()
    assert n == 1
    assert list_memories(USER) == []
    forget_user(USER)


def test_ttl_expiry():
    # A 1-second TTL memory should be excluded from recall/list after it expires.
    remember(USER, "这条 1 秒后过期", ttl_seconds=1)
    # immediate recall still returns it
    assert any("过期" in r["content"] for r in recall(USER, "过期"))
    time.sleep(2)
    # after expiry it should be gone (without purge, just filtered out)
    assert not any("过期" in r["content"] for r in list_memories(USER))
    # purge then confirm hard-deleted
    assert purge_expired() >= 1
    assert not any("过期" in r["content"] for r in list_memories(USER))
