from http.server import BaseHTTPRequestHandler, HTTPServer
import json
from urllib.parse import parse_qs

from password_strength_checker_api import check_password_strength


class SimpleAPIHandler(BaseHTTPRequestHandler):
    def do_POST(self):
        if self.path != "/check":
            self.send_error(404, "Not found")
            return

        content_length = int(self.headers.get("Content-Length", 0))
        post_data = self.rfile.read(content_length).decode("utf-8")
        try:
            data = json.loads(post_data)
            password = data.get("password")
        except Exception:
            self.send_response(400)
            self.end_headers()
            self.wfile.write(b'{"error": "Invalid JSON"}')
            return

        if not password:
            self.send_response(400)
            self.end_headers()
            self.wfile.write(b'{"error": "Missing password"}')
            return

        result = check_password_strength(password)

        self.send_response(200)
        self.send_header("Content-Type", "application/json")
        self.end_headers()
        self.wfile.write(json.dumps(result).encode("utf-8"))


if __name__ == "__main__":
    server_address = ("", 8080)
    print("🚀 Starting server on http://localhost:8080")
    httpd = HTTPServer(server_address, SimpleAPIHandler)
    httpd.serve_forever()
