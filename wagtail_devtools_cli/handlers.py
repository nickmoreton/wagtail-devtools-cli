import requests


class RequestHandler:
    def __init__(self, url, login_path="/admin/login/"):
        self.url = url
        self._is_authenticated = False
        self.login_url = f"{self.url}/{login_path.strip(" / ")}/"
        self.session = requests.Session()

    def login(self, username, password):
        try:
            login_form = self.session.get(self.login_url)
            if login_form.status_code == 404:
                raise Exception("Login page not found")
        except requests.exceptions.ConnectionError:
            exit(
                "Connection error: please check the URL and make sure the server is running"
            )  # pragma: no cover

        user = {
            "username": username,
            "password": password,
            "csrfmiddlewaretoken": login_form.cookies["csrftoken"],
        }
        self.session.post(self.login_url, data=user)
        # if the sessionid cookie is set, the user is authenticated
        if self.session.cookies.get("sessionid"):
            self._is_authenticated = True
        return self

    def get_response(self, url):
        response = self.session.get(url)
        return response

    def is_authenticated(self):
        return self._is_authenticated

    def logout(self):
        self._is_authenticated = False
        # clear the cookies to completely log out
        self.session.cookies.clear()
        del self.session
        return self
