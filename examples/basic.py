"""Minimal SDK usage example.

Run after `longmem db init` and configuring .env:

    python examples/basic.py
"""
from longmem import Memory

if __name__ == "__main__":
    mem = Memory(user_id="alice", session_id="s1")

    mem.remember("用户是一名后端工程师，主要用 Java 和 Python。")
    mem.remember("用户正在做一个开源 AI 记忆中间件项目。")
    mem.remember("用户喜欢在周末爬山。")

    print("=== recall: 用户的技术背景 ===")
    for r in mem.recall("用户会哪些编程语言"):
        print(f"  [{r['score']:.3f}] {r['content']}")

    print("\n=== recall: 用户的项目 ===")
    for r in mem.recall("用户在做什么开源项目"):
        print(f"  [{r['score']:.3f}] {r['content']}")
