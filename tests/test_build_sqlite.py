"""Tests that scripts/build_sqlite.py copies the source database without changing it."""

import sqlite3

import pytest
from build_sqlite import DEFAULT_INPUT, build

ROW_COUNTS = {
    "AIR": 1705,
    "BIBLIOG": 337,
    "INVENTOR": 15055,
    "REFERENC": 628,
    "TOE": 153,
    "UNITDATA": 6260,
    "UNITLOC": 3402,
    "WPNS": 209,
}


@pytest.fixture(scope="module")
def connection(tmp_path_factory):
    output = tmp_path_factory.mktemp("build") / "acsdb.sqlite"
    build(DEFAULT_INPUT, output)
    with sqlite3.connect(output) as database:
        yield database
    database.close()


def test_holds_only_the_source_tables(connection):
    objects = connection.execute("SELECT type, name FROM sqlite_master").fetchall()
    assert sorted(objects) == [("table", name) for name in sorted(ROW_COUNTS)]


@pytest.mark.parametrize(("table", "count"), ROW_COUNTS.items())
def test_row_counts(connection, table, count):
    assert connection.execute(f'SELECT count(*) FROM "{table}"').fetchone()[0] == count  # noqa: S608


def test_columns_keep_source_names_and_order(connection):
    columns = [row[1] for row in connection.execute('PRAGMA table_info("UNITLOC")')]
    assert columns[:3] == ["UNIT_NAME", "DATE", "NATION"]
    assert len(columns) == 38


@pytest.mark.parametrize(
    "value",
    [
        "k5400 (WERBOMONT)",  # a typo the source documents note
        "P408369 (LAVACHERIE)",  # an error the source documents correct
        "        (ENNERY)",  # leading spaces
    ],
)
def test_source_errors_and_spacing_are_kept(connection, value):
    rows = connection.execute('SELECT count(*) FROM "UNITLOC" WHERE START_LOC = ?', (value,))
    assert rows.fetchone()[0] > 0


def test_missing_value_codes_and_timestamps_are_kept(connection):
    date, in_combat = connection.execute(
        'SELECT DATE, TIM_IN_CBT FROM "UNITLOC" ORDER BY rowid LIMIT 1'
    ).fetchone()
    assert date == "1944-12-19 00:00:00"
    assert in_combat == pytest.approx(999.9)
