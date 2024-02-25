# Wagtail Devtools Cli

A CLI that interacts with a JSON API endpoint of a Wagtail project to generate reports about the project.

## Requirements

- The target project needs to have the [Wagtail Exposapi](https://github.com/wagtail-packages/wagtail-exposapi) package installed.
- Poetry is installed on your local machine or you have the ability to run the CLI in a virtual environment, a requirements.txt file is also provided for pip usage.

## Installation

The CLI runs on your local machine and requires Python 3.8 or higher.

Clone this repo to a location on your computer and cd into the directory you cloned it to.

Install the dependencies and activate the virtual environment:

Using Poetry:

```bash
poetry install
poetry shell
```

Using Pip

```bash
python3 -m venv venv
pip install -r requirements.txt
source venv/bin/activate
```

Copy the `.env.example` file to `.env`

```bash
cp .env.example .env
```

and update the values to match your project.

## Report Types

### Checks Responses

Runs a get request on each endpoint exposed by the JSON API and reports on the response status code.

Run the following command to run the report:

Using Poetry:

```bash
poetry run cli
```

Using Pip:

```bash
python -m wagtail_devtools_cli.cli
```

If any responses other than 200 are received, the CLI will output details about the endpoint and the response status code. This will generally happen for status codes of 400, 300, 500.

#### Options

Options are available to customize it's behavior:

```bash
poetry run cli --help
# or
python -m wagtail_devtools_cli.cli --help
```

The vars in the .env file can be overridden by passing the following options:

- `--host` - The host of the Wagtail project
- `--all` - Run the report on all endpoints (this is passed to the JSON API endpoint as a query parameter)
- `--expanded` - Show the response for all endpoints, including those that return a 200 status code
- `--username` - The username to use for authentication on the target Wagtail project
- `--password` - The password to use for authentication on the target Wagtail project
- `--endpoint` - The endpoint where the JSON API is exposed on the target Wagtail project
- `--login-path` - The path to the login page on the target Wagtail project

## Contribute to the project

Contributions to the project are welcome. To contribute, please read the [CONTRIBUTING.md](docs/CONTRIBUTING.md) file.
