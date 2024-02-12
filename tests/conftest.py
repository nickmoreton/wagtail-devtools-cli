import json
import threading

from http.server import BaseHTTPRequestHandler, HTTPServer

import pytest


class MockServer(BaseHTTPRequestHandler):
    """A mock server to use when testing requests."""

    def _set_headers_get(self, status_code=200, content_type="text/plain"):
        # Set the headers for a GET request
        self.send_response(status_code)
        self.send_header(
            "Set-Cookie",
            "csrftoken=FaketokeN; Path=/; Secure; HttpOnly",
        )
        self.send_header("Content-type", content_type)
        self.end_headers()

    def _set_headers_post(self, status_code=302, content_type="text/plain"):
        # Set the headers for a POST request
        self.send_response(status_code)
        self.send_header(
            "Set-Cookie",
            "sessionid=FakeSession; Path=/; Secure; HttpOnly",
        )
        self.send_header("Content-type", content_type)
        self.send_header("Content-Length", 0)  # avoids "Connection reset by peer" error
        self.end_headers()

    def do_GET(self):
        if self.path == "/not-a-path/":
            self._set_headers_get(404)
            self.wfile.write("Not Found".encode("utf-8"))
            return
        if self.path == "/exposapi/":
            data = [
                {
                    "group": "AdminEditPage",
                    "name": "HomePage (sandbox_home)",
                    "url": "http://localhost:8000/admin/pages/3/edit/",
                },
            ]
            self._set_headers_get()
            self.wfile.write(json.dumps(data).encode("utf-8"))
            return
        if self.path == "/failed-login/":
            self._set_headers_get(401)
            self.wfile.write("Not Authenticated".encode("utf-8"))
            return
        self._set_headers_get()
        self.wfile.write("This is a mock response".encode("utf-8"))

    def do_POST(self):
        self._set_headers_post()
        self.wfile.write("Logged In".encode("utf-8"))


def start_mock_server(port=8888):
    # Start the mock server
    server_address = ("localhost", port)
    httpd = HTTPServer(server_address, MockServer)
    thread = threading.Thread(target=httpd.serve_forever)
    thread.daemon = True
    thread.start()
    return httpd


def stop_mock_server(httpd):
    # Stop the mock server
    httpd.shutdown()
    httpd.server_close()


@pytest.fixture()
def mock_server(scope="session"):
    # Use this fixture as a parameter in your tests to start and stop the mock server
    server = start_mock_server()
    yield server
    stop_mock_server(server)
