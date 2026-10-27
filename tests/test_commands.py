import pytest
from typer.testing import CliRunner

from openbdf.main import app

runner = CliRunner()


@pytest.mark.parametrize(
    "subcommand",
    [
        "",
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
