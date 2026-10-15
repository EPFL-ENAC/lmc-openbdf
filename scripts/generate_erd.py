"""Print docs/src/developer/erd.md: a Mermaid ER diagram of the SQLModel tables.

Usage: make erd
"""

from sqlmodel import SQLModel

import openbdf.model.tables  # noqa: F401 registers every table on SQLModel.metadata

# Wide tables have hundreds of columns, the diagram is unreadable past this
MAX_COLUMNS = 20


def generate_mermaid() -> str:
    metadata = SQLModel.metadata
    lines = ["```mermaid", "erDiagram"]

    for table_name, table in sorted(metadata.tables.items()):
        lines.append(f"  {table_name} {{")
        # Keys first so relationships stay readable, then the model's declaration order
        columns = sorted(table.columns, key=lambda c: not (c.primary_key or c.foreign_keys))
        for column in columns[:MAX_COLUMNS]:
            # VARCHAR(255) -> VARCHAR, Mermaid rejects parentheses in types
            col_type = str(column.type).split("(")[0].replace(" ", "_")
            key = " PK" if column.primary_key else " FK" if column.foreign_keys else ""
            lines.append(f"    {col_type} {column.name}{key}")
        if len(columns) > MAX_COLUMNS:
            lines.append(f'    more columns "{len(columns) - MAX_COLUMNS} more"')
        lines.append("  }")

    relationships = {
        f'  {fk.column.table.name} ||--o{{ {table.name} : "{fk.parent.name}"'
        for table in metadata.tables.values()
        for fk in table.foreign_keys
    }
    lines.extend(sorted(relationships))
    lines.append("```")
    return "\n".join(lines)


def generate_markdown() -> str:
    return (
        "# Database ERD\n\n"
        "Every table on `SQLModel.metadata` (`openbdf/model/tables.py`), generated with `make erd`.\n"
        f"Shows the first {MAX_COLUMNS} columns of each table, keys first. Regenerate after changing the models.\n\n"
        + generate_mermaid()
    )


if __name__ == "__main__":
    print(generate_markdown())
