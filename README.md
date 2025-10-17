
# Assignment 7 — Personal Portfolio (Flask)

This repository contains a Flask-based personal portfolio site with a small SQLite database for managing projects.


## File structure (important files)
- `app.py` — Flask application and route handlers
- `DAL.py` — Data Access Layer: initializes the DB and provides `get_projects()` and `add_project()` helpers
- `projects.db` — SQLite database (created at runtime in the project root)
- `pyproject.toml` — project metadata and dependencies (Flask, Pillow)
- `templates/` — Jinja2 templates
	- `index.html`, `about.html`, `projects.html`, `project_form.html`, `contact.html`, etc.
- `static/`
	- `css/styles.css` — custom styles
	- `images/` — project images (uploaded images are saved here)

## Dependencies
- Python 3.10+ (your environment)
- Flask
- Pillow (for image resizing)

Install locally (recommended inside a virtual environment):


or install from `pyproject.toml` with your preferred tooling.

## How to run
From the project root (activate your venv first if you created one):
python app.py

Open a browser and visit:
- http://127.0.0.1:5000/ — Home

When the app starts, `DAL.init_db()` runs and will create `projects.db` with a `projects` table if needed.

## Adding projects and images
- Use the "Add Project" button (or visit `/project-form`) to submit a new project and optionally upload an image.
- Uploaded images are saved into `static/images/`. The server will resize images to a consistent max size for display.
- You can also add images manually by placing files in `static/images/` and submitting the project via the older form (if present) with the filename.

## Notes and next steps
- For production use, add CSRF protection, stricter upload validation, and authentication for project creation.
- The image resizing currently fits images within a 600x400 box preserving aspect ratio; if you prefer fixed square thumbnails or center-crop behavior, I can change the resizing logic.

## Contact
This repo was created as part of Assignment 5 for the X501 AiDD course.

