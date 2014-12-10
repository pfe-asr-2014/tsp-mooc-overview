#!flask/bin/python
from flask import Flask, jsonify, render_template, request
from docker import Client
from services import Services

services = Services(Client(base_url='unix://var/run/docker.sock'), "config.yml")
app = Flask(__name__, static_url_path='')

@app.route('/')
def home():
    return render_template("index.html", title='Overview', state=services.states())

@app.route('/api/v1/docker', methods=['GET'])
def show_docker():
    return jsonify(services.docker_state())

@app.route('/api/v1/services', methods=['GET'])
def list_services():
    return jsonify(services.states())

@app.route('/api/v1/services/<id>', methods=['PATCH'])
def patch_service(id):
    err = services.change(id, request.json['state'])

    if err:
        return jsonify({'message':'This change cannot be made', 'error': err}), 400
    else:
        return jsonify({'message':'Correctly applied. Change in progress.'})

@app.template_filter('toclass')
def service_state_toclass_filter(s):
    if s == 'Stopped':
        return 'color-red'
    elif s == 'Running':
        return 'color-green'
    elif s == 'Not Installed':
        return 'color-gray'
    else:
        return ''

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')
