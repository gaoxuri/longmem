"""Minimal zero-dependency web demo front-end for LongMem.

Serves a single HTML page that talks to a running LongMem API.
No third-party packages — uses only the Python standard library.

Usage:
    1. Start the API:        python -m longmem.api   (default :8123)
    2. Start this demo:      python examples/web_demo.py
    3. Open:                  http://localhost:8000
"""
import argparse
import os
import sys
from http.server import HTTPServer, SimpleHTTPRequestHandler

HERE = os.path.dirname(os.path.abspath(__file__))
STATIC = os.path.join(HERE, "static")


class Handler(SimpleHTTPRequestHandler):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, directory=STATIC, **kwargs)

    def log_message(self, *a):  # quiet
        pass


def main():
    p = argparse.ArgumentParser(description="LongMem web demo (zero deps)")
    p.add_argument("--port", type=int, default=8000)
    p.add_argument("--api", default="http://localhost:8123",
                   help="Base URL of a running LongMem API")
    args = p.parse_args()

    os.environ["LONGMEM_API_BASE"] = args.api

    httpd = HTTPServer(("0.0.0.0", args.port), Handler)
    print(f"LongMem demo → http://localhost:{args.port}  (API: {args.api})")
    try:
        httpd.serve_forever()
    except KeyboardInterrupt:
        httpd.shutdown()


if __name__ == "__main__":
    main()
