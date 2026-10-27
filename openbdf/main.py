from pathlib import Path

import typer
from openpyxl import load_workbook

from openbdf.cli.save import (
    csv_dir_from_build,
    save_bec_translator,
    save_bmc_translator,
    save_openbdf_to_xlsx,
    save_translator,
    workbook_from_csv_dir,
)
from openbdf.lib.converters.dataframe import project_package_from_tables
from openbdf.lib.converters.translator_csv import workbook_sheets_to_csv_dir
from openbdf.lib.converters.translators import ABOUT_SHEET_NAME, DocumentTranslator
from openbdf.lib.openbdf_tables import OpenBDFTables
from openbdf.lib.sources.excel_source import DuplicateSheetNamesError, ExcelSheetSource
from openbdf.lib.validation import (
    DroppedLine,
    OpenBDFValidationError,
    Severity,
    format_findings,
    sort_findings,
    validate_project,
)

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
        help="Optional path(s) to Excel files or directories of sheet CSV files containing a translator sheet. Multiple files are merged (category conflicts resolve last-wins). If provided, they will be used to translate attribute names from the input dataframes. Each sheet should contain at least two columns: one for the original attribute names and one for the translated names.",
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
        True,
        "--drop-invalid-materials/--no-drop-invalid-materials",
        help="Drop bill of materials lines that miss required fields and report them as warnings. Enabled by default, use --no-drop-invalid-materials to keep these lines.",
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
            if Path(translator_path).is_dir():
                loaded_translator = DocumentTranslator.from_csv_dir(
                    directory=translator_path,
                    attribute_name_col=translator_attribute_name_col,
                    translated_name_col=translator_translated_name_col,
                    default_value_col=translator_default_value_col,
                    preprocess_rule_col=translator_preprocess_rule_col,
                    header_row=translator_header_row,
                )
            else:
                loaded_translator = DocumentTranslator.from_xlsx(
                    xlsx_path=translator_path,
                    attribute_name_col=translator_attribute_name_col,
                    translated_name_col=translator_translated_name_col,
                    default_value_col=translator_default_value_col,
                    preprocess_rule_col=translator_preprocess_rule_col,
                    header_row=translator_header_row,
                )
            document_translator = document_translator + loaded_translator
    else:
        document_translator = DocumentTranslator.default_openbdf_translator()

    try:
        with ExcelSheetSource(files) as source:
            tables = OpenBDFTables.from_source(source, document_translator)
    except DuplicateSheetNamesError as exc:
        typer.echo(f"Error: {exc}", err=True)
        raise typer.Exit(code=1) from exc

    if tables is None:
        typer.echo("Error: the files contain no project sheet or bill of materials sheet.", err=True)
        raise typer.Exit(code=1)

    findings: list[OpenBDFValidationError] = []
    project = project_package_from_tables(
        tables,
        document_translator,
        findings=findings,
        draft=draft,
        drop_invalid=drop_invalid_materials,
    )
    findings.extend(
        validate_project(
            project,
            tables,
            document_translator=document_translator,
            dropped_rows=frozenset(
                finding.row for finding in findings if isinstance(finding, DroppedLine) and finding.row is not None
            ),
        )
    )
    findings = sort_findings(findings)

    for line in format_findings(findings):
        typer.echo(line, err=True)

    if not draft and any(finding.severity is Severity.REJECT for finding in findings):
        typer.echo("The workbook has reject findings, so it was not saved. Use --draft to save it anyway.", err=True)
        raise typer.Exit(code=1)

    save_openbdf_to_xlsx(
        xlsx_path=output_path,
        project=project,
    )


