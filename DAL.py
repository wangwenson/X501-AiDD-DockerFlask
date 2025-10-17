import sqlite3
from pathlib import Path
from typing import List, Dict, Optional

DB_PATH = Path(__file__).parent / "projects.db"

CREATE_TABLE_SQL = """CREATE TABLE IF NOT EXISTS projects (
	id INTEGER PRIMARY KEY AUTOINCREMENT,
	Title TEXT NOT NULL,
	Description TEXT,
	ImageFileName TEXT
);"""


def init_db(path: Path = DB_PATH) -> Path:
	"""Create the SQLite database file and the `projects` table if they don't exist.

	Returns the path to the database file.
	"""
	conn = sqlite3.connect(str(path))
	try:
		cur = conn.cursor()
		cur.execute(CREATE_TABLE_SQL)
		conn.commit()
	finally:
		conn.close()
	return path


def get_connection(path: Path = DB_PATH) -> sqlite3.Connection:
	return sqlite3.connect(str(path))


def add_project(title: str, description: str, image_file: str, path: Path = DB_PATH) -> int:
	"""Insert a new project and return the new row id."""
	conn = get_connection(path)
	try:
		cur = conn.cursor()
		cur.execute(
			"INSERT INTO projects (Title, Description, ImageFileName) VALUES (?,?,?)",
			(title, description, image_file),
		)
		conn.commit()
		return cur.lastrowid
	finally:
		conn.close()


def get_projects(path: Path = DB_PATH) -> List[Dict[str, Optional[str]]]:
	"""Return all projects as a list of dicts."""
	conn = get_connection(path)
	try:
		conn.row_factory = sqlite3.Row
		cur = conn.cursor()
		cur.execute("SELECT id, Title, Description, ImageFileName FROM projects ORDER BY id DESC")
		rows = cur.fetchall()
		return [dict(r) for r in rows]
	finally:
		conn.close()


if __name__ == "__main__":
	p = init_db()
	print(f"Created/checked DB at: {p}")
