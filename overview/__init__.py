from services import Services
from docker import Client
from flask import Flask

from frontend import register_frontend
from api import register_api
from helpers import register_helpers

def create_app(services_override=None):
    if services_override:
        services = services_override
    else:
        services = Services(Client(base_url='unix://var/run/docker.sock'), "config.yml")

    app = Flask(__name__, static_url_path='')
    register_frontend(app, services)
    register_api(app, services)
    register_helpers(app, services)

    return app
