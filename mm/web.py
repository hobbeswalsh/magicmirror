from flask import Blueprint
from flask import render_template

from concurrent import futures

from .lib import get_greeting
from .lib import get_calendar
from .lib import get_forecast

web = Blueprint('web', __name__)


@web.route('/')
def index():
    real_results = {"greeting": get_greeting()}
    with futures.ProcessPoolExecutor(max_workers=5) as executor:
        results = {
            executor.submit(get_calendar, 10): "schedule",
            executor.submit(get_forecast): "weather",
        }
        for future in futures.as_completed(results):
            topic = results[future]
            try:
                real_results[topic] = future.result()
            except Exception:
                real_results[topic] = "oops"

    schedule = real_results.get("schedule")
    weather = real_results.get("weather")
    greeting = real_results.get("greeting")
    return render_template(
        "index.html",
        weather=weather,
        schedule=schedule,
        greeting=greeting)
