#!/usr/bin/env python3
"""
import_to_datasette.py

Create a SQLite DB suitable for Datasette from a JSON array file.
Usage:
  python3 import_to_datasette.py --input stories_with_entities5.json --output stardem_topic_entities.db

Behavior:
- Reads the input JSON (must be a top-level array of objects).
- Computes the union of keys across all objects and creates a `stories` table
  with an `id INTEGER PRIMARY KEY` and one column per key (TEXT), except
  `metadata_importance` which is stored INTEGER when present.
- For nested dict/list values, stores JSON-encoded strings.
- Creates an FTS5 virtual table `stories_fts` on `title` and `content` and
  populates it to enable full-text search from Datasette.
"""
import argparse
import json
import sqlite3
import re
from pathlib import Path


def sanitize_col(name: str) -> str:
    # Replace non-alphanum with underscore and coerce leading digits
    s = re.sub(r"[^0-9a-zA-Z_]", "_", name)
    if re.match(r"^[0-9]", s):
        s = "c_" + s
    return s.lower()


def gather_columns(records):
    cols = set()
    for r in records:
        if not isinstance(r, dict):
            continue
        cols.update(r.keys())
    # Ensure deterministic ordering: metadata fields first then alphabetical
    preferred = [
        "title",
        "date",
        "author",
        "content",
        "docref",
        "article_id",
        "date_parsed",
        "entities_people",
        "entities_quoted_people",
        "metadata_sport",
        "metadata_story_type",
        "metadata_location",
        "metadata_teams",
        "metadata_schools",
        "metadata_level_of_play",
        "metadata_competition_type",
        "metadata_outcome",
        "metadata_importance",
    ]
    ordered = []
    for p in preferred:
        if p in cols:
            ordered.append(p)
            cols.remove(p)
    remaining = sorted(cols)
    return ordered + remaining


def to_sql_value(v):
    # Convert python value to something storable in TEXT/INTEGER fields
    if v is None:
        return None
    if isinstance(v, (str, int, float)):
        return v
    # For lists/dicts/other types, store JSON string
    try:
        return json.dumps(v, ensure_ascii=False)
    except Exception:
        return str(v)


def create_and_populate(db_path: str, records, columns):
    db = sqlite3.connect(db_path)
    cur = db.cursor()

    # Create stories table
    col_defs = ["id INTEGER PRIMARY KEY"]
    sanitized = {}
    for c in columns:
        sc = sanitize_col(c)
        sanitized[c] = sc
        if c == "metadata_importance":
            col_defs.append(f"{sc} INTEGER")
        else:
            col_defs.append(f"{sc} TEXT")
    create_sql = f"CREATE TABLE IF NOT EXISTS stories ({', '.join(col_defs)});"
    cur.execute(create_sql)

    # Insert rows
    placeholders = ','.join(['?'] * len(columns))
    col_list_sql = ','.join(sanitized[c] for c in columns)
    insert_sql = f"INSERT INTO stories ({col_list_sql}) VALUES ({placeholders})"

    for r in records:
        vals = []
        for c in columns:
            v = r.get(c) if isinstance(r, dict) else None
            vals.append(to_sql_value(v))
        cur.execute(insert_sql, vals)
    db.commit()

    # Create FTS5 virtual table and populate for title + content
    # Make sure SQLite was compiled with FTS5. If not, this will raise.
    try:
        cur.execute("CREATE VIRTUAL TABLE IF NOT EXISTS stories_fts USING fts5(title, content, content='stories', content_rowid='id');")
        # Populate FTS from existing rows
        cur.execute("INSERT INTO stories_fts(rowid, title, content) SELECT id, title, content FROM stories WHERE title IS NOT NULL OR content IS NOT NULL;")
        db.commit()
    except sqlite3.OperationalError as e:
        print("Warning: could not create FTS5 table (sqlite may lack FTS5). Skipping FTS. Error:", e)

    # Create an index on date_parsed if present
    if 'date_parsed' in columns:
        try:
            cur.execute("CREATE INDEX IF NOT EXISTS idx_stories_date_parsed ON stories(date_parsed);")
            db.commit()
        except Exception:
            pass

    # Return rowcount
    cur.execute("SELECT count(*) FROM stories;")
    total = cur.fetchone()[0]
    db.close()
    return total


def main():
    p = argparse.ArgumentParser()
    p.add_argument('--input', '-i', required=True, help='Input JSON file (array of objects)')
    p.add_argument('--output', '-o', default='stardem_topic_entities.db', help='Output SQLite DB path')
    args = p.parse_args()

    infile = Path(args.input)
    if not infile.exists():
        raise SystemExit(f"Input file not found: {infile}")

    with infile.open('r', encoding='utf-8') as f:
        data = json.load(f)

    if not isinstance(data, list):
        raise SystemExit('Input JSON must be a top-level array of objects')

    cols = gather_columns(data)
    print(f"Detected {len(cols)} columns; creating DB {args.output} with {len(data)} rows...")
    total = create_and_populate(args.output, data, cols)
    print(f"Done. Inserted {total} rows into '{args.output}' (table: stories).")

if __name__ == '__main__':
    main()
