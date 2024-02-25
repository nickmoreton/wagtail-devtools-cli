# Contribute to the project

Contributions to the project are welcome.

## Development Setup

It's recommended to use [Poetry](https://python-poetry.org/) to manage the project's dependencies.

```bash
poetry install
poetry shell
```

## Testing

The project uses [pytest](https://docs.pytest.org/en/stable/) for testing.

```bash
pytest
```

or to run the tests with coverage:

```bash
pytest --cov=./
```

## Linting & Formatting

The project uses [black](https://black.readthedocs.io/en/stable/) for formatting and [flake8](https://flake8.pycqa.org/en/latest/) for linting as well as [isort](https://pycqa.github.io/isort/) for sorting imports.

Pre-commit hooks are set up to run these tools before each commit.

To run these tools manually:

```bash
pre-commit run --all-files
```

or better still install the pre-commit hooks before you commit any changes:

```bash
pre-commit install
```
