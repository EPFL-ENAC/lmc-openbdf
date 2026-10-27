.PHONY: help set-version translators translator-csv
help: ## Show available targets
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | awk 'BEGIN {FS = ":.*?## "}; {printf "\033[36m%-20s\033[0m %s\n", $$1, $$2}'

install: ## Install with uv sync and pre-commit
	uv sync --all-extras
	uv run pre-commit install

lint: ## Run pre-commit on all files
	uv run pre-commit run --all-files

build: ## Run python -m build
	uv run python -m build

translators: ## Build the translator in .xslx from the committed .csv directories
	@mkdir -p build/translators
	uv run --extra cli openbdf save-bec-template build/translators/translator_bec_template.xlsx
	uv run --extra cli openbdf save-bmc-template build/translators/translator_bmc_template.xlsx
	uv run --extra cli openbdf csv-to-translator translators/translator_at build/translators/translator_at.xlsx
	uv run --extra cli openbdf csv-to-translator translators/translator_bec_at build/translators/translator_bec_at.xlsx
	uv run --extra cli openbdf csv-to-translator translators/translator_bmc_at build/translators/translator_bmc_at.xlsx

translator-csv: ## Convert an .xslx translator to a .csv directory: make translator-csv IN=<xlsx> OUT=<dir>
	@if [ -z "$(IN)" ] || [ -z "$(OUT)" ]; then echo "usage: make translator-csv IN=translator.xlsx OUT=translator_dir" >&2; exit 1; fi
	uv run --extra cli openbdf translator-to-csv "$(IN)" "$(OUT)"

test: ## Run pytest
	uv run --extra dev --extra cli pytest

generate-lca-results-classes: ## Generate LCA classes modules
	uv run --extra dev python scripts/generate_lca_results_classes.py

check-lca-results-classes: ## Check LCA classes modules
	uv run --extra dev python scripts/generate_lca_results_classes.py --check

erd: ## regenerate docs/src/developer/erd.md's Mermaid ER diagram from the SQLModel tables
	uv run python scripts/generate_erd.py > docs/src/developer/erd.md

set-version: ## Set the template version in about.md, the release workflow and the README
	@uv run python scripts/set_template_version.py $(filter-out $@,$(MAKECMDGOALS))

v%:
	@:
