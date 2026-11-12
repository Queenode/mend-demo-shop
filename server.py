"""
Checkout API.

    POST /quote  {"items": [{"sku": "tee", "qty": 2}], "coupon": "SAVE10"}

Crashes are reported to Mend, which proposes a fix as a pull request.
"""
from __future__ import annotations

import json
import os
from http.server import BaseHTTPRequestHandler, HTTPServer

from mend.sdk import MendWatch

from shop.pricing import quote

mend = MendWatch(repo="Rampop01/mend-demo-shop")


class Handler(BaseHTTPRequestHandler):
    def _send(self, status: int, body: dict) -> None:
        data = json.dumps(body).encode()
        self.send_response(status)
        self.send_header("Content-Type", "application/json")
        self.send_header("Content-Length", str(len(data)))
        self.end_headers()
        self.wfile.write(data)

    def do_POST(self) -> None:
        if self.path != "/quote":
            self._send(404, {"error": "not found"})
            return
        try:
            body = json.loads(self.rfile.read(int(self.headers.get("Content-Length") or 0)) or b"{}")
            self._send(200, quote(body.get("items", []), body.get("coupon", "")))
        except Exception as exc:
            mend.capture_exception(exc)
            self._send(500, {"error": "internal error"})

    def log_message(self, format: str, *args) -> None:
        print(f"{self.command} {self.path} -> {args[1] if len(args) > 1 else ''}")


if __name__ == "__main__":
    port = int(os.environ.get("PORT", "8000"))
    print(f"Shop API on http://127.0.0.1:{port}")
    HTTPServer(("127.0.0.1", port), Handler).serve_forever()
