import json

from concurrent import futures
from flask import Blueprint
from flask import render_template

from .api import get_greeting
from .api import get_calendar
from .api import get_forecast

web = Blueprint('web', __name__)


@web.route('/')
def index():
    real_results = {"greeting": json.loads(get_greeting().data)}
    with futures.ProcessPoolExecutor(max_workers=5) as executor:
        results = {
            executor.submit(get_calendar): "schedule",
            executor.submit(get_forecast): "weather",
        }
        for future in futures.as_completed(results):
            topic = results[future]
            try:
                result = future.result()
            except Exception as e:
                raise
            else:
                real_results[topic] = json.loads(result.data)

    schedule = real_results.get("schedule")
    weather = real_results.get("weather")
    greeting = real_results.get("greeting")
    print greeting
    return render_template(
        "index.html",
        weather=weather,
        schedule=schedule,
        greeting=greeting)

