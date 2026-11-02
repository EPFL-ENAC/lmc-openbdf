import pytest
from typer.testing import CliRunner

from openbdf.main import app

runner = CliRunner()


@pytest.mark.parametrize(
    "subcommand",
    [
        "",
        "codes",
        "explain",
        "open",
        "save-bec-template",
        "save-bmc-template",
        "csv-to-translator",
        "translator-to-csv",
    ],
)
def test_help(subcommand: str):
    """Test help messages for CLI commands."""
    result = runner.invoke(app, [*subcommand.split(), "--help"])
    assert result.exit_code == 0


def test_codes_lists_the_reject_findings_before_the_warnings():
    result = runner.invoke(app, ["codes"])

    assert result.exit_code == 0
    assert "| E001  MissingRequiredField " in result.output
    assert "| W001  AutomaticFieldSupplied " in result.output
    assert result.output.index("E001") < result.output.index("W001")
