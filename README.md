# ACSDB: the Ardennes Campaign Simulation Data Base

[![DOI](https://zenodo.org/badge/DOI/10.5281/zenodo.23968496.svg)](https://doi.org/10.5281/zenodo.23968496)
[![Lint](https://github.com/jrnold/acsdb/actions/workflows/lint.yml/badge.svg?branch=main)](https://github.com/jrnold/acsdb/actions/workflows/lint.yml)
[![License: CC0-1.0](https://img.shields.io/badge/License-CC0_1.0-lightgrey.svg)](https://creativecommons.org/publicdomain/zero/1.0/)

Source files for the Ardennes Campaign Simulation Data Base (ACSDB), a daily unit-level database of the
1944 Ardennes Campaign (Battle of the Bulge). It was delivered to the US Army Concepts Analysis Agency
in 1989 under contract MDA903-87-C-0787.

## Files

`data/raw/acsdb/` holds the source files. Start with `CONTENTS.TXT`. `ADDB.mdb` and `CONTENTS.TXT` are
from the NTIS CD-ROM. The PDFs are the deskewed scans embedded in `docs/DTIC_AD1034106.pdf`, with their
text layer replaced using `ocrmypdf --redo-ocr --output-type pdf --optimize 0 -l eng`. The page images
are unchanged, but OCR text can be wrong, so check figures against the page image.

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
`DBFIELDS.PDF`. `ADDB.mdb` and `CONTENTS.TXT` are what was saved from the CD in 2015. Compare them with the disc to
confirm the copy is complete.

## Data release

The database, its SQLite copy and the documentation are archived on Zenodo:
[10.5281/zenodo.23968496](https://doi.org/10.5281/zenodo.23968496).

## Rights

The Dupuy Institute lists the [ACSDB](https://dupuyinstitute.org/products/other-databases/acsdb/) as owned
by the US Army Concepts Analysis Agency and in the public domain. Derived data, namely the SQLite copy
and the OCR text layers, is released under [CC0 1.0](https://creativecommons.org/publicdomain/zero/1.0/).
