from pathlib import Path

import typer

from openbdf.cli.save import save_openbdf_to_xlsx, save_translator
from openbdf.lib.converters.dataframe import project_package_from_tables
from openbdf.lib.converters.translators import DocumentTranslator
from openbdf.lib.openbdf_tables import OpenBDFTables
from openbdf.lib.sources.excel_source import DuplicateSheetNamesError, ExcelSheetSource
from openbdf.lib.validation import OpenBDFValidationErrors, check_declared_results, format_findings

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
    files: list[Path] = typer.Argument(..., help="One or more Excel files to open as a single document"),
    translator_paths: list[str] = typer.Option(
        [],
        "--translator",
        "-t",
        help="Optional path(s) to Excel files containing a translator sheet. Multiple files are merged (category conflicts resolve last-wins). If provided, they will be used to translate attribute names from the input dataframes. Each sheet should contain at least two columns: one for the original attribute names and one for the translated names.",
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
    translator_default_value_col: int | None = typer.Option(
        5,
        "--translator-default-value-col",
        "-tdvc",
        help="The column index (0-based) in the attribute translator sheet that contains the default value for a field. Default is 5. Ignored if the column does not exist.",
    ),
    translator_preprocess_rule_col: int | None = typer.Option(
        6,
        "--translator-preprocess-rule-col",
        "-tprc",
        help="The column index (0-based) in the attribute translator sheet that contains the preprocess rule for a field. Default is 6. Ignored if the column does not exist.",
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
    drop_invalid_materials: bool = typer.Option(
        False,
        "--drop-invalid-materials",
        help="Drop bill of materials lines that miss required fields and print which were dropped.",
    ),
    output_path: Path = typer.Option(
        Path("./output.xlsx"),
        "--output-path",
        "-o",
        help="File path where the opened document is saved. Defaults to ./output.xlsx.",
    ),
):
    """
    Open one or more Excel files as a single document and display its contents.
    Usage:
        openbdf open project.xlsx
        openbdf open project.xlsx materials.xlsx results.xlsx
    """
    if translator_paths:
        document_translator = DocumentTranslator()
        for translator_path in translator_paths:
            document_translator = document_translator + DocumentTranslator.from_xlsx(
                xlsx_path=translator_path,
                attribute_name_col=translator_attribute_name_col,
                translated_name_col=translator_translated_name_col,
                default_value_col=translator_default_value_col,
                preprocess_rule_col=translator_preprocess_rule_col,
                header_row=translator_header_row,
            )
    else:
        document_translator = DocumentTranslator.default_openbdf_translator()

    try:
        with ExcelSheetSource(files) as source:
            tables = OpenBDFTables.from_source(source, document_translator)
    except DuplicateSheetNamesError as exc:
        typer.echo(f"Error: {exc}", err=True)
        raise typer.Exit(code=1) from exc

    if tables is None or (not draft and tables.project_material_database is None):
        print("Failed to open the files. Please check the provided paths and formats.")
        return False

    project = project_package_from_tables(
        tables,
        document_translator,
        draft=draft,
        drop_invalid=drop_invalid_materials,
    )

    try:
        findings = check_declared_results(project, draft=draft)
    except OpenBDFValidationErrors as exc:
        for line in format_findings(exc.findings):
            typer.echo(line, err=True)
        raise typer.Exit(code=1) from exc

    for line in format_findings(findings):
        typer.echo(line, err=True)

    save_openbdf_to_xlsx(
        xlsx_path=output_path,
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
        openbdf save-translator-template translators/translator_template.xlsx
    """

    save_translator(
        xlsx_path=Path(path),
    )


if __name__ == "__main__":
    app()
