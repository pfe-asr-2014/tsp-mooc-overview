import os
from flask import render_template
from overview import app, services

@app.route('/')
def home():
    base = os.environ["HOST_IP"] if "HOST_IP" in os.environ else "localhost"
    return render_template("index.html", title='Overview', state=services.states(), base = base)
