from dataclasses import dataclass
from unittest.mock import Mock

import pytest

from rich import box

from wagtail_devtools_cli.cli import Item
from wagtail_devtools_cli.helpers import (
    BASE_COLUMN,
    BOX,
    STYLE_ERROR,
    STYLE_INFO,
    STYLE_OK,
    STYLE_WARNING,
    TABLE_FORMAT,
    rich_result_row,
    rich_table,
)


def test_constants():
    assert isinstance(BOX, box.Box)
    assert STYLE_OK == "green1"
    assert STYLE_ERROR == "red1"
    assert STYLE_WARNING == "gold1"
    assert STYLE_INFO == "dark_orange"
    assert BASE_COLUMN == "URL\nGroup | Name"
    assert TABLE_FORMAT == {
        "box": BOX,
        "show_lines": True,
        "expand": True,
    }


class MockItem:
    url = "http://example.com"
    group = "group"
    name = "name"


def test_rich_result_row():
    assert rich_result_row(MockItem) == "http://example.com\n" "group | name"


def test_rich_table():
    items = [MockItem, MockItem]
    title = "title"
    caption = "caption"
    style = "style"
    table = rich_table(title, caption, style, items)
    assert table.title == title
    assert table.caption == caption
    assert table.style == style
    assert table.row_count == 2


def test_rich_table_no_items():
    items = []
    title = "title"
    caption = "caption"
    style = "style"
    table = rich_table(title, caption, style, items)
    assert table.title == title
    assert table.caption == caption
    assert table.style == style
    assert table.row_count == 0


@dataclass
class MockResponse:
    status_code: int


@pytest.fixture
def mock_session():
    mock_session = Mock()
    mock_session.get_response.return_value = MockResponse(status_code=200)
    return mock_session


def test_item_url_status_code(mock_session):
    item = Item(
        session=mock_session,
        group="TestGroup",
        name="TestItem",
        url="http://example.com",
    )
    assert item.url_status_code == 200
