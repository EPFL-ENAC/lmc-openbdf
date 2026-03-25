install:
	uv sync --all-extras
	uv run pre-commit install

lint:
	uv run pre-commit run --all-files

build:
	uv run python -m build

test:
	uv run --extra dev pytest
