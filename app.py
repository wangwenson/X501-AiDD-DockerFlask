from flask import Flask, render_template, request, redirect, url_for, flash
import DAL
from pathlib import Path
import os

try:
    from PIL import Image
except Exception:
    Image = None

app = Flask(__name__)

# Ensure DB exists on startup
DAL.init_db()


@app.route('/')
def index():
    return render_template('index.html', active_page='home')


@app.route('/about')
def about():
    return render_template('about.html', active_page='about')


@app.route('/resume')
def resume():
    return render_template('resume.html', active_page='resume')


@app.route('/projects')
def projects():
    projects = DAL.get_projects()
    return render_template('projects.html', active_page='projects', projects=projects)


@app.route('/contact')
def contact():
    return render_template('contact.html', active_page='contact')


@app.route('/project-form')
def project_form():
    return render_template('project_form.html', active_page='projects')


@app.route('/projects/upload', methods=['POST'])
def upload_project():
    title = request.form.get('title', '').strip()
    description = request.form.get('description', '').strip()
    img = request.files.get('image')
    image_filename = ''
    images_dir = Path(__file__).parent / 'static' / 'images'
    images_dir.mkdir(parents=True, exist_ok=True)

    if img and img.filename:
        # Secure filename: keep alphanum, dash, underscore, dot
        orig = os.path.basename(img.filename)
        safe_name = ''.join(c for c in orig if c.isalnum() or c in (' ', '.', '-', '_')).rstrip()
        # ensure unique
        base, ext = os.path.splitext(safe_name)
        if not ext:
            ext = '.jpg'
        candidate = f"{base}{ext}"
        counter = 1
        while (images_dir / candidate).exists():
            candidate = f"{base}_{counter}{ext}"
            counter += 1
        target_path = images_dir / candidate

        # Save temporarily and resize if PIL is available
        img.save(str(target_path))
        image_filename = candidate
        if Image:
            try:
                with Image.open(str(target_path)) as im:
                    # Normalize size: fit within 600x400 while preserving aspect
                    max_w, max_h = 600, 400
                    im.thumbnail((max_w, max_h))
                    im.save(str(target_path))
            except Exception:
                # If image processing fails, leave the original file
                pass

    if title:
        DAL.add_project(title, description, image_filename)

    return redirect(url_for('projects'))


@app.route('/projects/add', methods=['POST'])
def add_project():
    # Expecting form fields: title, description, imageFileName
    title = request.form.get('title', '').strip()
    description = request.form.get('description', '').strip()
    image = request.form.get('imageFileName', '').strip()
    if title:
        DAL.add_project(title, description, image)
    return redirect(url_for('projects'))


@app.route('/thankyou')
def thankyou():
    first_name = request.args.get('firstName', '')
    last_name = request.args.get('lastName', '')
    return render_template('thankyou.html', first_name=first_name, last_name=last_name)


if __name__ == '__main__':
    # Bind to 0.0.0.0 so the app is reachable from Docker container port mapping
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port, debug=True)
