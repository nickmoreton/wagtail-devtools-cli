import pytest
import requests
from http.server import BaseHTTPRequestHandler, HTTPServer
import threading

from wagtail_devtools_cli.handlers import RequestHandler

def test_request_handler_login(mock_server):
    host = f"http://{mock_server.server_address[0]}:{mock_server.server_address[1]}"
    handler = RequestHandler(host)
    handler.login("test", "test")
    assert handler.is_authenticated() == True
    handler.logout()
    assert handler.is_authenticated() == False


def test_request_handler_404(mock_server):
    host = f"http://{mock_server.server_address[0]}:{mock_server.server_address[1]}"
    handler = RequestHandler(host, login_path="/not-a-path/")
    with pytest.raises(Exception) as e_info:
        handler.login("test", "test")
    assert str(e_info.value) == "Login page not found"

def test_request_handler_get_response(mock_server):
    host = f"http://{mock_server.server_address[0]}:{mock_server.server_address[1]}"
    handler = RequestHandler(host)
    handler.login("test", "test")
    response = handler.get_response(host)
    assert response.status_code == 200
    assert response.text == "This is a mock response"

