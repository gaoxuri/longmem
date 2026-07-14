"""Minimal SDK usage example.

Run after starting the API and configuring .env (see .env.example):

    # terminal 1: start the API (auto-creates tables)
    python -m longmem.api
    # terminal 2:
    python examples/basic.py
"""
from longmem import Memory

if __name__ == "__main__":
    mem = Memory(user_id="alice", session_id="s1")

    mem.remember("用户是一名后端工程师，主要用 Java 和 Python。")
    mem.remember("用户正在做一个开源 AI 记忆中间件项目。")
    mem.remember("用户喜欢在周末爬山。", ttl_seconds=3600)  # expires in 1h

    print("=== recall: 用户的技术背景 ===")
    for r in mem.recall("用户会哪些编程语言"):
        print(f"  [{r['score']:.3f}] {r['content']}")

    print("\n=== recall: 用户的项目 ===")
    for r in mem.recall("用户在做什么开源项目"):
        print(f"  [{r['score']:.3f}] {r['content']}")

    print("\n=== recall: 只取偏好类 (type_filter) ===")
    for r in mem.recall("用户的兴趣", type_filter="fact"):
        print(f"  [{r['score']:.3f}] {r['content']}")
