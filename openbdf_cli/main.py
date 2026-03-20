from enum import Enum
from pathlib import Path
from typing import Optional

import typer
from eralchemy2 import render_er
from model.general_info import SQLModel
from typing_extensions import Annotated

app = typer.Typer(help="CLI utilities for the project.")


@app.command()
def hello(name: str):
    print(f"Hello {name}")


@app.command()
def render_model(
    output: Annotated[
        Path,
        typer.Argument(help="Output file path, e.g. schema_graph.png"),
    ],
):
    """
    Render the SQLModel metadata as an ER diagram.
    """

    render_er(SQLModel.metadata, str(output))
    typer.echo(f"ER diagram written to {output}")


@app.command(name="explain")
def explain(
    target: str = typer.Option(..., "--target", "-t", help="The data model class name"),
    field: list[str] = typer.Option(
        None,
        "--field",
        "-f",
        help="The specific field key(s) to explain. If omitted, all fields are shown.",
    ),
    output: Optional[Path] = typer.Option(
        None,
        "--output",
        "-o",
        help="Optional output file path to save the explanation as Markdown. If none provided, prints to the console directly.",
    ),
):
    """
    Explain the metadata of a specific field (or all fields) in a model.
    Usage:
      openbdf explain --target ProjectRecordBase --field project_name
      openbdf explain --target ProjectRecordBase
    """
    from cli.explain import analyze_model, generate_markdown, print_to_console

    # field will be None if the option is not provided,
    # or a list of strings if one or more are provided.
    analysis = analyze_model(target, field)

    if output:
        markdown_content = generate_markdown(analysis)
        with open(output, "w") as f:
            f.write(markdown_content)
    else:
        print_to_console(analysis)


if __name__ == "__main__":
    app()
