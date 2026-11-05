"""Copy the ACSDB Access database to SQLite, changing nothing but the file format.

Usage: uv run scripts/build_sqlite.py [--input ADDB.mdb] [--output acsdb.sqlite]
"""

from __future__ import annotations

import argparse
import sqlite3
import tempfile
from pathlib import Path

from access_parser import AccessParser

ROOT = Path(__file__).resolve().parent.parent
DEFAULT_INPUT = ROOT / "data" / "raw" / "acsdb" / "ADDB.mdb"
DEFAULT_OUTPUT = ROOT / "data" / "processed" / "acsdb.sqlite"

# Access column type codes that aren't text. Everything else, including dates, is stored as TEXT.
SQLITE_TYPES = {
    1: "INTEGER",
    2: "INTEGER",
    3: "INTEGER",
    4: "INTEGER",
    5: "REAL",
    6: "REAL",
    7: "REAL",
}


def quoted(identifier: str) -> str:
    """Quote a SQL identifier."""
    return '"' + identifier.replace('"', '""') + '"'


def copy_table(connection: sqlite3.Connection, database: AccessParser, name: str) -> None:
    """Copy one Access table, keeping its source column order and row order."""
    table = database.get_table(name)
    columns = sorted(table.columns.values(), key=lambda column: column.column_index)
    names = [str(column.col_name_str) for column in columns]
    data = table.parse()

    definitions = ", ".join(
        f"{quoted(str(column.col_name_str))} {SQLITE_TYPES.get(column.type, 'TEXT')}"
        for column in columns
    )
    connection.execute(f"CREATE TABLE {quoted(name)} ({definitions})")
    placeholders = ", ".join("?" * len(names))
    connection.executemany(
        f"INSERT INTO {quoted(name)} VALUES ({placeholders})",  # noqa: S608
        zip(*(data[column] for column in names), strict=True),
    )


def build(source: Path, output: Path) -> None:
    """Build the database at `output`, replacing it only once the build has succeeded."""
    database = AccessParser(str(source))
    names = sorted(name for name in database.catalog if not name.startswith("MSys"))
    output.parent.mkdir(parents=True, exist_ok=True)
    with tempfile.TemporaryDirectory(dir=output.parent) as directory:
        scratch = Path(directory) / output.name
        connection = sqlite3.connect(scratch)
        try:
            for name in names:
                copy_table(connection, database, name)
            connection.commit()
            for name in names:
                count = connection.execute(f"SELECT count(*) FROM {quoted(name)}").fetchone()[0]  # noqa: S608
                print(f"{name}: {count} rows")
        finally:
            connection.close()
        scratch.replace(output)
    print(f"Wrote {output}")


def main() -> None:
    """Run the command line."""
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument("--input", type=Path, default=DEFAULT_INPUT, help="Access database")
    parser.add_argument("--output", type=Path, default=DEFAULT_OUTPUT, help="SQLite file to write")
    arguments = parser.parse_args()
    build(arguments.input, arguments.output)


if __name__ == "__main__":
    main()
