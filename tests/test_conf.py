import requests


def test_mock_server(mock_server):
    host = f"http://{mock_server.server_address[0]}:{mock_server.server_address[1]}"
    response = requests.get(host)
    assert response.status_code == 200
    assert response.text == "This is a mock response"
    assert response.cookies["csrftoken"] == "FaketokeN"

    response = requests.post(
        host,
        data={
            "username": "test",
            "password": "test",
            "csrfmiddlewaretoken": "FaketokeN",
        },
    )
    assert response.status_code == 302
    assert response.cookies["sessionid"] == "FakeSession"

    response = requests.get(f"{host}/not-a-path/")
    assert response.status_code == 404

    response = requests.get(f"{host}/exposapi/")
    assert response.status_code == 200
    assert response.json() == [
        {
            "group": "AdminEditPage",
            "name": "HomePage (sandbox_home)",
            "url": "http://localhost:8888/admin/pages/3/edit/",
        },
    ]

    response = requests.get(f"{host}/exposapi/?all=1")
    assert response.status_code == 200
    assert response.json() == [
        {
            "group": "AdminEditPage1",
            "name": "HomePage (sandbox_home)",
            "url": "http://localhost:8888/admin/pages/3/edit/",
        },
        {
            "group": "AdminEditPage2",
            "name": "HomePage (sandbox_home)",
            "url": "http://localhost:8888/admin/pages/4/edit/",
        },
    ]

    response = requests.get(f"{host}/failed-login/")
    assert response.status_code == 401
