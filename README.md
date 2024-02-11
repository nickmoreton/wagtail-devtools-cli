# Wagtail Devtools Cli

A command line tool for generating reports about a Wagtail CMS project.

## Installation

Clone this repo to a location on your computer and cd into the directory you cloned it to.

Run:

```bash
poetry install
poetry shell
```

## Report Types

**Note:** Requires the following package to be installed on the target project: [Wagtail Exposapi](https://github.com/wagtail-packages/wagtail-exposapi) or a JSON API endpoint that returns the same data structures.

### Responses

Runs a get request on each endpoint exposed by an API endpoint

#### Usage

Run the following command to start the report:

```bash
poetry run cli
```

#### Options

Options are available to customize it's behavior:

```bash
poetry run cli --help
```
