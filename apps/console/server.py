"""Local read-only PRC server for Work, Agents, and Trace surfaces."""

from __future__ import annotations

import json
import sys
from http.server import SimpleHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path
from urllib.parse import parse_qs, urlparse

ROOT = Path(__file__).resolve().parents[2]
APP_DIR = Path(__file__).resolve().parent
CASE_DIR = ROOT / "PRC_STAGEWISE_CASE_PACK" / "PRC_VERTICAL_SLICE_HANDOFF_v1" / "data" / "aisailing"
sys.path.insert(0, str(ROOT))

from packages.session_sources.codex_jsonl import list_sessions, read_session  # noqa: E402


class Handler(SimpleHTTPRequestHandler):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, directory=str(APP_DIR), **kwargs)

    def do_GET(self):  # noqa: N802
        parsed = urlparse(self.path)
        query = parse_qs(parsed.query)
        if parsed.path == "/favicon.ico":
            self.send_response(204)
            self.end_headers()
            return
        if parsed.path == "/api/health":
            return self._json({"status": "ok", "source": "local_codex_jsonl", "read_only": True})
        if parsed.path == "/api/sessions":
            project = query.get("project", [None])[0]
            sessions = list_sessions(project=project)
            return self._json({"sessions": sessions, "count": len(sessions), "source": "local_codex_jsonl"})
        if parsed.path == "/api/session":
            session_id = query.get("session_id", [None])[0]
            source_path = query.get("path", [None])[0]
            if not session_id:
                return self._json({"error": "session_id_required"}, 400)
            try:
                return self._json(read_session(session_id, path_hint=source_path))
            except FileNotFoundError as exc:
                return self._json({"error": "session_not_found", "message": str(exc)}, 404)
            except PermissionError as exc:
                return self._json({"error": "source_path_rejected", "message": str(exc)}, 403)
            except Exception as exc:  # local diagnostic response; never mutate source
                return self._json({"error": type(exc).__name__, "message": str(exc)}, 500)
        if parsed.path == "/api/case":
            try:
                graph = json.loads((CASE_DIR / "AISAILING_EVOLUTION_GRAPH.json").read_text(encoding="utf-8"))
                overview = (CASE_DIR / "AISAILING_EVOLUTION_OVERVIEW.md").read_text(encoding="utf-8")
                ledger = (CASE_DIR / "AISAILING_EVIDENCE_LEDGER.md").read_text(encoding="utf-8")
                return self._json({"graph": graph, "overview": overview, "ledger": ledger})
            except Exception as exc:
                return self._json({"error": type(exc).__name__, "message": str(exc)}, 503)
        if parsed.path in ("/", "/index.html"):
            return super().do_GET()
        return super().do_GET()

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
    print(f"PRC local read-only session viewer at http://127.0.0.1:{port}", flush=True)
    server.serve_forever()


if __name__ == "__main__":
    main()
