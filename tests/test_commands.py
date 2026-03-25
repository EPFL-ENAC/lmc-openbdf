import pytest
from typer.testing import CliRunner

from openbdf.main import app

runner = CliRunner()


@pytest.mark.parametrize(
    "subcommand",
    [
        "",
        "explain",
    ],
)
def test_help(subcommand: str):
    """Test help messages for CLI commands."""
    result = runner.invoke(app, [*subcommand.split(), "--help"])
    assert result.exit_code == 0
