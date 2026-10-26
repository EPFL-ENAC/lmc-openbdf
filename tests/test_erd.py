import subprocess
import sys
from pathlib import Path

_ROOT = Path(__file__).resolve().parent.parent


def test_erd_doc_is_in_sync_with_the_models():
    # Subprocess: SQLModel.metadata is global, tables defined by other tests would leak in
    result = subprocess.run(
        [sys.executable, "scripts/generate_erd.py"], cwd=_ROOT, capture_output=True, text=True, check=True
    )
    committed = (_ROOT / "docs/src/developer/erd.md").read_text(encoding="utf-8")
    assert result.stdout == committed, "docs/src/developer/erd.md is out of sync with the models. Run: make erd"
    # GitHub's Mermaid stops rendering past 50k characters
    assert len(committed) < 50_000
