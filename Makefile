# Detect operating system
OS := $(shell uname)

# Set Graphviz environment variables only for macOS
ifeq ($(OS),Darwin)
	GRAPHVIZ_CFLAGS := -I$(shell brew --prefix graphviz)/include
	GRAPHVIZ_LDFLAGS := -L$(shell brew --prefix graphviz)/lib
	MAC_ENV := CFLAGS="$(GRAPHVIZ_CFLAGS)" LDFLAGS="$(GRAPHVIZ_LDFLAGS)"
else
	MAC_ENV :=
endif

install:
	$(MAC_ENV) uv sync --all-extras
	uv run pre-commit install

lint:
	uv run pre-commit run --all-files

build:
	uv run python -m build

test:
	uv run pytest
