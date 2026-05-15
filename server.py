#!/usr/bin/env python3
"""
Python 学习平台 - 启动脚本
运行: python server.py
然后在浏览器打开 http://localhost:8888
"""

import http.server
import socketserver
import json
import subprocess
import sys
import os
import tempfile
import urllib.parse
import time
import logging

PORT = 8888
WEB_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), "web")

logging.basicConfig(level=logging.INFO, format='%(asctime)s %(message)s', datefmt='%H:%M:%S')
logger = logging.getLogger(__name__)

# Rate limiting: {ip: [timestamps]}
rate_limit = {}
RATE_WINDOW = 60  # seconds
RATE_MAX = 30  # requests per window

# Forbidden code patterns
FORBIDDEN = ['os.system(', 'subprocess.call(', 'subprocess.Popen(', 'shutil.rmtree(', '__import__']


class MyHandler(http.server.SimpleHTTPRequestHandler):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, directory=WEB_DIR, **kwargs)

    def check_rate_limit(self):
        ip = self.client_address[0]
        now = time.time()
        if ip not in rate_limit:
            rate_limit[ip] = []
        rate_limit[ip] = [t for t in rate_limit[ip] if now - t < RATE_WINDOW]
        if len(rate_limit[ip]) >= RATE_MAX:
            return False
        rate_limit[ip].append(now)
        return True

    def send_json_error(self, code, message):
        body = json.dumps({"error": message}, ensure_ascii=False).encode("utf-8")
        self.send_response(code)
        self.send_header("Content-Type", "application/json; charset=utf-8")
        self.send_header("Content-Length", str(len(body)))
        self.end_headers()
        self.wfile.write(body)

    def log_message(self, format, *args):
        logger.info(f"{self.client_address[0]} - {format % args}")

    def do_POST(self):
        if self.path == "/run":
            self.handle_run()
        else:
            self.send_error(404)

    def handle_run(self):
        if not self.check_rate_limit():
            self.send_json_error(429, "请求过于频繁，请稍后再试")
            return

        try:
            length = int(self.headers.get("Content-Length", 0))
            body = self.rfile.read(length)
            data = json.loads(body)
            code = data.get("code", "")

            if len(code) > 10000:
                self.send_json_error(400, "代码长度超过限制（最大 10000 字符）")
                return

            # Security check
            for pattern in FORBIDDEN:
                if pattern in code:
                    self.send_json_error(403, f"禁止使用: {pattern}")
                    return

            if not code.strip():
                self.send_json({"stdout": "", "stderr": "请先写点代码再运行"})
                return

            with tempfile.NamedTemporaryFile(
                mode="w", suffix=".py", delete=False
            ) as f:
                f.write(code)
                tmp_path = f.name

            try:
                result = subprocess.run(
                    [sys.executable, tmp_path],
                    capture_output=True,
                    text=True,
                    timeout=10,
                )
                self.send_json({
                    "stdout": result.stdout,
                    "stderr": result.stderr,
                    "exitcode": result.returncode,
                })
            except subprocess.TimeoutExpired:
                self.send_json({"stdout": "", "stderr": "执行超时（10秒限制）", "exitcode": -1})
            finally:
                os.unlink(tmp_path)

        except Exception as e:
            self.send_json({"stdout": "", "stderr": str(e), "exitcode": -1})

    def send_json(self, data):
        body = json.dumps(data, ensure_ascii=False).encode("utf-8")
        self.send_response(200)
        self.send_header("Access-Control-Allow-Origin", "*")
        self.send_header("Content-Type", "application/json; charset=utf-8")
        self.send_header("Content-Length", str(len(body)))
        self.end_headers()
        self.wfile.write(body)

    def do_OPTIONS(self):
        self.send_response(204)
        self.send_header("Access-Control-Allow-Origin", "*")
        self.send_header("Access-Control-Allow-Methods", "POST, GET, OPTIONS")
        self.send_header("Access-Control-Allow-Headers", "Content-Type")
        self.end_headers()

    def do_GET(self):
        try:
            super().do_GET()
        except Exception:
            self.send_error(404)


if __name__ == "__main__":
    os.chdir(WEB_DIR)

    socketserver.TCPServer.allow_reuse_address = True

    with socketserver.TCPServer(("0.0.0.0", PORT), MyHandler) as httpd:
        url = f"http://localhost:{PORT}"
        print(f"Python 学习平台已启动！")
        print(f"浏览器打开: {url}")
        print(f"按 Ctrl+C 停止")
        print()

        try:
            httpd.serve_forever()
        except KeyboardInterrupt:
            print("\n服务已停止")
