install:
	uv sync --all-extras
	uv run pre-commit install

lint:
	uv run pre-commit run --all-files

build:
	uv run python -m build

test:
	uv run --extra dev pytest

generate-lca-results-classes:
	uv run --extra dev python scripts/generate_lca_results_classes.py

check-lca-results-classes:
	uv run --extra dev python scripts/generate_lca_results_classes.py --check
