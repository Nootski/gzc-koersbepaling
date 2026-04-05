import json
import os
import sys
import threading
from http.server import ThreadingHTTPServer
from urllib.request import Request, urlopen

sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))

import server  # noqa: E402


def _start_server(port=0):
    """Start the server on a random free port and return (httpd, port)."""
    server.state = server.load_state.__wrapped__() if hasattr(server.load_state, "__wrapped__") else {
        "votes": {}, "stickies": {}, "texts": {}, "participants": {}, "version": 0
    }
    httpd = ThreadingHTTPServer(("127.0.0.1", port), server.Handler)
    actual_port = httpd.server_address[1]
    t = threading.Thread(target=httpd.serve_forever, daemon=True)
    t.start()
    return httpd, actual_port


def _get(port, path):
    r = urlopen(f"http://127.0.0.1:{port}{path}")
    return json.loads(r.read())


def _post(port, path, data):
    body = json.dumps(data).encode()
    req = Request(f"http://127.0.0.1:{port}{path}", data=body, headers={"Content-Type": "application/json"})
    r = urlopen(req)
    return json.loads(r.read())


class TestServerAPI:
    def setup_method(self):
        server.STATE_FILE = "/tmp/heidedag_test_state.json"
        if os.path.exists(server.STATE_FILE):
            os.remove(server.STATE_FILE)
        server.state = {"votes": {}, "stickies": {}, "texts": {}, "participants": {}, "version": 0}
        self.httpd, self.port = _start_server()

    def teardown_method(self):
        self.httpd.shutdown()
        if os.path.exists(server.STATE_FILE):
            os.remove(server.STATE_FILE)

    def test_get_state_returns_empty(self):
        data = _get(self.port, "/api/state")
        assert data["votes"] == {}
        assert data["stickies"] == {}
        assert data["texts"] == {}

    def test_vote_increments(self):
        result = _post(self.port, "/api/update", {"type": "vote", "id": "s1", "direction": "up"})
        assert result["ok"] is True
        state = _get(self.port, "/api/state")
        assert state["votes"]["s1"]["up"] == 1

    def test_vote_multiple(self):
        _post(self.port, "/api/update", {"type": "vote", "id": "s1", "direction": "up"})
        _post(self.port, "/api/update", {"type": "vote", "id": "s1", "direction": "up"})
        _post(self.port, "/api/update", {"type": "vote", "id": "s1", "direction": "down"})
        state = _get(self.port, "/api/state")
        assert state["votes"]["s1"]["up"] == 2
        assert state["votes"]["s1"]["down"] == 1

    def test_unvote_decrements(self):
        _post(self.port, "/api/update", {"type": "vote", "id": "s1", "direction": "up"})
        _post(self.port, "/api/update", {"type": "vote", "id": "s1", "direction": "up"})
        _post(self.port, "/api/update", {"type": "unvote", "id": "s1", "direction": "up"})
        state = _get(self.port, "/api/state")
        assert state["votes"]["s1"]["up"] == 1

    def test_unvote_does_not_go_below_zero(self):
        _post(self.port, "/api/update", {"type": "vote", "id": "s2", "direction": "down"})
        _post(self.port, "/api/update", {"type": "unvote", "id": "s2", "direction": "down"})
        _post(self.port, "/api/update", {"type": "unvote", "id": "s2", "direction": "down"})
        state = _get(self.port, "/api/state")
        assert state["votes"]["s2"]["down"] == 0

    def test_text_update(self):
        _post(self.port, "/api/update", {"type": "text", "id": "principle-org", "value": "Wij organiseren..."})
        state = _get(self.port, "/api/state")
        assert state["texts"]["principle-org"] == "Wij organiseren..."

    def test_text_overwrite(self):
        _post(self.port, "/api/update", {"type": "text", "id": "p1", "value": "eerste"})
        _post(self.port, "/api/update", {"type": "text", "id": "p1", "value": "tweede"})
        state = _get(self.port, "/api/state")
        assert state["texts"]["p1"] == "tweede"

    def test_sticky_add(self):
        _post(self.port, "/api/update", {
            "type": "sticky_add", "zone": "checkin", "id": "s-123",
            "text": "Hallo", "color": "#FFF9C4", "author": "Maat 1", "authorColor": "#4CAF50"
        })
        state = _get(self.port, "/api/state")
        assert "s-123" in state["stickies"]["checkin"]
        assert state["stickies"]["checkin"]["s-123"]["text"] == "Hallo"

    def test_sticky_update(self):
        _post(self.port, "/api/update", {
            "type": "sticky_add", "zone": "z1", "id": "s-1",
            "text": "", "color": "yellow", "author": "", "authorColor": ""
        })
        _post(self.port, "/api/update", {"type": "sticky_update", "zone": "z1", "id": "s-1", "text": "Bijgewerkt"})
        state = _get(self.port, "/api/state")
        assert state["stickies"]["z1"]["s-1"]["text"] == "Bijgewerkt"

    def test_sticky_delete(self):
        _post(self.port, "/api/update", {
            "type": "sticky_add", "zone": "z1", "id": "s-del",
            "text": "weg", "color": "yellow", "author": "", "authorColor": ""
        })
        _post(self.port, "/api/update", {"type": "sticky_delete", "zone": "z1", "id": "s-del"})
        state = _get(self.port, "/api/state")
        assert "s-del" not in state["stickies"].get("z1", {})

    def test_join(self):
        _post(self.port, "/api/update", {"type": "join", "name": "Maat 1", "color": "#4CAF50"})
        state = _get(self.port, "/api/state")
        assert "Maat 1" in state["participants"]

    def test_version_increments(self):
        r1 = _post(self.port, "/api/update", {"type": "text", "id": "x", "value": "a"})
        r2 = _post(self.port, "/api/update", {"type": "text", "id": "x", "value": "b"})
        assert r2["version"] > r1["version"]

    def test_state_persisted_to_file(self):
        _post(self.port, "/api/update", {"type": "text", "id": "persist", "value": "test"})
        assert os.path.exists(server.STATE_FILE)
        with open(server.STATE_FILE) as f:
            data = json.load(f)
        assert data["texts"]["persist"] == "test"

    def test_html_served_at_root(self):
        from urllib.request import urlopen
        r = urlopen(f"http://127.0.0.1:{self.port}/")
        assert r.status == 200
        body = r.read().decode()
        assert "Koersbepaling" in body
