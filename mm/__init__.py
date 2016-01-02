from flask import Flask

from .api import api
from .web import web

app = Flask(__name__)

app.register_blueprint(api, url_prefix='/api/v1')
app.register_blueprint(web, url_prefix='/')

