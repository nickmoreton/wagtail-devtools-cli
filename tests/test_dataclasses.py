from dataclasses import dataclass

from wagtail_devtools_cli.cli import Report


@dataclass
class MockItem200:
    group: str = "TestGroup"
    name: str = "TestItem"
    url: str = "http://example.com"
    url_status_code: int = 200


@dataclass
class MockItem404:
    group: str = "TestGroup"
    name: str = "TestItem"
    url: str = "http://example.com"
    url_status_code: int = 404


@dataclass
class MockItem500:
    group: str = "TestGroup"
    name: str = "TestItem"
    url: str = "http://example.com"
    url_status_code: int = 500


@dataclass
class MockItem302:
    group: str = "TestGroup"
    name: str = "TestItem"
    url: str = "http://example.com"
    url_status_code: int = 302


def test_report_get_errors_500():
    report = Report(items=[MockItem200, MockItem404, MockItem500, MockItem302])
    assert report.get_errors_500() == [MockItem500]
    assert report.get_errors_500() != [MockItem200, MockItem404, MockItem302]


def test_report_get_errors_404():
    report = Report(items=[MockItem200, MockItem404, MockItem500, MockItem302])
    assert report.get_errors_404() == [MockItem404]
    assert report.get_errors_404() != [MockItem200, MockItem500, MockItem302]


def test_report_get_errors_302():
    report = Report(items=[MockItem200, MockItem404, MockItem500, MockItem302])
    assert report.get_errors_302() == [MockItem302]
    assert report.get_errors_302() != [MockItem200, MockItem404, MockItem500]


def test_report_get_success_200():
    report = Report(items=[MockItem200, MockItem404, MockItem500, MockItem302])
    assert report.get_success_200() == [MockItem200]
    assert report.get_success_200() != [MockItem404, MockItem500, MockItem302]
