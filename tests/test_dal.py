import sqlite3
from pathlib import Path
import DAL


def test_init_and_add_get(tmp_path):
    # Use a temporary DB file
    db_file = tmp_path / "test_projects.db"
    # Initialize DB
    DAL.init_db(path=db_file)
    assert db_file.exists()

    # Add a project
    rowid = DAL.add_project("Test Title", "Test description", "img.jpg", path=db_file)
    assert isinstance(rowid, int) and rowid > 0

    # Get projects
    projects = DAL.get_projects(path=db_file)
    assert isinstance(projects, list)
    assert len(projects) == 1
    p = projects[0]
    assert p["Title"] == "Test Title"
    assert p["Description"] == "Test description"
    assert p["ImageFileName"] == "img.jpg"
