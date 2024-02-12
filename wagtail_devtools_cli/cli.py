import click

from rich.console import Console

from wagtail_devtools_cli.dataclasses import Item, Report
from wagtail_devtools_cli.handlers import RequestHandler
from wagtail_devtools_cli.helpers import (
    STYLE_ERROR,
    STYLE_INFO,
    STYLE_OK,
    STYLE_WARNING,
    rich_table,
)


console = Console()  # Initialize the console for all output


@click.command()
@click.option(
    "-u",
    "--url",
    default="http://localhost:8000",
    help="The URL of the Wagtail project to be checked",
)
@click.option(
    "-a",
    "--all",
    is_flag=True,
    help="Query all records (default: False)",
)
@click.option(
    "-e", "--expanded", is_flag=True, help="Show expanded output (default: False)"
)
@click.option(
    "-u",
    "--username",
    default="superuser",
    help="The username to use for authentication (default: superuser)",
)
@click.option(
    "-p",
    "--password",
    default="superuser",
    help="The password to use for authentication (default: superuser)",
)
@click.option(
    "-t",
    "--endpoint",
    default="exposapi",
    help="The endpoint to query for records (default: exposapi)",
)
@click.option(
    "-l",
    "--login-path",
    default="/admin/login/",
    help="The path to the login page (default: /admin/login/)",
)
def main(url, all, expanded, username, password, endpoint, login_path):
    """A CLI tool for reporting errors in Wagtail projects

    It does this by querying the wagtail-exposapi endpoint and checking
    the status code of the URLs returned.

    arg: url (str) (The URL of the Wagtail project to be checked)

    """

    # Authenticate a user
    request_handler = RequestHandler(url, login_path)
    request_handler.login(username, password)

    if not request_handler.is_authenticated():  # pragma: no cover
        console.print(
            "Not authenticated: please check your username and password", style="red1"
        )
        return

    console.print("Authenticated 🔓", style="green1")
    console.print("Querying the wagtail-exposapi endpoint...", style="orange1")

    # Query the endpoint
    endpoint = endpoint.strip("/")
    index_endpoint = url + f"/{endpoint}/"

    if all:
        response = request_handler.get_response(index_endpoint + "?all=true")
    else:
        response = request_handler.get_response(index_endpoint)

    if response.status_code == 404:  # pragma: no cover
        console.print("Endpoint not found", style="red1")
        return

    # Process the results
    results = [e for e in response.json()]
    report = Report()

    for result in results:
        item = Item(request_handler, **result)
        report.items.append(item)

    if request_handler.is_authenticated():
        request_handler.logout()
        console.print("Logged out")

    console.print("")
    console.print(f"Found {len(results)} records")
    console.print("Processing results...", style="orange1")
    print_report(report, expanded)


def print_report(report, expanded):
    # Print the report
    if report.get_success_200() and expanded:
        console.print(
            rich_table(
                title=f"200 Success #{len(report.get_success_200())}",
                caption="These are the 200 success that were found (cmd/ctrl + click to open links in browser)",
                style=STYLE_OK,
                items=report.get_success_200(),
            )
        )
        click.echo("\n")

    if report.get_errors_500():
        console.print(
            rich_table(
                title=f"500 Errors #{len(report.get_errors_500())}",
                caption="These are the 500 errors that were found (cmd/ctrl + click to open links in browser)",
                style=STYLE_ERROR,
                items=report.get_errors_500(),
            )
        )
        click.echo("\n")

    if report.get_errors_404():
        console.print(
            rich_table(
                title=f"404 Errors #{len(report.get_errors_404())}",
                caption="These are the 404 errors that were found (cmd/ctrl + click to open links in browser)",
                style=STYLE_WARNING,
                items=report.get_errors_404(),
            )
        )
        click.echo("\n")

    if report.get_errors_302():
        console.print(
            rich_table(
                title=f"302 Errors #{len(report.get_errors_302())}",
                caption="These are the 302 errors that were found (cmd/ctrl + click to open links in browser)",
                style=STYLE_INFO,
                items=report.get_errors_302(),
            )
        )
        click.echo("\n")
