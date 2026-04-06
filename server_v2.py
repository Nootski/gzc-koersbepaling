#!/usr/bin/env python3
"""
Koersbepaling v2 — Multi-user real-time server met SSE
Zero dependencies, alleen Python 3.7+
Start met: python3 server_v2.py
"""
import json
import os
import queue
import socket
import threading
import time
from http.server import ThreadingHTTPServer, SimpleHTTPRequestHandler
from urllib.parse import urlparse

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
STATE_FILE = os.path.join(BASE_DIR, "v2_state.json")
SESSIONS_DIR = os.path.join(BASE_DIR, "v2_sessions")
V2_DIR = os.path.join(BASE_DIR, "v2")

os.makedirs(SESSIONS_DIR, exist_ok=True)

PARTICIPANTS = {
    "Sophie": "#E57373",
    "Rinske": "#64B5F6",
    "Jesper": "#81C784",
    "Frank": "#FFB74D",
    "Anne": "#BA68C8",
    "Louise": "#4DB6AC",
}

state_lock = threading.Lock()
sse_clients = []
sse_lock = threading.Lock()


def fresh_state():
    return {
        "version": 0,
        "currentSlide": "welkom",
        "startedAt": time.strftime("%Y-%m-%dT%H:%M:%S"),
        "participants": {},
        "votes": {},
        "stickies": {},
        "texts": {},
    }


def load_state():
    if os.path.exists(STATE_FILE):
        with open(STATE_FILE) as f:
            data = json.load(f)
            if "startedAt" not in data:
                data["startedAt"] = time.strftime("%Y-%m-%dT%H:%M:%S")
            return data
    return fresh_state()


def archive_state():
    """Save current state to v2_sessions/ with timestamp, return the filename."""
    ts = time.strftime("%Y%m%d_%H%M%S")
    started = state.get("startedAt", "unknown")
    fname = f"sessie_{ts}.json"
    path = os.path.join(SESSIONS_DIR, fname)
    archive = dict(state)
    archive["archivedAt"] = time.strftime("%Y-%m-%dT%H:%M:%S")
    with open(path, "w") as f:
        json.dump(archive, f, ensure_ascii=False, indent=2)
    return fname, started


def save_state():
    with open(STATE_FILE, "w") as f:
        json.dump(state, f, ensure_ascii=False, indent=2)


state = load_state()


def broadcast(event):
    """Send SSE event to all connected clients."""
    data = json.dumps(event, ensure_ascii=False)
    msg = f"data: {data}\n\n".encode()
    with sse_lock:
        dead = []
        for q in sse_clients:
            try:
                q.put_nowait(msg)
            except Exception:
                dead.append(q)
        for q in dead:
            sse_clients.remove(q)


