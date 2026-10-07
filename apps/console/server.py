"""Local read-only PRC V2.5 server backed by the Codex native observer."""

from __future__ import annotations

import json
import sys
from http.server import SimpleHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
APP_DIR = Path(__file__).resolve().parent
TARGET_RUN_ID = "01a0eca4-7029-7f92-b5a9-2006edb08721"

sys.path.insert(0, str(ROOT))

from packages.codex_runtime.observer import CodexRuntimeObserver  # noqa: E402
from packages.workstage_projection import project_run  # noqa: E402


def load_projection() -> dict:
    observer = CodexRuntimeObserver()
    try:
        observer.start()
        return project_run(observer.read_run(TARGET_RUN_ID, limit=200))
    finally:
        observer.close()


class Handler(SimpleHTTPRequestHandler):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, directory=str(APP_DIR), **kwargs)

    def do_GET(self):  # noqa: N802
        if self.path == "/api/health":
            self._json({"status": "ok", "source": "codex.app-server", "read_only": True})
            return
        if self.path == "/api/run.json":
            try:
                self._json(load_projection())
            except Exception as exc:  # local probe should expose the real blocker
                self._json({"status": "ERROR", "error": type(exc).__name__, "message": str(exc)}, 503)
            return
        if self.path == "/" or self.path == "/index.html":
            try:
                projection = load_projection()
                html = (APP_DIR / "index.html").read_text(encoding="utf-8")
                html = html.replace("__PRC_DATA__", json.dumps(projection, ensure_ascii=False))
                body = html.encode("utf-8")
                self.send_response(200)
                self.send_header("Content-Type", "text/html; charset=utf-8")
                self.send_header("Content-Length", str(len(body)))
                self.end_headers()
                self.wfile.write(body)
            except Exception as exc:
                self._json({"status": "ERROR", "error": type(exc).__name__, "message": str(exc)}, 503)
            return
        super().do_GET()

    def _json(self, value: dict, status: int = 200):
        body = json.dumps(value, ensure_ascii=False).encode("utf-8")
        self.send_response(status)
        self.send_header("Content-Type", "application/json; charset=utf-8")
        self.send_header("Cache-Control", "no-store")
        self.send_header("Content-Length", str(len(body)))
        self.end_headers()
        self.wfile.write(body)


def main() -> None:
    port = int(sys.argv[1]) if len(sys.argv) > 1 else 4173
    server = ThreadingHTTPServer(("127.0.0.1", port), Handler)
    print(f"PRC V2.5 listening on http://127.0.0.1:{port}", flush=True)
    server.serve_forever()


if __name__ == "__main__":
    main()
