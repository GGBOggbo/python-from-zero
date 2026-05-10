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

PORT = 8888
WEB_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), "web")


class MyHandler(http.server.SimpleHTTPRequestHandler):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, directory=WEB_DIR, **kwargs)

    def log_message(self, format, *args):
        pass

    def do_POST(self):
        if self.path == "/run":
            self.handle_run()
        else:
            self.send_error(404)

    def handle_run(self):
        try:
            length = int(self.headers.get("Content-Length", 0))
            body = self.rfile.read(length)
            data = json.loads(body)
            code = data.get("code", "")

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
        self.send_header("Content-Type", "application/json; charset=utf-8")
        self.send_header("Content-Length", str(len(body)))
        self.end_headers()
        self.wfile.write(body)


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
