from flask import Flask, jsonify, render_template, request

def register_api(app, services):

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
