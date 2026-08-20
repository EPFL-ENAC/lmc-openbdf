# OpenBDF

_Schema and parser for GBDI's OpenBDF format_


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
  path/to/cola_building_information.xlsx \
  -t translators/translator_cola.xlsx
  -o output.xslx
```
It will list potential validation errors, that prevent the export. To export anyway in case of errors, append the option `--draft`.
