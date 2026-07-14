"""Command-line interface for LongMem."""
import argparse
import json

from .store import remember, recall, list_memories, delete_memory, forget_user


def main():
    p = argparse.ArgumentParser(prog="longmem", description="AI long-term memory CLI")
    sub = p.add_subparsers(dest="cmd", required=True)

    r = sub.add_parser("remember", help="Store a memory")
    r.add_argument("--user", required=True)
    r.add_argument("--content", required=True)
    r.add_argument("--session", default=None)
    r.add_argument("--type", default="fact")

    rc = sub.add_parser("recall", help="Recall memories by query")
    rc.add_argument("--user", required=True)
    rc.add_argument("--query", required=True)
    rc.add_argument("--session", default=None)
    rc.add_argument("--top-k", type=int, default=None)
    rc.add_argument("--threshold", type=float, default=None)

    ls = sub.add_parser("list", help="List a user's memories")
    ls.add_argument("--user", required=True)
    ls.add_argument("--session", default=None)

    dl = sub.add_parser("delete", help="Delete a memory by id")
    dl.add_argument("--id", type=int, required=True)

    fg = sub.add_parser("forget", help="Forget all of a user's memories")
    fg.add_argument("--user", required=True)

    args = p.parse_args()

    if args.cmd == "remember":
        res = remember(args.user, args.content, args.session, args.type)
        print(json.dumps({"ok": True, **res}, ensure_ascii=False))
    elif args.cmd == "recall":
        res = recall(args.user, args.query, args.session, args.top_k, args.threshold)
        print(json.dumps(res, ensure_ascii=False, indent=2))
    elif args.cmd == "list":
        print(json.dumps(list_memories(args.user, args.session), ensure_ascii=False, indent=2))
    elif args.cmd == "delete":
        print(json.dumps({"ok": delete_memory(args.id)}, ensure_ascii=False))
    elif args.cmd == "forget":
        print(json.dumps({"ok": True, "deleted": forget_user(args.user)}, ensure_ascii=False))


if __name__ == "__main__":
    main()
