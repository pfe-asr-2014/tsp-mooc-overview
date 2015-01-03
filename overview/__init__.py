from services import Services
from docker import Client
from flask import Flask

services = Services(Client(base_url='unix://var/run/docker.sock'), "config.yml")
app = Flask(__name__, static_url_path='')

import overview.frontend
import overview.api
import overview.helpers