class Handler(SimpleHTTPRequestHandler):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, directory=V2_DIR, **kwargs)

    def log_message(self, fmt, *args):
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

        elif path == "/api/participants":
            self.send_json(PARTICIPANTS)

        elif path == "/api/sessions":
            files = sorted(
                [f for f in os.listdir(SESSIONS_DIR) if f.endswith(".json")],
                reverse=True,
            )
            sessions = []
            for f in files:
                fp = os.path.join(SESSIONS_DIR, f)
                with open(fp) as fh:
                    d = json.load(fh)
                sessions.append({
                    "file": f,
                    "startedAt": d.get("startedAt", "?"),
                    "archivedAt": d.get("archivedAt", "?"),
                    "version": d.get("version", 0),
                    "votes": len(d.get("votes", {})),
                    "stickies": sum(len(v) for v in d.get("stickies", {}).values()),
                })
            self.send_json(sessions)

        elif path == "/api/stream":
            self._handle_sse()

        elif path in ("/", ""):
            self._serve_html("/index.html")

        elif path == "/join":
            self._serve_html("/join.html")

        elif path == "/view":
            self._serve_html("/view.html")

        else:
            super().do_GET()

    def _serve_html(self, html_path):
        """Serve HTML file with no-cache headers."""
        self.path = html_path
        f = self.send_head()
        if f:
            try:
                self.wfile.write(f.read())
            finally:
                f.close()

    def end_headers(self):
        if self.path and self.path.endswith(".html"):
            self.send_header("Cache-Control", "no-cache, no-store, must-revalidate")
            self.send_header("Pragma", "no-cache")
            self.send_header("Expires", "0")
        super().end_headers()

    def _handle_sse(self):
        self.send_response(200)
        self.send_header("Content-Type", "text/event-stream")
        self.send_header("Cache-Control", "no-cache")
        self.send_header("Connection", "keep-alive")
        self.send_header("Access-Control-Allow-Origin", "*")
        self.send_header("X-Accel-Buffering", "no")
        self.end_headers()

        q = queue.Queue()
        with sse_lock:
            sse_clients.append(q)

        with state_lock:
            init_data = json.dumps(state, ensure_ascii=False)
        self.wfile.write(f"event: init\ndata: {init_data}\n\n".encode())
        self.wfile.flush()

        try:
            while True:
                try:
                    msg = q.get(timeout=15)
                    self.wfile.write(msg)
                    self.wfile.flush()
                except queue.Empty:
                    self.wfile.write(b": heartbeat\n\n")
                    self.wfile.flush()
        except (BrokenPipeError, ConnectionResetError, OSError):
            pass
        finally:
            with sse_lock:
                if q in sse_clients:
                    sse_clients.remove(q)

    def do_POST(self):
        path = urlparse(self.path).path

        if path == "/api/update":
            length = int(self.headers.get("Content-Length", 0))
            body = json.loads(self.rfile.read(length))
            with state_lock:
                self._apply(body)
                state["version"] += 1
                save_state()
            broadcast(body)
            self.send_json({"ok": True, "version": state["version"]})

        elif path == "/api/reset":
            with state_lock:
                fname, started = archive_state()
                state.clear()
                state.update(fresh_state())
                save_state()
            broadcast({"type": "reset"})
            self.send_json({
                "ok": True,
                "archived": fname,
                "previousStartedAt": started,
                "newStartedAt": state["startedAt"],
            })

        else:
            self.send_response(404)
            self.end_headers()

    def _apply(self, update):
        t = update.get("type")

        if t == "join":
            name = update["name"]
            if name in PARTICIPANTS:
                state["participants"][name] = {
                    "color": PARTICIPANTS[name],
                    "online": True,
                    "lastSeen": time.time(),
                }

        elif t == "heartbeat":
            name = update.get("name")
            if name in state["participants"]:
                state["participants"][name]["lastSeen"] = time.time()
                state["participants"][name]["online"] = True

        elif t == "navigate":
            state["currentSlide"] = update["slide"]

        elif t == "vote":
            sid = update["id"]
            direction = update["direction"]
            author = update.get("author", "")
            if sid not in state["votes"]:
                state["votes"][sid] = {}
            state["votes"][sid][author] = direction

        elif t == "unvote":
            sid = update["id"]
            author = update.get("author", "")
            if sid in state["votes"] and author in state["votes"][sid]:
                del state["votes"][sid][author]

        elif t == "sticky_add":
            zone = update["zone"]
            if zone not in state["stickies"]:
                state["stickies"][zone] = {}
            state["stickies"][zone][update["id"]] = {
                "text": update.get("text", ""),
                "color": update["color"],
                "author": update.get("author", ""),
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
    PORT = 8082
    ip = get_local_ip()
    os.chdir(V2_DIR)
    server = ThreadingHTTPServer(("0.0.0.0", PORT), Handler)

    print()
    print("  ╔═══════════════════════════════════════════════╗")
    print("  ║  Koersbepaling v2 — Multi-user Server         ║")
    print("  ╠═══════════════════════════════════════════════╣")
    print(f"  ║  Facilitator: http://{ip}:{PORT}/             ║")
    print(f"  ║  Deelnemers:  http://{ip}:{PORT}/join         ║")
    print("  ║  Druk Ctrl+C om te stoppen                    ║")
    print("  ╚═══════════════════════════════════════════════╝")
    print()

    try:
        server.serve_forever()
    except KeyboardInterrupt:
        print("\n  Server gestopt. State opgeslagen.")
        server.shutdown()
