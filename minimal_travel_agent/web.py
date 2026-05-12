import json
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path

from main import run_agent_from_request
from tools import TripRequest


ROOT = Path(__file__).parent
STATIC_DIR = ROOT / "static"


class TravelAgentHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        if self.path in ["/", "/index.html"]:
            self._send_file(STATIC_DIR / "index.html", "text/html; charset=utf-8")
            return

        if self.path == "/styles.css":
            self._send_file(STATIC_DIR / "styles.css", "text/css; charset=utf-8")
            return

        if self.path == "/app.js":
            self._send_file(STATIC_DIR / "app.js", "application/javascript; charset=utf-8")
            return

        self.send_error(404)

    def do_POST(self):
        if self.path != "/api/plan":
            self.send_error(404)
            return

        length = int(self.headers.get("Content-Length", "0"))
        payload = json.loads(self.rfile.read(length).decode("utf-8"))

        request = TripRequest(
            departure=payload.get("departure", "上海"),
            destination=payload.get("destination", "日本"),
            days=int(payload.get("days", 5)),
            budget=int(payload.get("budget", 8000)),
            style=payload.get("style", "轻松、不赶路、喜欢美食和城市散步"),
        )
        result = run_agent_from_request(request)
        self._send_json({"result": result})

    def log_message(self, format, *args):
        return

    def _send_file(self, path: Path, content_type: str):
        content = path.read_bytes()
        self.send_response(200)
        self.send_header("Content-Type", content_type)
        self.send_header("Content-Length", str(len(content)))
        self.end_headers()
        self.wfile.write(content)

    def _send_json(self, data: dict):
        content = json.dumps(data, ensure_ascii=False).encode("utf-8")
        self.send_response(200)
        self.send_header("Content-Type", "application/json; charset=utf-8")
        self.send_header("Content-Length", str(len(content)))
        self.end_headers()
        self.wfile.write(content)


def main():
    server = ThreadingHTTPServer(("127.0.0.1", 8000), TravelAgentHandler)
    print("Travel Agent web app: http://127.0.0.1:8000")
    server.serve_forever()


if __name__ == "__main__":
    main()
