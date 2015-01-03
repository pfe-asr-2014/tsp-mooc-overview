from flask import render_template
from overview import app

@app.route('/')
def home():
    return render_template("index.html", title='Overview', state=services.states())
