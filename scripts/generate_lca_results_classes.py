from __future__ import annotations

from pathlib import Path

import typer

from openbdf.model import lca_results

app = typer.Typer(help="Generate the LCA results model classes from the data registry.")


def _model_dir() -> Path:
    """Directory that holds the generated LCA result model modules."""
    return Path(lca_results.__file__).resolve().parent


@app.command(name="generate")
def generate(
    check: bool = typer.Option(
        False,
        "--check",
        help="Verify the generated files are up to date instead of writing them. "
        "Exits with a non-zero code if any file is out of date.",
    ),
) -> None:
    """
    Regenerate the tall and wide LCA result model classes.
    Usage:
        generate
        generate --check
    """
    for filename, render in lca_results.GENERATED_MODULES:
        target = _model_dir() / filename
        content = lca_results.format_module_source(render())

        if check:
            existing = target.read_text(encoding="utf-8")
            if existing != content:
                typer.echo(
                    f"Out of date: {target}. Run: make generate-lca-results-classes",
                    err=True,
                )
                raise typer.Exit(code=1)
            typer.echo(f"Up to date: {filename}")
        else:
            target.write_text(content, encoding="utf-8")
            typer.echo(f"Generated: {filename}")


if __name__ == "__main__":
    app()