@app.command(name="save-template", no_args_is_help=True)
def save_template(
    path: str = typer.Argument(
        ..., help="The path where the template Excel file, or the CSV directory with --csv, will be saved"
    ),
    csv: bool = typer.Option(
        False,
        "--csv",
        help="Write one CSV file per sheet into the given directory instead of an Excel file.",
    ),
):
    """
    Save a template Excel file with the correct structure for OpenBDF.
    Usage:
        openbdf save-template ./template.xlsx
        openbdf save-template ./template --csv
    """

    if csv:
        csv_dir_from_build(lambda buffer: save_openbdf_to_xlsx(xlsx_path=buffer, project=None), Path(path))
    else:
        save_openbdf_to_xlsx(
            xlsx_path=Path(path),
            project=None,
        )


@app.command(name="save-translator-template", no_args_is_help=True)
def save_translator_template(
    path: str = typer.Argument(
        ..., help="The path where the translator template Excel file, or the CSV directory with --csv, will be saved"
    ),
    csv: bool = typer.Option(
        False,
        "--csv",
        help="Write one CSV file per sheet into the given directory instead of an Excel file.",
    ),
):
    """
    Save a template Excel file for the attribute translator.
    Usage:
        openbdf save-translator-template translators/translator_template.xlsx
        openbdf save-translator-template translators/translator_template --csv
    """

    if csv:
        csv_dir_from_build(save_translator, Path(path))
    else:
        save_translator(
            xlsx_path=Path(path),
        )


@app.command(name="save-bec-template", no_args_is_help=True)
def save_bec_template(
    path: str = typer.Argument(
        ...,
        help="The path where the bec translator template Excel file, or the CSV directory with --csv, will be saved",
    ),
    csv: bool = typer.Option(
        False,
        "--csv",
        help="Write one CSV file per sheet into the given directory instead of an Excel file.",
    ),
):
    """
    Save a template Excel file for the building element classification translator.
    Usage:
        openbdf save-bec-template build/translators/translator_bec_template.xlsx
        openbdf save-bec-template build/translators/translator_bec_template --csv
    """

    if csv:
        csv_dir_from_build(save_bec_translator, Path(path))
    else:
        save_bec_translator(
            xlsx_path=Path(path),
        )


@app.command(name="save-bmc-template", no_args_is_help=True)
def save_bmc_template(
    path: str = typer.Argument(
        ...,
        help="The path where the bmc translator template Excel file, or the CSV directory with --csv, will be saved",
    ),
    csv: bool = typer.Option(
        False,
        "--csv",
        help="Write one CSV file per sheet into the given directory instead of an Excel file.",
    ),
):
    """
    Save a template Excel file for the material classification translator.
    Usage:
        openbdf save-bmc-template build/translators/translator_bmc_template.xlsx
        openbdf save-bmc-template build/translators/translator_bmc_template --csv
    """

    if csv:
        csv_dir_from_build(save_bmc_translator, Path(path))
    else:
        save_bmc_translator(
            xlsx_path=Path(path),
        )


@app.command(name="csv-to-translator", no_args_is_help=True)
def csv_to_translator(
    directory: Path = typer.Argument(..., help="The directory holding one CSV file per sheet"),
    path: Path = typer.Argument(..., help="The path where the translator Excel file will be saved"),
):
    """
    Build a translator Excel file from a directory of sheet CSV files.
    Usage:
        openbdf csv-to-translator translators/translator_at build/translators/translator_at.xlsx
    """

    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_bytes(workbook_from_csv_dir(directory).getvalue())


@app.command(name="translator-to-csv", no_args_is_help=True)
def translator_to_csv(
    path: Path = typer.Argument(..., help="The translator Excel file to convert"),
    directory: Path = typer.Argument(..., help="The directory where the CSV files are written"),
):
    """
    Write one CSV file per sheet of an existing translator Excel file.
    Usage:
        openbdf translator-to-csv translators/translator_at_v2.0.0.xlsx translators/translator_at
    """

    workbook_sheets_to_csv_dir(load_workbook(path), directory, exclude=(ABOUT_SHEET_NAME,))


if __name__ == "__main__":
    app()
