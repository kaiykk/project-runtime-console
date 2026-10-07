"""Small JSON-RPC client for the local Codex app-server.

The client is intentionally read-only. It initializes a native app-server
connection, issues allowlisted read requests, and retains notifications in
memory for the observer. It never starts a thread or turn.
"""

from __future__ import annotations

import json
import os
import queue
import subprocess
import threading
from dataclasses import dataclass
from typing import Any


class CodexAppServerError(RuntimeError):
    """Raised when the app-server cannot satisfy a read request."""


@dataclass(frozen=True)
class AppServerInfo:
    user_agent: str
    codex_home: str
    platform_family: str
    platform_os: str


class CodexAppServerClient:
    """A bounded stdio JSON-RPC client for Codex app-server v2."""

    def __init__(
        self,
        *,
        codex_bin: str = "codex",
        timeout: float = 15.0,
        client_version: str = "0.1.0",
    ) -> None:
        self.codex_bin = codex_bin
        self.timeout = timeout
        self.client_version = client_version
        self._process: subprocess.Popen[bytes] | None = None
        self._reader_thread: threading.Thread | None = None
        self._next_id = 0
        self._pending: dict[int, queue.Queue[dict[str, Any]]] = {}
        self._pending_lock = threading.Lock()
        self._write_lock = threading.Lock()
        self._start_lock = threading.Lock()
        self._notifications: list[dict[str, Any]] = []
        self._notifications_lock = threading.Lock()
        self._stopped = threading.Event()
        self.info: AppServerInfo | None = None

    @property
    def started(self) -> bool:
        return self._process is not None and self._process.poll() is None

    def start(self) -> AppServerInfo:
        with self._start_lock:
            if self.started and self.info is not None:
                return self.info
            self._stopped.clear()
            self._process = subprocess.Popen(
                [self.codex_bin, "app-server", "--stdio"],
                stdin=subprocess.PIPE,
                stdout=subprocess.PIPE,
                stderr=subprocess.DEVNULL,
                env=os.environ.copy(),
            )
            self._reader_thread = threading.Thread(
                target=self._read_loop,
                name="prc-codex-app-server-reader",
                daemon=True,
            )
            self._reader_thread.start()
            result = self.request(
                "initialize",
                {
                    "clientInfo": {
                        "name": "project-runtime-console",
                        "title": "Project Runtime Console",
                        "version": self.client_version,
                    },
                    "capabilities": {
                        "experimentalApi": True,
                        "optOutNotificationMethods": [],
                    },
                },
            )
            self._notify("initialized", {})
            self.info = AppServerInfo(
                user_agent=str(result.get("userAgent", "")),
                codex_home=str(result.get("codexHome", "")),
                platform_family=str(result.get("platformFamily", "")),
                platform_os=str(result.get("platformOs", "")),
            )
            return self.info

    def close(self) -> None:
        self._stopped.set()
        process = self._process
        if process is None:
            return
        if process.poll() is None:
            process.terminate()
            try:
                process.wait(timeout=2)
            except subprocess.TimeoutExpired:
                process.kill()
                process.wait(timeout=2)
        self._process = None

    def request(self, method: str, params: dict[str, Any] | None = None) -> dict[str, Any]:
        if self._process is None or self._process.stdin is None:
            raise CodexAppServerError("app-server is not started")
        with self._pending_lock:
            self._next_id += 1
            request_id = self._next_id
            response_queue: queue.Queue[dict[str, Any]] = queue.Queue(maxsize=1)
            self._pending[request_id] = response_queue
        message = {"jsonrpc": "2.0", "id": request_id, "method": method}
        if params is not None:
            message["params"] = params
        try:
            with self._write_lock:
                self._process.stdin.write((json.dumps(message) + "\n").encode("utf-8"))
                self._process.stdin.flush()
            response = response_queue.get(timeout=self.timeout)
        except (OSError, queue.Empty) as exc:
            raise CodexAppServerError(f"request failed: {method}") from exc
        finally:
            with self._pending_lock:
                self._pending.pop(request_id, None)
        if "error" in response:
            raise CodexAppServerError(
                f"{method}: {json.dumps(response['error'], ensure_ascii=True)}"
            )
        result = response.get("result")
        if not isinstance(result, dict):
            raise CodexAppServerError(f"{method}: invalid response result")
        return result

    def notifications_since(self, cursor: int = 0) -> tuple[int, list[dict[str, Any]]]:
        with self._notifications_lock:
            return len(self._notifications), list(self._notifications[cursor:])

    def _notify(self, method: str, params: dict[str, Any]) -> None:
        if self._process is None or self._process.stdin is None:
            return
        message = {"jsonrpc": "2.0", "method": method, "params": params}
        try:
            with self._write_lock:
                self._process.stdin.write((json.dumps(message) + "\n").encode("utf-8"))
                self._process.stdin.flush()
        except OSError:
            return

    def _read_loop(self) -> None:
        process = self._process
        if process is None or process.stdout is None:
            return
        while not self._stopped.is_set():
            line = process.stdout.readline()
            if not line:
                return
            try:
                message = json.loads(line.decode("utf-8"))
            except (UnicodeDecodeError, json.JSONDecodeError):
                continue
            if not isinstance(message, dict):
                continue
            request_id = message.get("id")
            if isinstance(request_id, int):
                with self._pending_lock:
                    response_queue = self._pending.get(request_id)
                if response_queue is not None:
                    response_queue.put(message)
                continue
            method = message.get("method")
            if isinstance(method, str):
                with self._notifications_lock:
                    self._notifications.append(message)
