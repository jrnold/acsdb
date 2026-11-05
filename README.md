# ACSDB: the Ardennes Campaign Simulation Data Base

Source files for the Ardennes Campaign Simulation Data Base (ACSDB), a daily unit-level database of the
1944 Ardennes Campaign (Battle of the Bulge). It was delivered to the US Army Concepts Analysis Agency
in 1989 under contract MDA903-87-C-0787.

## Files

`data/raw/acsdb/` holds the files as received, unmodified. Start with `CONTENTS.TXT`.

  | File                                         | Contents                                                  |
  | -------------------------------------------- | --------------------------------------------------------- |
  | `ADDB.mdb`                                   | The database, in Microsoft Access format                  |
  | `USRGUIDE.PDF`, `DBFIELDS.PDF`               | The user's guide excerpt and database field documentation |
  | `SECI-II.PDF`, `SECIII-V.PDF`, `SECVI-X.PDF` | Final report excerpts                                     |
  | `APPIIA-F.PDF`, `APPIIG.PDF`, `APPIIH-I.PDF` | Final report appendix excerpts                            |
  | `MAPCOORD.PDF`, `GEOSUMRY.PDF`               | The map grid and coordinate conversion                    |

## SQLite database

`scripts/build_sqlite.py` copies the Access database to `data/processed/acsdb.sqlite`, changing only
the file format:

```sh
uv run scripts/build_sqlite.py
```

Tables, columns, row order and values are as in the source, including its errors and its codes for
missing values. SQLite has no date type, so dates are stored as `YYYY-MM-DD HH:MM:SS` text.

## Provenance

Purchased on CD-ROM from the National Technical Information Service (NTIS) in September 2015, order
number ADM001245 (DTIC accession ADM001245). The Center for Army Analysis prepared the CD in March 2000.

`CONTENTS.TXT` describes eight dBASE IV files, which are not in this copy, and doesn't list
`DBFIELDS.PDF`. The files here are what was saved from the CD in 2015. Compare them with the disc to
confirm the copy is complete.

## Rights

Not yet determined. This repo adds no licence.
