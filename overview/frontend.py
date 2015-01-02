from flask import render_template

def register_frontend(app, services):

    @app.route('/')
    def home():
        return render_template("index.html", title='Overview', state=services.states())
