import io
import os
import tempfile
import pytest
from pathlib import Path

import DAL
import app as myapp

from PIL import Image


@pytest.fixture
def client(tmp_path, monkeypatch):
    # Create a temporary DB and images dir
    db_file = tmp_path / "test_projects.db"
    images_dir = tmp_path / "images"
    images_dir.mkdir()

    # Monkeypatch DAL functions to use the tmp DB path
    monkeypatch.setattr(DAL, 'DB_PATH', db_file)

    # Ensure app uses the DAL init_db for the tmp DB
    DAL.init_db(path=db_file)

    # Monkeypatch the images directory used by the app to the temp dir
    monkeypatch.setenv('FLASK_TEST_IMAGES', str(images_dir))

    # Create test client
    myapp.app.config['TESTING'] = True
    client = myapp.app.test_client()
    yield client


def create_test_image(filename="test.png", size=(100, 100), color=(255, 0, 0)):
    # Create an in-memory image and return bytes
    img = Image.new('RGB', size, color)
    bio = io.BytesIO()
    img.save(bio, 'PNG')
    bio.seek(0)
    return bio


def test_projects_page_empty(client):
    resp = client.get('/projects')
    assert resp.status_code == 200
    assert b'No projects found' in resp.data or b'Add Project' in resp.data


def test_upload_project(client, tmp_path):
    # Upload an image and project via the project-form route
    img_bytes = create_test_image()
    data = {
        'title': 'Uploaded Project',
        'description': 'A description',
        'image': (img_bytes, 'upload.png')
    }
    resp = client.post('/projects/upload', data=data, content_type='multipart/form-data', follow_redirects=True)
    assert resp.status_code == 200
    # After redirect, projects page should contain the uploaded title
    assert b'Uploaded Project' in resp.data
