"""Set the template version in about.md, the release workflow and the README.

Usage: python scripts/set_template_version.py vX.Y.Z
"""

import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent

ABOUT_PATTERN = r"(?m)^(\*\*Version )\d+\.\d+\.\d+(?=\*\*)"
RELEASE_PATTERN = r"(?m)^(\s*TEMPLATE_VERSION: )v\d+\.\d+\.\d+$"
# Longest asset names first, so no alternative can shadow a longer one.
README_PATTERN = (
    r"(?m)(releases/latest/download/"
    r"(?:translator_bec_template|translator_bmc_template|translator_template"
    r"|translator_bec_at|translator_bmc_at|openbdf_template|translator_at)_)v\d+\.\d+\.\d+(?=\.xlsx)"
)


def replace_version(path: Path, pattern: str, version: str) -> int:
    """Replace the version token in path and return the number of replacements."""
    content = path.read_text(encoding="utf-8")
    updated, count = re.subn(pattern, rf"\g<1>{version}", content)
    if updated != content:
        path.write_text(updated, encoding="utf-8")
    return count


def main(argv: list[str]) -> int:
    if len(argv) != 2 or not re.fullmatch(r"v\d+\.\d+\.\d+", argv[1]):
        print("usage: make set-version vX.Y.Z", file=sys.stderr)
        return 2

    version = argv[1]
    targets = (
        ("openbdf/about.md", ABOUT_PATTERN, version.removeprefix("v")),
        (".github/workflows/release.yaml", RELEASE_PATTERN, version),
        ("README.md", README_PATTERN, version),
    )
    for relative_path, pattern, replacement in targets:
        count = replace_version(ROOT / relative_path, pattern, replacement)
        if count == 0:
            print(f"{relative_path}: no version token found", file=sys.stderr)
            return 1
        print(f"{relative_path}: {count} replaced")
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv))
