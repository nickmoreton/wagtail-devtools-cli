from rich import box
from rich.table import Table


BOX = box.MARKDOWN
STYLE_OK = "green1"
STYLE_ERROR = "red1"
STYLE_WARNING = "gold1"
STYLE_INFO = "dark_orange"
BASE_COLUMN = "URL\nGroup | Name"
TABLE_FORMAT = {
    "box": BOX,
    "show_lines": True,
    "expand": True,
}


def rich_result_row(result):
    return f"{result.url}\n{result.group} | {result.name}"


def rich_table(title, caption, style, items):
    table = Table(title=title, caption=caption, style=style, **TABLE_FORMAT)
    table.add_column(BASE_COLUMN)

    for result in items:
        table.add_row(rich_result_row(result))

    return table
