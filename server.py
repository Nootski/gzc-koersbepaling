#!/usr/bin/env python3
"""
Koersbepaling Maatschap — Live Server
Zero dependencies, alleen Python 3.7+
Start met: python3 server.py
"""
import json
import os
import socket
import threading
import time
from http.server import ThreadingHTTPServer, SimpleHTTPRequestHandler
from urllib.parse import urlparse

STATE_FILE = "heidedag_state.json"
state_lock = threading.Lock()

def load_state():
    if os.path.exists(STATE_FILE):
        with open(STATE_FILE) as f:
            return json.load(f)
    return {"votes": {}, "stickies": {}, "texts": {}, "participants": {}, "version": 0}

def save_state():
    with open(STATE_FILE, "w") as f:
        json.dump(state, f, ensure_ascii=False, indent=2)

state = load_state()


class Handler(SimpleHTTPRequestHandler):
    def log_message(self, format, *args):
        pass

    def send_json(self, data, code=200):
        body = json.dumps(data, ensure_ascii=False).encode()
        self.send_response(code)
        self.send_header("Content-Type", "application/json; charset=utf-8")
        self.send_header("Access-Control-Allow-Origin", "*")
        self.send_header("Cache-Control", "no-cache")
        self.end_headers()
        self.wfile.write(body)

    def do_OPTIONS(self):
        self.send_response(200)
        self.send_header("Access-Control-Allow-Origin", "*")
        self.send_header("Access-Control-Allow-Methods", "GET, POST, OPTIONS")
        self.send_header("Access-Control-Allow-Headers", "Content-Type")
        self.end_headers()

    def do_GET(self):
        path = urlparse(self.path).path
        if path == "/api/state":
            with state_lock:
                self.send_json(state)
        elif path in ("/", ""):
            self.path = "/facilitatie-app.html"
            super().do_GET()
        else:
            super().do_GET()

    def do_POST(self):
        if self.path == "/api/update":
            length = int(self.headers.get("Content-Length", 0))
            body = json.loads(self.rfile.read(length))
            with state_lock:
                self._apply(body)
                state["version"] += 1
                save_state()
            self.send_json({"ok": True, "version": state["version"]})
        else:
            self.send_response(404)
            self.end_headers()

    def _apply(self, update):
        t = update.get("type")

        if t == "vote":
            sid = update["id"]
            d = update["direction"]
            if sid not in state["votes"]:
                state["votes"][sid] = {"up": 0, "side": 0, "down": 0}
            state["votes"][sid][d] = state["votes"][sid].get(d, 0) + 1

        elif t == "sticky_add":
            zone = update["zone"]
            if zone not in state["stickies"]:
                state["stickies"][zone] = {}
            state["stickies"][zone][update["id"]] = {
                "text": update.get("text", ""),
                "color": update["color"],
                "author": update["author"],
                "authorColor": update["authorColor"],
            }

        elif t == "sticky_update":
            zone = update["zone"]
            sid = update["id"]
            if zone in state["stickies"] and sid in state["stickies"][zone]:
                state["stickies"][zone][sid]["text"] = update["text"]

        elif t == "sticky_delete":
            zone = update.get("zone")
            sid = update.get("id")
            if zone in state.get("stickies", {}) and sid in state["stickies"][zone]:
                del state["stickies"][zone][sid]

        elif t == "text":
            state["texts"][update["id"]] = update["value"]

        elif t == "join":
            state["participants"][update["name"]] = {
                "color": update["color"],
                "lastSeen": time.time(),
            }

        elif t == "heartbeat":
            name = update.get("name")
            if name and name in state["participants"]:
                state["participants"][name]["lastSeen"] = time.time()


def get_local_ip():
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    try:
        s.connect(("8.8.8.8", 80))
        return s.getsockname()[0]
    except Exception:
        return "127.0.0.1"
    finally:
        s.close()


if __name__ == "__main__":
    PORT = 8080
    ip = get_local_ip()
    os.chdir(os.path.dirname(os.path.abspath(__file__)))
    server = ThreadingHTTPServer(("0.0.0.0", PORT), Handler)

    print()
    print("  ╔══════════════════════════════════════════╗")
    print("  ║   Koersbepaling Maatschap — Live Server  ║")
    print("  ╠══════════════════════════════════════════╣")
    print("  ║                                          ║")
    print("  ║   Deel deze link met de maten:           ║")
    url = f"http://{ip}:{PORT}"
    local_url = f"http://localhost:{PORT}"
    print(f"  ║   → {url:<36s} ║")
    print("  ║                                          ║")
    print("  ║   Of lokaal:                             ║")
    print(f"  ║   → {local_url:<36s} ║")
    print("  ║                                          ║")
    print("  ║   Druk Ctrl+C om te stoppen              ║")
    print("  ╚══════════════════════════════════════════╝")
    print()

    try:
        server.serve_forever()
    except KeyboardInterrupt:
        print("\n  Server gestopt. State opgeslagen in heidedag_state.json")
        server.shutdown()
