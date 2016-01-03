import datetime

import requests

WEATHER_API_URL = "http://api.openweathermap.org/data/2.5/forecast/daily"
WEATHER_API_LOCATION = "Seattle,WA"
WEATHER_API_KEY = "24ffa004a91a88adcab74f0f74040277"

DEFAULT_WEATHER = "wi-alien"
WEATHER_CODE_TO_ICON_MAP = {
    200: "wi-storm-showers",
    201: "wi-thunderstorm",
    202: "wi-thunderstorm",
    210: "wi-lightning",
    211: "wi-lightning",
    212: "wi-lightning",
    221: "wi-lightning",
    230: "wi-storm-showers",
    231: "wi-storm-showers",
    232: "wi-storm-showers",

    300: "wi-sprinkle",
    301: "wi-sprinkle",
    302: "wi-sprinkle",
    310: "wi-sprinkle",
    311: "wi-sprinkle",
    312: "wi-sprinkle",
    313: "wi-sprinkle",
    314: "wi-sprinkle",
    321: "wi-sprinkle",

    500: "wi-rain",
    501: "wi-rain",
    502: "wi-rain",
    503: "wi-rain",
    504: "wi-rain-wind",
    511: "wi-sleet",
    520: "wi-rain-mix",
    521: "wi-rain-mix",
    522: "wi-rain-mix",
    531: "wi-rain-mix",

    600: "wi-snow",
    601: "wi-snow",
    602: "wi-snow",
    611: "wi-sleet",
    612: "wi-sleet",
    615: "wi-rain-mix",
    616: "wi-rain-mix",
    620: "wi-snow",
    621: "wi-snow",
    622: "wi-snow",

    701: "wi-fog",
    711: "wi-smoke",
    721: "wi-dust",
    731: "wi-sandstorm",
    741: "wi-fog",
    751: "wi-dust",
    761: "wi-dust",
    762: "wi-volcano",
    771: "wi-flood",
    781: "wi-tornado",

    800: "wi-day-sunny",
    801: "wi-cloudy",
    802: "wi-cloud",
    803: "wi-cloud",
    804: "wi-cloudy",
}

DAYS = {
    0: "mon",
    1: "tue",
    2: "wed",
    3: "thu",
    4: "fri",
    5: "sat",
    6: "sun",
}


def get_forecast():
    payload = {
        "q": WEATHER_API_LOCATION,
        "appid": WEATHER_API_KEY,
        "units": "imperial",
    }
    response = requests.get(WEATHER_API_URL, params=payload)
    if response.ok:
        result = response.json()
        for day in result.get("list", []):
            weather_id = day.get("weather", [{}])[0].get("id")
            dt = day.get("dt")
            if weather_id is None:
                continue
            day["weather"][0]["icon"] = WEATHER_CODE_TO_ICON_MAP.get(
                weather_id, DEFAULT_WEATHER)
            if dt is not None:
                day["weekday"] = DAYS.get(
                    datetime.date.fromtimestamp(dt).weekday())

        return result
    else:
        return None
