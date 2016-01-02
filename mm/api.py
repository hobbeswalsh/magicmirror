import json
import time

from flask import Blueprint
from flask import jsonify
from flask import request

from . import gcal
from . import greet
from . import weather

api = Blueprint('api', __name__)


@api.route('/ping')
def pong():
    return jsonify({
        "response": "PONG",
        "timestamp": time.time(),
    })


@api.route('/weather')
def get_forecast():
    return jsonify(weather.get_forecast())


@api.route('/calendar')
def get_calendar():
    days = int(request.args.get('days', 1))
    return jsonify(gcal.get_events(future_days=days))


@api.route('/greet')
def get_greeting():
    return jsonify(greet.get_greeting())

