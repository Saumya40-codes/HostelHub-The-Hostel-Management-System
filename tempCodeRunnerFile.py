from hostel import create_app

app = create_app()

if __name__ == '__main__':
    app.config['TEMPLATES_AUTO_RELOAD'] = True
    app.config['UPLOAD_FOLDER'] = 'static/uploads'
    app.jinja_env.auto_reload = True
    app.run(debug=True)