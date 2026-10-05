#!/usr/bin/env python3
"""Small local console server for the Step 1 vertical slice."""

from __future__ import annotations

import argparse
import json
from http.server import SimpleHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path
from urllib.parse import urlparse

CONSOLE_ROOT = Path(__file__).resolve().parent


class ConsoleHandler(SimpleHTTPRequestHandler):
    data_path: Path

    def __init__(self, *args, **kwargs):
        super().__init__(*args, directory=str(CONSOLE_ROOT), **kwargs)

    def do_GET(self) -> None:  # noqa: N802
        path = urlparse(self.path).path
        if path == "/api/state":
            self._send_json()
            return
        if path == "/":
            self.path = "/index.html"
        super().do_GET()

    def _send_json(self) -> None:
        try:
            payload = json.loads(self.data_path.read_text(encoding="utf-8"))
        except (OSError, json.JSONDecodeError) as exc:
            body = json.dumps({"error": type(exc).__name__}).encode("utf-8")
            self.send_response(500)
            self.send_header("Content-Type", "application/json")
            self.send_header("Content-Length", str(len(body)))
            self.end_headers()
            self.wfile.write(body)
            return
        body = json.dumps(payload, ensure_ascii=False).encode("utf-8")
        self.send_response(200)
        self.send_header("Content-Type", "application/json; charset=utf-8")
        self.send_header("Cache-Control", "no-store")
        self.send_header("Content-Length", str(len(body)))
        self.end_headers()
        self.wfile.write(body)


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--data", type=Path, required=True)
    parser.add_argument("--port", type=int, default=8765)
    args = parser.parse_args()
    if not args.data.exists():
        parser.error(f"data file does not exist: {args.data}")
    ConsoleHandler.data_path = args.data
    server = ThreadingHTTPServer(("127.0.0.1", args.port), ConsoleHandler)
    print(f"Project Runtime Console: http://127.0.0.1:{args.port}")
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        return 0
    finally:
        server.server_close()
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
