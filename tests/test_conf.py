import pytest
import requests


def test_mock_server(mock_server):
    response = requests.get("http://localhost:8888")
    assert response.status_code == 200
    assert response.text == "This is a mock response"
    assert response.cookies["csrftoken"] == "FaketokeN"

    response = requests.post("http://localhost:8888", data={"username": "test", "password": "test", "csrfmiddlewaretoken": "FaketokeN"})
    assert response.status_code == 302
    assert response.cookies["sessionid"] == "FakeSession"
    
    response = requests.get("http://localhost:8888/not-a-path/")
    assert response.status_code == 404

    response = requests.get("http://localhost:8888/exposapi/")
    assert response.status_code == 200
    assert response.json() == [
        {
            "group": "AdminEditPage",
            "name": "HomePage (sandbox_home)",
            "url": "http://localhost:8000/admin/pages/3/edit/",
        },
    ]

    response = requests.get("http://localhost:8888/failed-login/")
    assert response.status_code == 401
    
