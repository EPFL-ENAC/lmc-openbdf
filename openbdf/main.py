from pathlib import Path

import typer

from openbdf.cli.open import open_openbdf_xlsx
from openbdf.cli.save import save_openbdf_to_xlsx, save_translator

app = typer.Typer(help="CLI utilities for the project.")


@app.command(name="explain", no_args_is_help=True)
def explain(
    target: str = typer.Option(..., "--target", "-t", help="The data model class name"),
    field: list[str] = typer.Option(
        None,
        "--field",
        "-f",
        help="The specific field key(s) to explain. If omitted, all fields are shown.",
    ),
    output: Path | None = typer.Option(
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
    from openbdf.cli.explain import analyze_model, generate_markdown, print_to_console

    # field will be None if the option is not provided,
    # or a list of strings if one or more are provided.
    analysis = analyze_model(target, field)

    if output:
        markdown_content = generate_markdown(analysis)

        absolute_path = output.expanduser().resolve()
        absolute_path.write_text(markdown_content, encoding="utf-8")
    else:
        print_to_console(analysis)


@app.command(name="open", no_args_is_help=True)
def open(
    file: str = typer.Argument(..., help="The file to open"),
    translator_path: str = typer.Option(
        "",
        "--translator",
        "-t",
        help="Optional path to an Excel file containing a translator sheet. If provided, it will be used to translate attribute names from the input dataframes. The sheet should contain at least two columns: one for the original attribute names and one for the translated names.",
    ),
    translator_attribute_name_col: int = typer.Option(
        0,
        "--translator-attribute-name-col",
        "-tanc",
        help="The column index (0-based) in the translator sheet that contains the original attribute names. Default is 0.",
    ),
    translator_translated_name_col: int = typer.Option(
        1,
        "--translator-translated-name-col",
        "-ttnc",
        help="The column index (0-based) in the attribute translator sheet that contains the translated attribute names. Default is 1.",
    ),
    translator_header_row: int = typer.Option(
        0,
        "--translator-header-row",
        "-athr",
        help="The row index (0-based) of the header in the attribute translator sheet. Default is 0 (the first row).",
    ),
    draft: bool = typer.Option(
        False,
        "--draft",
        "-d",
        help="Whether to create a draft version of the project. If set, the command will accept missing fields while still validating existing values",
    ),
):
    """
    Open a file and display its contents.
    Usage:
        openbdf open --file data.xlsx --bom-sheet Sheet1
    """

    project = open_openbdf_xlsx(
        xlsx_path=file,
        translator_path=translator_path,
        translator_attribute_name_col=translator_attribute_name_col,
        translator_translated_name_col=translator_translated_name_col,
        translator_header_row=translator_header_row,
        draft=draft,
    )

    if project is None:
        print("Failed to open the file. Please check the provided path and format.")
        return False

    save_openbdf_to_xlsx(
        xlsx_path=Path("./output.xlsx"),
        project=project,
    )


@app.command(name="save-template", no_args_is_help=True)
def save_template(
    path: str = typer.Argument(..., help="The path where the template Excel file will be saved"),
):
    """
    Save a template Excel file with the correct structure for OpenBDF.
    Usage:
        openbdf save-template ./template.xlsx
    """

    save_openbdf_to_xlsx(
        xlsx_path=Path(path),
        project=None,
    )


@app.command(name="save-translator-template", no_args_is_help=True)
def save_translator_template(
    path: str = typer.Argument(..., help="The path where the translator template Excel file will be saved"),
):
    """
    Save a template Excel file for the attribute translator.
    Usage:
        openbdf save-translator-template ./translator_template.xlsx
    """

    save_translator(
        xlsx_path=Path(path),
    )


if __name__ == "__main__":
    app()
