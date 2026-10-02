# OpenBDF

_Schema and parser for the Open Building Data Format (OpenBDF) developed by GBDI_


# 🐇 Quick start

## Requirements

- [uv](https://docs.astral.sh/uv/) Python package and project manager
- Make


## Installation

```bash
make install
```


## Usage

```bash
uv run openbdf --help
```

To convert project files into an openbdf file (`output.xslx`), run (COLA example):
```
uv run openbdf open \
  path/to/cola_file.xlsx \
  path/to/cola_general_info.xlsx \
  -t translators/translator_at_v2.0.0.xlsx
  -t translators/translator_bec_at_v2.0.0.xlsx
  --drop-invalid-materials
  -o output.xslx
```
It will list potential validation errors, that prevent the export. To export anyway in case of errors, append the option `--draft`.

> [!NOTE] Multiple translator files can be merged with a single command, as shown above. When two files translate the same category, the last file wins.

## LCA results model classes

The tall and wide LCA result model classes (`lca_results_full_tall.py` and `lca_results_full_wide.py`) are generated from the data registry in `openbdf/model/lca_results.py`. Do not edit the generated files by hand.

To regenerate them after changing the registry, run:

```bash
make generate-lca-results-classes
```

To verify the generated files are up to date without writing them, run:

```bash
make check-lca-results-classes
```

The test `tests/test_generated_lca_results_classes.py` also checks that the committed generated files stay in sync with the registry.
