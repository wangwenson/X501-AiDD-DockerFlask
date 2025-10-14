from flask import Flask, render_template, request

app = Flask(__name__)

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
    return render_template('projects.html', active_page='projects')

@app.route('/contact')
def contact():
    return render_template('contact.html', active_page='contact')

@app.route('/thankyou')
def thankyou():
    first_name = request.args.get('firstName', '')
    last_name = request.args.get('lastName', '')
    return render_template('thankyou.html', first_name=first_name, last_name=last_name)

if __name__ == '__main__':
    app.run(debug=True)
