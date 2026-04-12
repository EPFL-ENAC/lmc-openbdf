from pathlib import Path

import typer

from openbdf.cli.open import open_openbdf_xlsx
from openbdf.cli.save import save_openbdf_to_xlsx

app = typer.Typer(help="CLI utilities for the project.")


@app.command()
def hello(name: str):
    print(f"Hello {name}")


@app.command(name="explain")
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


@app.command(name="open")
def open(
    file: str = typer.Option(..., "--file", "-f", help="The file to open"),
    info_sheet: str = typer.Option(
        "General Info",
        "--info-sheet",
        "-i",
        help="The sheet containing the general info data. Required if opening an Excel file with multiple sheets.",
    ),
    info_header_col: int = typer.Option(
        0,
        "--info-header-col",
        "-ih",
        help="The column index (0-based) of the header in the general info sheet. Default is 0 (the first column).",
    ),
    info_values_col: int = typer.Option(
        1,
        "--info-values-col",
        "-iv",
        help="The column index (0-based) of the values in the general info sheet. Default is 1 (the second column).",
    ),
    info_start_row: int = typer.Option(
        1,
        "--info-start-row",
        "-is",
        help="The starting row index (0-based) for the bill of materials data in the Excel sheet after the header. Default is 1 (the first row after the header).",
    ),
    bom_sheet: str = typer.Option(
        "Building Bill of Materials",
        "--bom-sheet",
        "-b",
        help="The sheet containing the bill of materials data. Required if opening an Excel file with multiple sheets.",
    ),
    bom_header_row: int = typer.Option(
        0,
        "--bom-header-row",
        "-hr",
        help="The row index (0-based) of the header in the bill of materials sheet. Default is 0 (the first row).",
    ),
    bom_start_row: int = typer.Option(
        0,
        "--bom-start-row",
        "-s",
        help="The starting row index (0-based) for the bill of materials data in the Excel sheet after the header. Default is 0 (the first row after the header).",
    ),
    bom_start_col: int = typer.Option(
        0,
        "--bom-start-col",
        "-c",
        help="The starting column index (0-based) for the bill of materials data in the Excel sheet. Default is 0 (the first column).",
    ),
    bom_end_row: int | None = typer.Option(
        None,
        "--bom-end-row",
        "-er",
        help="The ending row index (0-based) for the bill of materials data in the Excel sheet. If not provided, it will read until the last row with data.",
    ),
    bom_end_col: int | None = typer.Option(
        None,
        "--bom-end-col",
        "-ec",
        help="The ending column index (0-based) for the bill of materials data in the Excel sheet. If not provided, it will read until the last column with data.",
    ),
):
    """
    Open a file and display its contents.
    Usage:
        openbdf open --file data.xlsx --bom-sheet Sheet1
    """

    project = open_openbdf_xlsx(
        xlsx_path=file,
        info_sheet_name=info_sheet,
        info_header_col=info_header_col,
        info_values_col=info_values_col,
        info_start_row=info_start_row,
        bom_sheet_name=bom_sheet,
        bom_header_row=bom_header_row,
        bom_start_row=bom_start_row,
        bom_start_col=bom_start_col,
        bom_end_row=bom_end_row,
        bom_end_col=bom_end_col,
    )

    save_openbdf_to_xlsx(
        xlsx_path=Path("../output.xlsx"),
        project=project,
    )


if __name__ == "__main__":
    app()
