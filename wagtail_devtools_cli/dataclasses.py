from dataclasses import dataclass, field

import requests


@dataclass
class Item:
    session: requests.Session
    group: str
    name: str
    url: str
    url_status_code: int = 0

    def __post_init__(self):
        self._process_url()

    def _process_url(self):
        response = self.session.get_response(self.url)
        self.url_status_code = response.status_code


@dataclass
class Report:
    items: list = field(default_factory=list)

    def get_errors_500(self):
        error_500 = []
        for item in self.items:
            if item.url_status_code == 500:
                error_500.append(item)
        return error_500

    def get_errors_404(self):
        error_404 = []
        for item in self.items:
            if item.url_status_code == 404:
                error_404.append(item)
        return error_404

    def get_errors_302(self):
        error_302 = []
        for item in self.items:
            if item.url_status_code == 302:
                error_302.append(item)
        return error_302

    def get_success_200(self):
        success = []
        for item in self.items:
            if item.url_status_code == 200:
                success.append(item)
        return success
