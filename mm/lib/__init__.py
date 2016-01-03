import time

from . import gcal
from . import greet
from . import weather


def pong():
    return {
        "response": "PONG",
        "timestamp": time.time(),
    }


def get_forecast():
    return weather.get_forecast()


def get_calendar(days=1):
    return gcal.get_events(future_days=days)


def get_greeting():
    return greet.get_greeting()


def get_icon_for_weather_code(code):
    return weather.WEATHER_CODE_TO_ICON_MAP.get(code, "wi-alien")
