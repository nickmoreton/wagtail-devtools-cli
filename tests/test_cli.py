from operator import contains

from click.testing import CliRunner

from wagtail_devtools_cli.cli import main, print_report
from wagtail_devtools_cli.dataclasses import Item, Report


def test_main(mock_server):
    host = f"http://{mock_server.server_address[0]}:{mock_server.server_address[1]}"
    runner = CliRunner()
    result = runner.invoke(main, ["--host", host])

    assert result.exit_code == 0


def test_main_expanded(mock_server):
    host = f"http://{mock_server.server_address[0]}:{mock_server.server_address[1]}"
    runner = CliRunner()
    result = runner.invoke(main, ["--expanded", True, "--host", host])

    assert result.exit_code == 0


def test_not_authenticated(mock_server):
    host = f"http://{mock_server.server_address[0]}:{mock_server.server_address[1]}"
    runner = CliRunner()
    result = runner.invoke(main, ["--host", f"{host}/failed-login/"])

    assert result.exit_code == 1


def test_404(mock_server):
    host = f"http://{mock_server.server_address[0]}:{mock_server.server_address[1]}"
    runner = CliRunner()
    result = runner.invoke(main, ["--host", f"{host}/not-a-path/"])

    assert result.exit_code == 1


class MockItem(Item):
    session: object
    group: str
    name: str
    url: str
    url_status_code: int = 0

    def __post_init__(self):
        pass


def test_print_report(capfd):
    """
    Test the print_report function
    """

    print_report(
        Report(
            items=[
                MockItem(
                    session=object,
                    group="Pages",
                    name="Page 1",
                    url="http://localhost:8000/admin/pages/1/",
                    url_status_code=200,
                ),
                MockItem(
                    session=object,
                    group="Pages",
                    name="Page 2",
                    url="http://localhost:8000/admin/pages/2/",
                    url_status_code=404,
                ),
                MockItem(
                    session=object,
                    group="Pages",
                    name="Page 3",
                    url="http://localhost:8000/admin/pages/3/",
                    url_status_code=500,
                ),
                MockItem(
                    session=object,
                    group="Pages",
                    name="Page 4",
                    url="http://localhost:8000/admin/pages/4/",
                    url_status_code=302,
                ),
            ]
        ),
        expanded=True,
    )

    out, err = capfd.readouterr()

    assert contains(out, "These are the 200 success that were found")
    assert contains(out, "These are the 404 errors that were found")
    assert contains(out, "These are the 500 errors that were found")
    assert contains(out, "These are the 302 errors that were found")
